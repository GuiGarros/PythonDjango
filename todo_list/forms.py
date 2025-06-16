# forms.py
from django import forms
from .models import Task
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Usuário")
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirme a Senha")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data
    

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'descricao', 'status']

class NewTaskForm(forms.ModelForm):
#    username = forms.CharField(max_length=100, required=True, label="Usuário")
   class Meta:
        model = Task
        fields = ['name', 'descricao', 'status']
