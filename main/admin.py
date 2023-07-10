from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import (
    Project, Blog, Service, SubService, HomeSlider, CustomerReview, Email, PropertyCoordinates,
    Employee, PartnerSlider, Quote, ContactUs, Product, Booking, ProductImage, Property
)

# Register your models here.

admin.site.site_title = 'Bomach Group Admin'
admin.site.index_title = 'Welcome to Bomach Group'
# admin.site.site_header = format_html('<a href="/admin/"><img src="/static/assets/img/logo/bomach-logo-full.jpeg" style="height: 100px"></a>')

admin.site.unregister(Group)

# Experimental feature

@admin.register(PropertyCoordinates)
class PropertyCoordinatesAdmin(admin.ModelAdmin):
    fields = ('name', 'x', 'y', 'date')
    list_display = ('name', 'x', 'y', 'date')
    search_fields = ('name', 'x', 'y')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'slug', 'phone', 'email', 'location', 'coordinates', 'image', 'content', 'priority', 'activate', 'from_admin', 'date')
    list_display = ('id', 'name', 'slug', 'phone', 'email', 'location', 'priority', 'activate', 'from_admin', 'date')
    search_fields = ('name', 'id', 'location')


# in production

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'image', 'content', 'rating', 'priority', 'date')
    list_display = ('name', 'slug', 'rating', 'priority', 'date')
    search_fields = ('name','slug')


@admin.register(SubService)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name', 'service', 'slug', 'image', 'content', 'rating', 'priority', 'date')
    list_display = ('name', 'slug', 'rating', 'priority', 'date')
    search_fields = ('name','slug')



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'sub_service', 'image', 'content', 'priority', 'date')
    list_display = ('name', 'slug', 'priority', 'date')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'slug', 'service', 'video', 'content', 'product_images', 'priority', 'date')
    list_display = ('id', 'name', 'slug', 'priority', 'date')
    search_fields = ('name', 'id')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'priority', 'date')
    list_display = ('name', 'priority', 'date')
    search_fields = ()


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'author', 'image', 'content', 'priority', 'date')
    list_display = ('title', 'slug', 'author', 'priority', 'date')
    search_fields = ('title', 'author')


@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    fields = ('big_text', 'small_text', 'image', 'priority', 'date')
    list_display = ('big_text', 'small_text', 'priority', 'date')
    search_fields = ('big_text',)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    fields = ('name', 'review', 'occupation', 'priority', 'date')
    list_display = ('name', 'review', 'occupation', 'priority', 'date')
    search_fields = ('name', 'occupation')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('name', 'job_title', 'facebook', 'twitter', 'instagram', 'image', 'priority', 'date')
    list_display = ('name', 'job_title', 'facebook', 'twitter', 'instagram', 'priority', 'date')
    search_fields = ('name', 'job_title')


@admin.register(PartnerSlider)
class PartnerSliderAdmin(admin.ModelAdmin):
    fields = ('company', 'image', 'priority', 'date')
    list_display = ('company', 'priority', 'date')
    search_fields = ('company',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    fields = ('name', 'meeting_time', 'duration_in_minutes', 'phone', 'email', 'location', 'message', 'service', 'sub_service', 'date')
    list_display = ('name', 'meeting_time', 'duration_in_minutes', 'phone', 'email', 'location', 'message', 'date')
    ordering = ('meeting_time',)
    search_fields = ('name',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    fields = ('name', 'phone', 'email', 'location', 'message', 'service', 'sub_service', 'date')
    list_display = ('name', 'phone', 'email', 'location', 'message', 'date')
    search_fields = ('name',)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    fields = ('name', 'phone', 'email', 'location', 'message', 'date')
    list_display = ('name', 'phone', 'email', 'location', 'message', 'date')
    search_fields = ('name',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'date')
    search_fields = ('email', 'is_active')
    list_filter = ('date',)

