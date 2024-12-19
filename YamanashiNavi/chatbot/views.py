from django.shortcuts import render
from .models import Message
from openai import OpenAI
import os

from .forms import MessageForm

def ChatBot(request):

    params = {

        "title": "ChatBot",
        "form": MessageForm(),
        'response': ""
    }

    if request.method == "GET":
        return render(request, "chatbot/chatbot.html", params)
    
    elif request.method == 'POST':
        form = MessageForm(request.POST) 
        if form.is_valid():
            form.save()
            #return redirect('success')  # 保存後のリダイレクト先
            message = ""

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # フォームからのデータ取得
        system_prompt = form.cleaned_data.get('system_prompt', "")
        prompt = form.cleaned_data.get('prompt', "")
        message = ""

        try:
        # OpenAI APIを使用してレスポンスを生成
            response = client.chat.completions.create(
                model="gpt-4o",  # 使用するモデルを指定
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # 応答の創造性を制御（0-1の範囲、高いほど創造的）
                # max_tokens=150    # 応答の最大トークン数
            )
            message = response.choices[0].message.content
    
        except Exception as e:
            message = f"エラーが発生しました: {str(e)}"

    params['response'] = message

    return render(request, 'chatbot/chatbot.html', params)
