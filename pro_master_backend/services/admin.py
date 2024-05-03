from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import (Appointment,
                     Category,
                     Comment,
                     Employee,
                     Favorite,
                     Image,
                    #  Location,
                    #  LocationService,
                     Review,
                     ServiceProfile,
                     ServiceProfileCategory,
                     Schedule)

class ServiceProfileToCategory(admin.TabularInline):
    model = ServiceProfileCategory
    min_num = 1


class ServiceProfileToImage(admin.TabularInline):
    model = Image
    min_num = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_profile', 'image')
    search_fields = ('service_profile',)
    list_filter = ('service_profile',)
    empty_value_display = '-пусто-'


# @admin.register(Location)
# class LocationAdmin(OSMGeoAdmin):
#     list_display = ('id',
#                     'address',
#                     'point')
#     list_display_links = ('address',)
#     search_fields = ('address',)
#     list_filter = ('address',)
#     empty_value_display = '-пусто-'


@admin.register(ServiceProfile)
class ServiceProfileAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'created',
                    'additions_in_favorite_count')
    list_display_links = ('name',)
    search_fields = ('name', 'owner')
    list_filter = ('owner',)
    empty_value_display = '-пусто-'

    inlines = [ServiceProfileToCategory, ServiceProfileToImage]

    @admin.display(description='Количество добавлений в избранное')
    def additions_in_favorite_count(self, service):
        return service.in_favorite_for_clients.all().count()


@admin.register(ServiceProfileCategory)
class ServiceProfileCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_profile', 'category')
    search_fields = ('service_profile', 'category')
    list_filter = ('service_profile', 'category')
    empty_value_display = '-пусто-'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'phone_number',
                    'first_name',
                    'last_name',
                    'organization')
    list_display_links = ('id',)
    search_fields = ('phone_number', 'first_name', 'last_name')
    list_filter = ('organization',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_profile', 'client_profile')
    list_display_links = ('id',)
    search_fields = ('service_profile', 'client_profile')
    list_filter = ('service_profile', 'client_profile')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_profile', 'author', 'score')
    list_display_links = ('service_profile',)
    search_fields = ('service_profile', 'author')
    list_filter = ('service_profile', 'author')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author')
    list_display_links = ('review',)
    search_fields = ('review', 'author')
    list_filter = ('review', 'author')
    empty_value_display = '-пусто-'


# @admin.register(LocationService)
# class LocationServiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'location', 'service')
#     search_fields = ('location', 'service')
#     list_filter = ('location', 'service')
#     empty_value_display = '-пусто-'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'service_profile',
                    'date',
                    'start',
                    'end')
    list_display_links = ('service_profile',)
    search_fields = ('service_profile',)
    list_filter = ('service_profile', 'date', 'start', 'end')
    empty_value_display = '-пусто-'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'client_profile',
                    'schedule',
                    'appointment_time')
    list_display_links = ('client_profile',)
    search_fields = ('client_profile',)
    list_filter = ('client_profile', 'schedule', 'appointment_time')
    empty_value_display = '-пусто-'

