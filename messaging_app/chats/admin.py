from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Conversation, Message

User = get_user_model()

admin.site.register(User, UserAdmin)

@admin.register(Conversation)
class ConversationApp(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    list_filter = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation_id', 'sender_id',
                    'message_body', 'sent_at')
    list_filter = ('sent_at',)
