from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Message, Notification

User = get_user_model()

admin.site.register(User, UserAdmin)

@admin.register(Notification)
class NotificationApp(admin.ModelAdmin):
    list_display = ('notification_id',
                    'sender_id', 'message_id',
                    'read', 'created_at')
    list_filter = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender_id',
                    'receiver_id', 'content',
                    'timestamp')
    list_filter = ('timestamp',)
