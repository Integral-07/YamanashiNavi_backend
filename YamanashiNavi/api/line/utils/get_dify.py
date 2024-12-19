import requests
import json, os

from ..models import Session

# Dify APIのベースURL
BASE_URL = "https://api.dify.ai/v1/chat-messages"
API_KEY = os.getenv('DIFY_API_KEY')
if not API_KEY:
    raise ValueError("DIFY_API environment variable is not set.")

def get_dify_response(query: str, user: str, session) -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数

    :param query: ユーザーの質問
    :param user: ユーザー識別子
    :return: APIからの応答テキスト
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": session.conversation_id,
        "user": user
    }
    
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    if(session.conversation_id == ""):
        session = Session(user_id=session.user_id, conversation_id=response.json()['conversation_id'], lang_setting=session.lang_setting)
        session.save()

    return response.json()['answer']