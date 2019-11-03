from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from . import models
class MusicAdmin(admin.ModelAdmin):
    list_display = ("name", "url" ,"description" ,"lyrics", "liked_user_")
    def liked_user_(self, obj):
        return "\n".join([s.username for s in obj.liked_user.all()])


class SynerAdmin(admin.ModelAdmin):
    list_display = ("user",  "liked_music_")
    def liked_music_(self, obj):
        return "\n".join([s.name for s in obj.all()])

# class PlaylistAdmin(admin.ModelAdmin):
#     list_display = ("name", "music_", "created_by", "created_on")
#     def music_(self, obj):
#         return "\n".join([s.name for s in obj.music.all()])


class StudioAdmin(admin.ModelAdmin):
    list_display = ("name","status","headcount","link","host", "start_time","end_time","music_")
    def music_(self, obj):
        return "\n".join([s.name for s in obj.music.all()])
    # def play_list_(self, obj):
    #     return str(obj.id)
    #     ,"play_list_"

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("participant_user_",  "role","studio_")
    def participant_user_(self, obj):
        return str(obj.id)
    def studio_(self, obj):
        return str(obj.id)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name",  "text","created_on","commented_on_")
    def commented_on_(self, obj):
        return str(obj.id)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "studio_")
    def studio_(self, obj):
        return str(obj.id)
    
admin.site.register(models.Music, MusicAdmin)
admin.site.register(models.Syner, SynerAdmin)
# admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Studio, StudioAdmin)
admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.History, HistoryAdmin)
