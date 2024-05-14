from django.contrib import admin

from .models import ClientProfile


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
