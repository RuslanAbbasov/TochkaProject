import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, StreamingHttpResponse
from django.http import HttpResponse
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, VideoUploadForm
from .models import Video, Profile
from .services import open_file, add_like, remove_like, is_fan, get_fans


# Create your views here.


def homePage(request):
    return render(request, 'homePage.html', {'video_list': Video.objects.all()})


def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    # _profile = get_object_or_404(Profile, id=pk)
    # _user = get_object_or_404(User, id=pk)
    url = _video.generate_download_url()
    return render(request, "video.html", {"video": _video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


# def download(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         file = request.FILES['file']
#         preview = request.FILES['preview']
#         profile = Profile.objects.get(user=request.user)
#         upload_video = Video(user=profile, title=title, description=description, file=file, preview=preview)
#         upload_video.save()
#         messages.success(request, 'Video has been uploaded.')
#
#     return render(request, 'upload.html')


def upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # form = form.save(commit=False)
            newVideo = Video(user=request.user,
                             title=form.cleaned_data['title'],
                             description=form.cleaned_data['description'],
                             preview=form.cleaned_data['preview'],
                             file=form.cleaned_data['file'])
            newVideo.save()
            messages.success(request, f'Ваше видео успешно загружено.')
            return redirect('homePage')
        else:
            messages.success(request, form.errors)
            messages.success(request, form.non_field_errors)
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


def myVideo(request):
    return render(request, 'myVideo.html', {'video_list': Video.objects.filter(user=request.user.id)})
