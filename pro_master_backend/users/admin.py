from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'email',
                    'phone_number',
                    'date_joined',
                    'is_master')
    list_display_links = ('email',)
    search_fields = ('email',)
    list_filter = ('email',)
    empty_value_display = '-пусто-'
