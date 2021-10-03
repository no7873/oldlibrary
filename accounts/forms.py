from .models import User
from django import forms

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    email = forms.EmailField(label='이메일', widget=forms.EmailInput)
    nickname = forms.CharField(label='이름', widget=forms.TextInput)
    address = forms.CharField(label='주소', widget=forms.TextInput)
    detailadd = forms.CharField(label='상세주소', widget=forms.TextInput)
    phone = forms.CharField(label='전화번호', widget=forms.TextInput)


    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'address', 'detailadd', 'phone']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 다릅니다.')
        return cd['password2']