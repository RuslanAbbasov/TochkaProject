from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Video


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'preview', 'file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VideoUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(VideoUploadForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()
