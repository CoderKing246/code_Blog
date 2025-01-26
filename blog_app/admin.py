# from django.contrib import admin
# from .models import Posts,Message
# # Register your models here.
# admin.site.register(Posts)
# admin.site.register(Message)

from django.contrib import admin
from .models import Posts, Message

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # Display user in the admin list view

    def save_model(self, request, obj, form, change):
        # Automatically assign the logged-in user when saving a new post
        if not obj.pk:  # Only set user if the post is new
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Posts, PostsAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('body', 'user', 'post', 'created_at')  # Display related fields in admin
    list_filter = ('created_at',)  # Filter by creation date
    search_fields = ('body',)  # Enable search by message content

admin.site.register(Message, MessageAdmin)
