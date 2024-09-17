## Flask-SocketIO Bot Conversations API

This Python-based API fetches and organizes bot conversations from the Botpress platform using Flask and Flask-SocketIO. It handles real-time requests via WebSockets and groups messages by bot integrations and conversations, making it easier to process large volumes of chat data.

### Features:
- **Real-time communication**: Uses WebSockets (SocketIO) for real-time interaction.
- **Integration handling**: Fetches bot integrations from Botpress and structures conversations accordingly.
- **Message organization**: Groups messages by bot integration and conversation for better data management.
- **Error handling**: Robust error handling mechanism that notifies the client about any issues during execution.

### Key Functions:
- `update_botdata`: Updates bot data with a new integration ID.
- `get_bot_integrations`: Fetches all bot integrations from Botpress API.
- `get_webchat_integration`: Retrieves specific webchat integration data.
- `list_conversations_webchat`: Lists all conversations in the webchat integration.
- `get_conversation`: Fetches all messages from a specific conversation.
- `get_conversation_messages`: Gathers messages from all conversations.
- `group_messages_by_integration`: Organizes conversations by integration.
- `group_messages_by_conversation`: Further structures conversations and messages by integration and conversation ID.

### How it works:
1. The client sends a `get_conversations` event to the server.
2. The server retrieves all bot integrations and conversations from the Botpress API.
3. Messages are grouped and structured, then emitted back to the client for further use.

This API enables efficient real-time conversation tracking, making it a powerful tool for applications involving chatbots and integrations.
