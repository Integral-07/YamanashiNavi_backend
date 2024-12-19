from openai import OpenAI
from .get_dify import get_dify_response
from .get_gpt import get_gpt_response
import json, re
from urllib.parse import quote

from ..models import Session

#client = OpenAI(api_key=os.getenv("OPENAI_ASSISTANT_API_KEY"))

def create_carousel_template(_data_json):
    columns = []
    
    pattern = r"```json\s(.*?)\s```"
    match = re.search(pattern, _data_json, re.DOTALL)
    #_data_json = _data_json.replace("'", '"')

    if match:
        data_json = match.group(1)
    else:
        data_json = _data_json

    print(data_json)
    data = json.loads(data_json)
    print("[data]", data)
    idx = 0

    base_url = "https://maps.google.com/maps?q="
    while True:
        try:
            #image_url = get_dify_response(user="Re", query=f"{data[idx]["place"]}の画像のURLを返して")
            location = data[idx]["place"]
            encoded_url = base_url + quote(location)

            columns.append({
            "thumbnailImageUrl": "https://www.fuji-net.co.jp/wp/wp-content/uploads/2022/08/0.jpg",
            "imageBackgroundColor": "#FFFFFF",
            "title": data[idx]["place"],
            "text": data[idx]["description"],
            "defaultAction":{

                "type": "uri",
                "label": "View on GoogleMap",
                "uri": encoded_url
            },
            "actions": [
                {
                    "type": "uri",
                    "label": "View on GoogleMap",
                    "uri": encoded_url
                }
            ]
            })

            idx += 1;
        except IndexError:
            break

    return {
        "type": "template",
        "altText": "recommendation",
        "template": {
            "type": "carousel",
            "columns": columns,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover"
        }
    }

def create_single_text_message(event, session):
    
    response = ""

    try:
        if(event['type'] == "follow"):
            try:
                Session.objects.get(user_id=event['source']['userId'])
            except:
                new_session = Session(user_id=event['source']['userId'], conversation_id="", lang_setting='ja')
                new_session.save()

        elif(event['type'] == "unfollow"):
            try:
                session = Session.objects.get(user_id=event['source']['userId'])
                session.delete()
            except Session.DoesNotExist:
                # セッションが見つからない場合（フォローされていない場合）は何もしない
                pass

        elif(event['type'] == "image"):

            response = "いい写真ですね！\n画像に対するAI応答は今後実装予定です"


        elif(event['type'] == "message"):

            if(event['message']['text'] == "session reset"):
                try:
                    old_session = Session.objects.get(user_id=event['source']['userId'])
                    new_session = Session(user_id=old_session.user_id, conversation_id="", lang_setting=old_session.lang_setting)
                    new_session.save()
                except:
                    pass

            elif(event['message']['type'] == "text"):

                query = event['message']['text']
                user = event['source']['userId']

                response = get_dify_response(query, user, session)
                
            elif(event['message']['type'] == "location"):

                latitude = event['message']['latitude']
                longitude = event['message']['longitude']
                address = event['message']['address']
                query = f'今、緯度{latitude}、経度{longitude}の{address}にいます。周辺のおすすめをおしえてください。' + \
                    '出力形式は、場所名は"place",所在地は"address",GoogleMapへのリンクは"gmap", それ以外の説明は60文字以内にまとめて"description"に紐づけてjson形式で出力してください。 \
                        json形式とは[{"place": "", "address": "", "gmap": "", "description": ""}, {"place": "", "address": "", "gmap": "", "description": ""}]です。'
                user = event['source']['userId']

                response = get_dify_response(query, user, session)
                print(response)

    except Exception as e: 
        response = f"Error occurred: {str(e)}"

    return response