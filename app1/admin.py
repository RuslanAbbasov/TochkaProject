from django.contrib import admin
from .models import Profile, Video, Likes
from .forms import VideoUploadForm

admin.site.register(Profile)
admin.site.register(Likes)


# admin.site.register(Video)
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Post admin."""
    list_display = ('id', 'user', 'title', 'description', 'preview')
    search_fields = ('title', 'user.username')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url',)
        form = super(VideoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
# Register your models here.
