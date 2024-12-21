from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
import os, json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
"""
from django.conf import settings
from rest_framework import generics, status, views, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    '''ユーザのログイン処理
    
    Args:
        APIView (class): rest_framework.viewsのAPIViewを受け取る
    ''''''

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
"""

def Signup(request):
    if request.method == "POST":
        try:
            # リクエストボディをJSONとして読み取る
            data = json.loads(request.body)

            # 必須フィールドの確認
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            password_conf = data.get("password_conf")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required."},
                    status=400
                )
            
            if (password != password_conf):
                return Response(
                    {"error": "password does not match"},
                    status=400
                )
            
            else:
                new_user = User(username=username, email=email, password=password)
                new_user.save()
                user = authenticate(username=username, password=password)
                user_id = user.user_id
                return Response(
                    {"user_id": user_id},
                    status=200
                )   

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format."},
                status=400
            )

    # POST以外のリクエストへの対応
    return Response(
        {"error": "POST method required."},
        status=405
    )

def login(request):
    if request.method == "POST":
        try:
            # リクエストボディをJSONとして読み取る
            data = json.loads(request.body)

            # 必須フィールドの確認
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required."},
                    status=400
                )

            # 認証処理
            user = authenticate(username=username, password=password)

            if user is not None:
                # 認証成功時のレスポンス
                return Response(
                    {"message": "Login successful.", "user_id": user.user_id},
                    status=200
                )
            else:
                # 認証失敗時のレスポンス
                return Response(
                    {"error": "Invalid username or password."},
                    status=401
                )

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format."},
                status=400
            )

    # POST以外のリクエストへの対応
    return Response(
        {"error": "POST method required."},
        status=405
    )

from ..line.utils.get_dify import get_dify_response
from ..line.models import Session

@api_view(['GET', 'POST'])
def conversation(request, user_id):
    """
    会話履歴を取得（GET）または新しいメッセージを追加してAIの応答を生成（POST）
    """
    if request.method == 'GET':
        # メッセージをタイムスタンプ順に取得
        messages = Message.objects.filter(user_id=user_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # クライアントからのリクエストを保存
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # 新しいメッセージを保存
            user_message = serializer.save()

            try:
                new_session = Session(user_id=user_id, conversation_id="", lang_setting='ja')
                ai_message_content = get_dify_response(user_message, user_id, session=new_session)

                # AIからの応答を保存
                ai_message = Message(content=ai_message_content, role='bot', user_id=user_id)
                ai_message.save()

                # クライアントに応答を返す
                return Response({
                    "user_message": serializer.data,
                    "ai_message": MessageSerializer(ai_message).data
                }, status=201)

            except Exception as e:
                return Response({"error": f"AI応答の生成中にエラーが発生しました: {str(e)}"}, status=500)

        return Response(serializer.errors, status=400)
