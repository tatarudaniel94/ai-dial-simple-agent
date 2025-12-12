import os

from task.client import DialClient
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role
from task.prompts import SYSTEM_PROMPT
from task.tools.users.create_user_tool import CreateUserTool
from task.tools.users.delete_user_tool import DeleteUserTool
from task.tools.users.get_user_by_id_tool import GetUserByIdTool
from task.tools.users.search_users_tool import SearchUsersTool
from task.tools.users.update_user_tool import UpdateUserTool
from task.tools.users.user_client import UserClient
from task.tools.web_search import WebSearchTool

DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv('DIAL_API_KEY')

def main():
    # 1. Create UserClient
    user_client = UserClient()
    
    # 2. Create DialClient with all tools
    tools = [
        WebSearchTool(api_key=API_KEY, endpoint=DIAL_ENDPOINT),
        GetUserByIdTool(user_client=user_client),
        SearchUsersTool(user_client=user_client),
        CreateUserTool(user_client=user_client),
        UpdateUserTool(user_client=user_client),
        DeleteUserTool(user_client=user_client),
    ]
    
    dial_client = DialClient(
        endpoint=DIAL_ENDPOINT,
        deployment_name="gpt-4o",
        api_key=API_KEY,
        tools=tools
    )
    
    # 3. Create Conversation and add System message
    conversation = Conversation()
    conversation.add_message(Message(role=Role.SYSTEM, content=SYSTEM_PROMPT))
    
    print("\n🤖 User Management Agent ready. Type your request (Ctrl+C to exit):\n")
    
    # 4. Run infinite loop
    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            
            # Add User message to Conversation
            conversation.add_message(Message(role=Role.USER, content=user_input))
            
            # Call DialClient with conversation history
            ai_response = dial_client.get_completion(conversation.get_messages())
            
            # Add Assistant message to Conversation and print its content
            conversation.add_message(ai_response)
            print(f"\n🤖 Assistant: {ai_response.content}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


main()

# Request sample:
# Add Andrej Karpathy as a new user