from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
import os

from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginView(APIView):
    """ユーザのログイン処理
    
    Args:
        APIView (class): rest_framework.viewsのAPIViewを受け取る
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_ok)
            max_age = settings.COOKIES_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)

            return response
        
        return Response({'errMsg': 'ユーザ認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)

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
                
                ai_message_content = "返信"#get_dify_response(query, user, session)

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
