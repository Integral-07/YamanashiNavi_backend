import requests, json, os
from ..models import HistoryModel

BASE_URL = "https://api.dify.ai/v1/chat-messages"
API_KEY = os.getenv('DIFY_API_KEY')
if not API_KEY:
    raise ValueError("DIFY_API environment variable is not set.")

def get_dify_response(query: str, user: str, history) -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数

    :param query  : ユーザーの質問
    :param user   : ユーザ名
    :param history: ユーザの会話履歴
    :return: APIからの応答テキスト
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
            "inputs": {},
            "query": query,
            "response_mode": "streaming",
            "user": user,
    }
    
    if history.conversation_id:

        data["conversation_id"] = history.conversation_id       

    
    #response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
    #response.raise_for_status()

    result = ""
    with requests.post(BASE_URL, json=data, headers=headers, stream=True) as response:
        # ステータスコードが200であることを確認
        print(response.text)
        response.raise_for_status()
        for chunk in response.iter_lines():
            if chunk:  # 空の行をスキップ
                    # バイナリデータをデコードし、JSONとしてパース
                chunk_data = chunk.decode('utf-8')
                try:
                    #print(chunk_data)
                    json_data = chunk_data.split(":", 1)[1].strip()
                    chunk_json = json.loads(json_data)
                    if "answer" in chunk_json:
                        result += str(chunk_json.get("answer"))

                    if(history.conversation_id == ""):
                        updated_history = HistoryModel(id=history.id, conversation_id=chunk_json.get('conversation_id'), user=history.user)
                        updated_history.save()

                except json.JSONDecodeError:
                    result += "Error decoding JSON:" + str(chunk_data)
    
    return result