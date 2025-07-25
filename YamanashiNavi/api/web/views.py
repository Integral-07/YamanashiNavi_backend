from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.views import APIView
from .authentication import CustomJWTAuthentication
from django.contrib.auth.models import User
from .serializer import HistorySerializer, MessageSerializer
from .models import HistoryModel, MessageModel
from .utils.dify_response import get_dify_response

class HistoryView(APIView):

    authentication_classes = [ CustomJWTAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def get(self, request):

        user = User.objects.get(id=request.auth['user_id'])
        history =  get_object_or_404(HistoryModel, user=user)
        serializer = HistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):

        user = User.objects.get(id=request.auth['user_id'])
        history = get_object_or_404(HistoryModel, user=user)
        if history:
            data = request.data
            new_message = data.get('content')
            new_message_model = MessageModel(owner=history, role='user', content=new_message)
            new_message_model.save()

            # Response from AI
            try:
                ai_response = get_dify_response(query=new_message, history=history)
            except Exception as e:
                ai_response = "AI生成エラーです。\nAPIの有効期限が切れている可能性があります" + e
            new_ai_message = MessageModel(owner=history, role='ai', content=ai_response)
            new_ai_message.save()

            try:
                messages_to_delete = MessageModel.objects.filter(owner=history).order_by('-time_stamp')[50:]
                messages_to_delete.delete()
            except:
                pass
            serializer = MessageSerializer(new_ai_message)
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')

        return Response(status=status.HTTP_204_NO_CONTENT)


class IsAuthView(APIView):

    def get(self, request):

        if request.user.is_authenticated:
            return Response({"is_authenticated": True}, status=status.HTTP_200_OK)
        else:
            return Response({"is_authenticated": False}, status=status.HTTP_200_OK)



class SignupView(APIView):

    authentication_classes = [ JWTAuthentication ]
    permission_classes = [ ]

    def post(self, request):
        """
        ユーザーの新規登録処理
        """
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        # バリデーションチェック
        if not username or not email or not password:
            return Response({"error": "全てのフィールドを入力してください"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "このユーザー名は既に使用されています"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "このメールアドレスは既に登録されています"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({"error": "パスワードは8文字以上で入力してください"}, status=status.HTTP_400_BAD_REQUEST)

        # ユーザー作成
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        new_history = HistoryModel(user=user)
        new_history.save()

        first_message = MessageModel(owner=new_history, role="ai", content=f"{user.username}さん、こんにちは！\nやまなしNaviへようこそ🌸\n\n山梨の観光スポットやグルメ、旅プラン作りをお手伝いするよ✨\n「行きたい場所」や「気になること」があれば、気軽に聞いてね！\n山梨の魅力をいっぱい詰め込んだ度を一緒に作ろう💼💕")
        first_message.save()

        return Response({"message": "ユーザー登録が完了しました"}, status=status.HTTP_201_CREATED)




class LoginView(APIView):

    """ユーザのログイン処理
    
    Args:
        APIView (class): rest_framework.viewのAPIViewを受け取る
    """

    authentication_classes = [ JWTAuthentication ]
    permission_classes = [ ]


    def post(self, request):

        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)

        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)

            return response

        return Response({'errMsg': 'ユーザの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)



class RetryView(APIView):

    authentication_classes = [ JWTAuthentication ]
    permission_classes = []

    def post(self, request):

        request.data['refresh'] = request.META.get('HTTP_REFRESH_TOKEN')
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get('access', None)
        refresh = serializer.validated_data.get('refresh', None)

        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.cookie_set('access', access, httponly=True, max_age=max_age)
            response.cookie_set('refresh', refresh, httponly=True, max_age=max_age)

            return response

        return Response({'errMsg': 'ユーザの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args):

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
