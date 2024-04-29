from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import (Category,
                     Comment,
                     Image,
                    #  Location,
                    #  LocationService,
                     Review,
                     ServiceProfile,
                     ServiceProfileCategory)

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
    prepopulated_fields = {'slug': ('name',)}
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'author', 'score')
    list_display_links = ('service',)
    search_fields = ('service', 'author')
    list_filter = ('service', 'author')
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


# @admin.register(Schedule)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display = ('id',
#                     'service',
#                     'datetime_start',
#                     'datetime_end')
#     list_display_links = ('service',)
#     search_fields = ('service',)
#     list_filter = ('service',)
#     empty_value_display = '-пусто-'


# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('id',
#                     'service',
#                     'client',
#                     'appointment_datetime_start',
#                     'appointment_datetime_end')
#     list_display_links = ('service', 'client')
#     search_fields = ('service', 'client')
#     list_filter = ('service', 'client')
#     empty_value_display = '-пусто-'

