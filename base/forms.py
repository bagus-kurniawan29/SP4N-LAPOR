from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 
from django.contrib.auth.forms import AuthenticationForm
from base import views
from .models import Pengaduan

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nik = forms.CharField(max_length=16, required=False) 
    
    class Meta:
        model = CustomUser 
        fields = ['username', 'email', 'nik']     
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.nik = self.cleaned_data.get('nik')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user 

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class PengaduanForm(forms.ModelForm):
    class Meta:
        model = Pengaduan
        fields = ['tanggal_pelaporan', 'isi_laporan', 'gambar_bukti']