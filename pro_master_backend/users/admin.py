from django.contrib import admin

from .models import CustomUser, ClientProfile


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


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'client',
                    'profile_name',
                    'first_name',
                    'last_name',)
    list_display_links = ('profile_name',)
    search_fields = ('profile_name',)
    list_filter = ('profile_name',)
    empty_value_display = '-пусто-'
