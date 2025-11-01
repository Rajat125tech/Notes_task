from django.contrib import admin
from .models import Task, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','completed','created_at')
    search_fields = ('title','description','user__username')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id','user','task','title','created_at')
    search_fields = ('title','content','user__username','task__title')
