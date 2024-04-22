from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'date_joined',
                    'is_master')
    list_display_links = ('username',)
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
