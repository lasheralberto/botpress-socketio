from flask import Flask
from flask_socketio import SocketIO, emit
import requests
import json
 
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
 

class Conversations:
    def update_botdata(self, botdata, new_integration_id):
        botdata['integration_id'] = new_integration_id
        return botdata

    def get_bot_integrations(self, botdata):

        url = f"https://api.botpress.cloud/v1/admin/bots/{botdata['botid']}"
        headers = {
            "Accept": "application/json",
            "Authorization": botdata['bearer'],
            "X-bot-id": botdata['botid'],
            "X-workspace-id": botdata['workspace_id']
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)['bot']['integrations']

    def get_webchat_integration(self, auth_data):
        url = f"https://api.botpress.cloud/v1/admin/hub/integrations/{auth_data['integration_id']}"
        headers = {
            "accept": "application/json",
            "authorization": auth_data['bearer'],
            "x-bot-id": auth_data['botid'],
            "x-workspace-id": auth_data['workspace_id']
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def list_conversations_webchat(self, auth_data):
        url = "https://api.botpress.cloud/v1/chat/conversations"
        headers = {
            "authorization": auth_data['bearer'],
            "accept": "application/json",
            "x-integration-id": auth_data['integration_id'],
            "x-bot-id": auth_data['botid']
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_conversation(self, conversationid, auth_data):
        url = f"https://api.botpress.cloud/v1/chat/messages?conversationId={conversationid}"
        headers = {
            "authorization": auth_data['bearer'],
            "accept": "application/json",
            "x-integration-id": auth_data['integration_id'],
            "x-bot-id": auth_data['botid']
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_conversation_messages(self, auth_data):
        conversations = self.list_conversations_webchat(auth_data)
        conversation_map = {}
        conversations_list = []
        for conv in conversations['conversations']:
            conversation = self.get_conversation(conv['id'], auth_data)
            conversation_map[conv['id']] = conversation['messages']
            conversations_list.append(conversation_map)
        return conversations_list

    def group_messages_by_integration(self, botdata, integrations):
        all_messages = []
        for i in integrations:
            integration_data = {
                'name': integrations[i]['name'],
                'id': i
            }
            botd = self.update_botdata(botdata, i)
            conversations_messages = self.get_conversation_messages(botd)
            integration_data['messages'] = conversations_messages
            all_messages.append(integration_data)
        return all_messages

    def group_messages_by_conversation(self, data_grouped_by_integration):
        sorted_list = []
        for integration in data_grouped_by_integration:
            integration_name = integration['name']
            integration_id = integration['id']
            for message_dict in integration['messages']:
                for conversation_id, messages in message_dict.items():
                    sorted_list.append({
                        'conversation': conversation_id,
                        'integration_name': integration_name,
                        'integration_id': integration_id, 
                        'messages': messages
                    })
        return sorted_list

conversations = Conversations()

@socketio.on('get_conversations')
def handle_request_data(botdata):
    try:
        # Obtain integrations
        integrations = conversations.get_bot_integrations(botdata)
        
        # Group data by integration
        grouped_data_integration = conversations.group_messages_by_integration(botdata, integrations)
        
        # Group by conversation and integration
        data = conversations.group_messages_by_conversation(grouped_data_integration)
        
        # Emit the data back to the client
        socketio.emit('conversation_data', data)

    except Exception as e:
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    socketio.run(app, debug=True)
   



