from .models import User
from django import forms

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='아이디', widget=forms.TextInput, required=True, error_messages={'required': '아이디는 필수입력입니다.'})
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput, required=True, error_messages={'required': '비밀번호는 필수입력입니다.'})
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput, required=True, error_messages={'required': '비밀번호 확인을 해주세요.'})
    email = forms.EmailField(label='이메일', widget=forms.EmailInput, required=True, error_messages={'required': '이메일은 필수입력입니다.'})
    nickname = forms.CharField(label='이름', widget=forms.TextInput, required=True, error_messages={'required': '이름은 필수입력입니다.'})
    address = forms.CharField(label='주소', widget=forms.TextInput, required=False)
    detailadd = forms.CharField(label='상세주소', widget=forms.TextInput, required=False)
    phone = forms.CharField(label='전화번호', widget=forms.TextInput, required=True, error_messages={'required': '전화번호는 필수입력입니다.'})


    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'address', 'detailadd', 'phone']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        if password != password2:
            return self.add_error('password2', '비밀번호가 일치하지 않습니다.')
        if 8 > len(password):
            return self.add_error('password', '비밀번호는 8자 이상으로 입력해주세요.')
        if not (4 <= len(username) <= 20):
            return self.add_error('username', '아이디는 4~20자로 입력해 주세요.')

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if 8 > len(password):
    #         return self.add_error('password', '비밀번호는 8자 이상으로 입력해주세요.')
    #
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not (4 <= len(username) <= 20):
    #         return self.add_error('username', '아이디는 4~20자로 입력해 주세요.')

