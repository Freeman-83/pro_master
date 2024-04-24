from django.contrib import admin

from .models import CustomUser, ClientProfile, MasterProfile


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
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'client',
                    'username',
                    'first_name',
                    'last_name',)
    list_display_links = ('username',)
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


@admin.register(MasterProfile)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'master',
                    'category',
                    'username',
                    'first_name',
                    'last_name')
    list_display_links = ('username',)
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
