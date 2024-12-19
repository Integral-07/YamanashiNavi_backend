from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['prompt', 'system_prompt']
        labels = {
            'prompt': 'プロンプト',
            'system_prompt': 'システムプロンプト',
        }
        widgets = {
            'message1': forms.TextInput(attrs={'placeholder': 'ここにメッセージ1を入力'}),
            'message2': forms.TextInput(attrs={'placeholder': 'ここにメッセージ2を入力'}),
        }