from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from openai import ChatCompletion
import os

def login(request):
    pass

@api_view(['GET', 'POST'])
def conversation(request):
    """
    会話履歴を取得（GET）または新しいメッセージを追加してAIの応答を生成（POST）
    """
    if request.method == 'GET':
        # メッセージをタイムスタンプ順に取得
        messages = Message.objects.all().order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # クライアントからのリクエストを保存
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # 新しいメッセージを保存
            user_message = serializer.save()

            # OpenAI API キーの設定
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                return Response({"error": "OpenAI API key is not set."}, status=500)

            # OpenAI API 呼び出し
            try:
                ai_message_content = "返答"

                # AIからの応答を保存
                ai_message = Message(content=ai_message_content, role='bot')
                ai_message.save()

                # クライアントに応答を返す
                return Response({
                    "user_message": serializer.data,
                    "ai_message": MessageSerializer(ai_message).data
                }, status=201)

            except Exception as e:
                return Response({"error": f"AI応答の生成中にエラーが発生しました: {str(e)}"}, status=500)

        return Response(serializer.errors, status=400)
