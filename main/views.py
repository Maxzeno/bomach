from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django import forms

import json
from datetime import datetime, timedelta
from .models import (
    Project as ProjectModel, Blog as BlogModel, PropertyImage, Service as ServiceModel, Product as ProductModel,
    Employee, PartnerSlider, CustomerReview, HomeSlider, PropertyCategory as PropertyCategoryModel, SubPropertyCategory,
    Quote as QuoteModel, SubService, Booking as BookingModel, Property as PropertyModel, PropertyCoordinates)

from .forms import QuoteForm, ContactForm, BookingForm, EmailForm, SearchForm, PropertyForm, dynamic_field, PROPERTY_COORDINATE_NUM
from .utils import service_valid_options, property_category_valid_options

# Create your views here.

EMPLOYEES_COUNT = 18
PROJECT_COUNT = 31
HAPPY_CUSTOMER_COUNT = 43


class Base:
    context = {'services': ServiceModel.objects.all().order_by('-priority'), 'email_form': EmailForm()}

# Experimental feature

class Property(View, Base):
    def get(self, request):
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            properties = PropertyModel.objects.filter( 
                Q(name__icontains=query) | Q(location__icontains=query) | Q(id__icontains=query)
            )
        else:
            properties = PropertyModel.objects.all().order_by('-priority')
        return render(request, 'main/properties.html', {'form': form, 'properties': properties, **self.context})


class PropertyDetail(View, Base):
    def get(self, request, slug):
        the_property = get_object_or_404(PropertyModel, slug=slug)
        return render(request, 'main/property-details.html', {'property': the_property, **self.context})


class PropertyCreate(View, Base):
    def get(self, request):
        form = PropertyForm()
        return render(request, 'main/property-create.html', {'form': form, 'valid_options': ['select sub category'], **self.context})

    def post(self, request):
        form = PropertyForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        images = request.FILES.getlist('images')
        for image in images:
            if image.size > 5 * 1024 * 1024:  # Checking if the file size is greater than 5MB
                messages.error(request, 'each file size should be less than 5MB', extra_tags='danger')
                return render(request, 'main/property-create.html', {'form': form, 'valid_options': ['select sub category'], **self.context})
            
        if form.is_valid():
            property = form.save()
            for image in images:
                PropertyImage.objects.create(image=image, property=property)

            messages.success(request, 'Success we will review it and get back to you')
            form = PropertyForm()
            return render(request, 'main/property-create.html', {'form': form, 'valid_options': ['select sub category'], **self.context})

        print(form.errors)
        print(dir(form))
        messages.error(request, 'Fill the form properly', extra_tags='danger')
        return render(request, 'main/property-create.html', {'form': form, 'valid_options': ['select sub category'], **self.context})

# In Production 


class Index(View, Base):
    def get(self, request):
        projects = ProjectModel.objects.all().order_by('-priority')

        product_data = []

        for i in self.context['services']:
            products_filter = ProductModel.objects.filter(service=i).order_by('-priority')
            product_data.append([i, products_filter])

        blogs3 = BlogModel.objects.all().order_by('-priority')[:3]
        employees_count = Employee.objects.count() + EMPLOYEES_COUNT
        project_count = ProjectModel.objects.count() + PROJECT_COUNT
        customer = CustomerReview.objects.all()
        happy_customer_count = customer.count() + HAPPY_CUSTOMER_COUNT
        happy_customer = customer.order_by('-priority')[:100]
        partners = PartnerSlider.objects.all().order_by('-priority')
        home_sliders = HomeSlider.objects.all().order_by('-priority')[:20]

        valid_options = service_valid_options(ServiceModel, SubService)

        form = QuoteForm()
        return render(request, 'main/index.html', {'projects': projects, 'blogs3': blogs3, 'product_data': product_data,
            'employees_count': employees_count, 'project_count': project_count, 'home_sliders': home_sliders, 
            'happy_customer': happy_customer, 'happy_customer_count': happy_customer_count,
            'partners': partners, 'form': form, "valid_options": valid_options, **self.context})

    def post(self, request):
        projects = ProjectModel.objects.all().order_by('-priority')
        services3 = ServiceModel.objects.all().order_by('-priority')[:3]
        employees_count = Employee.objects.count() + EMPLOYEES_COUNT
        project_count = ProjectModel.objects.count() + PROJECT_COUNT
        customer = CustomerReview.objects.all()
        happy_customer_count = customer.count() + HAPPY_CUSTOMER_COUNT
        happy_customer = customer.order_by('-priority')[:100]
        partners = PartnerSlider.objects.all().order_by('-priority')
        home_sliders = HomeSlider.objects.all().order_by('-priority')[:20]

        product_data = []

        for i in self.context['services']:
            products_filter = ProductModel.objects.filter(service=i).order_by('-priority')
            product_data.append([i, products_filter])

        valid_options = service_valid_options(ServiceModel, SubService)

        form = QuoteForm(request.POST)

        context = {'projects': projects, 'services3': services3, 'product_data': product_data,
                'employees_count': employees_count, 'project_count': project_count, 'home_sliders': home_sliders, 
                'happy_customer': happy_customer, 'happy_customer_count': happy_customer_count,
                'partners': partners, 'form': form, **self.context}

        if form.is_valid():
            quote_model = form.save()

            messages.success(request, 'Message has been received')
            context['form'] = QuoteForm()
            return render(request, 'main/index.html', context)

        messages.error(request, 'Invalid values fill try again', extra_tags='danger')
        return render(request, 'main/index.html', context)



class GetSubService(View):
    def get(self, request):
        return JsonResponse([], safe=False)

    def post(self, request):
        service_id = request.POST.get('service_id')
        service = ServiceModel.objects.get(pk=service_id)
        children = SubService.objects.filter(service=service.pk).order_by('-priority')
        child_data = [{'id': child.pk, 'name': child.name} for child in children]
        return JsonResponse(child_data, safe=False)



class GetSubPropertyCategory(View):
    def get(self, request):
        return JsonResponse([], safe=False)

    def post(self, request):
        try:
            property_category_id = request.POST.get('property_category_id')
            property_category = PropertyCategoryModel.objects.get(pk=property_category_id)
            children = SubPropertyCategory.objects.filter(property_category=property_category.pk).order_by('-priority')
            child_data = [{'id': child.pk, 'name': child.name} for child in children]
            return JsonResponse(child_data, safe=False)
        except:
            return JsonResponse([], safe=False)


class AvailableDatetime(View):
    def get(self, request):
        return JsonResponse({"msg": False})

    def post(self, request):
        time_24 = timezone.now() + timedelta(hours=24)

        meeting_time = request.POST.get('meeting_time')
        datetime_obj = datetime.strptime(meeting_time, '%Y-%m-%dT%H:%M')
        aware_datetime = timezone.make_aware(datetime_obj)
        aware_datetime_plus30 = timezone.make_aware(datetime_obj + timedelta(minutes=30))
        aware_datetime_minus30 = timezone.make_aware(datetime_obj - timedelta(minutes=30))

        objects_within_range1 = BookingModel.objects.filter(Q(meeting_time__gte=aware_datetime) & Q(meeting_time__lte=aware_datetime_plus30))
        objects_within_range2 = BookingModel.objects.filter(Q(meeting_time__lte=aware_datetime) & Q(meeting_time__gte=aware_datetime_minus30))
        

        if not aware_datetime > time_24:
            return JsonResponse({"msg": False, 'date_msg': 'Should be at least 24 hours from now'})

        if objects_within_range1 or objects_within_range2:
            return JsonResponse({"msg": False, 'date_msg': 'We have a meeting at the specified time'})

        return JsonResponse({"msg": True, 'date_msg': ''})


class About(View, Base):
    def get(self, request):
        employees = Employee.objects.all().order_by('-priority')
        employees_count = employees.count() + EMPLOYEES_COUNT
        project_count = ProjectModel.objects.count() + PROJECT_COUNT
        happy_customer_count = CustomerReview.objects.count() + HAPPY_CUSTOMER_COUNT
        partners = PartnerSlider.objects.all().order_by('-priority')
        partners_3_grid = [[]]
        index = 0
        for i in range(len(partners)):
            if i % 3 == 0 and i != 0:
                index += 1
                partners_3_grid.append([])
            partners_3_grid[index].append(partners[i])
        return render(request, 'main/about.html', {'employees': employees, 'employees_count': employees_count,
         'partners_3_grid': partners_3_grid, 'happy_customer_count': happy_customer_count, 
         'project_count': project_count, **self.context})


class Team(View, Base):
    def get(self, request):
        employees = Employee.objects.all().order_by('-priority')
        return render(request, 'main/team.html', {'employees': employees, **self.context})


class Projects(View, Base):
    def get(self, request):
        services = ServiceModel.objects.all().order_by('-priority')
        projects = ProjectModel.objects.all().order_by('-priority')
        return render(request, 'main/project.html', {'projects': projects, **self.context})


class ProjectDetail(View, Base):
    def get(self, request, slug):
        project = get_object_or_404(ProjectModel, slug=slug)
        return render(request, 'main/project-details.html', {'project': project, **self.context})


class Blogs(View, Base):
    def get(self, request):
        blogs = BlogModel.objects.all().order_by('-priority')
        show_blog = blogs[:3]
        return render(request, 'main/blog.html', {'blogs': blogs, 'show_blog': show_blog, **self.context})


class BlogDetail(View, Base):
    def get(self, request, slug):
        blog = get_object_or_404(BlogModel, slug=slug)
        blogs = BlogModel.objects.exclude(pk=blog.pk).order_by('-priority')
        return render(request, 'main/blog-details.html', {'blog': blog, 'blogs': blogs, **self.context})


# class Products(View, Base):
#     def get(self, request):
#         products = ProductModel.objects.all().order_by('-priority')
#         return render(request, 'main/product.html', {'products': products, **self.context})


# class ProductDetail(View, Base):
#     def get(self, request, slug):
#         product = get_object_or_404(ProductModel, slug=slug)
#         return render(request, 'main/product-details.html', {'product': product, **self.context})


class Service(View, Base):
    def get(self, request):
        services = ServiceModel.objects.all()
        return render(request, 'main/services.html', {**self.context})


class ServiceDetail(View, Base):
    def get(self, request, slug):
        service = get_object_or_404(ServiceModel, slug=slug)
        sub_services = SubService.objects.filter(service=service).order_by('-priority')
        return render(request, 'main/service-details.html', {'sub_services': sub_services, 'service': service, **self.context})


class Contact(View, Base):
    def get(self, request):
        form = ContactForm()
        return render(request, 'main/contact.html', {'form': form, **self.context})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message has been received')
            form = ContactForm()
            return render(request, 'main/contact.html', {"form": form, **self.context})

        messages.error(request, 'Invalid values filled try again', extra_tags='danger')
        return render(request, 'main/contact.html', {"form": form, **self.context})


class Booking(View, Base):
    def get(self, request):
        form = BookingForm()
        valid_options = service_valid_options(ServiceModel, SubService)
        return render(request, 'main/booking.html', {'form': form, "valid_options": valid_options, **self.context})

    def post(self, request):
        is_valid = True
        time_24 = timezone.now() + timedelta(hours=23, minutes=59)

        meeting_time = request.POST.get('meeting_time')
        datetime_obj = datetime.strptime(meeting_time, '%Y-%m-%dT%H:%M')
        aware_datetime = timezone.make_aware(datetime_obj)
        aware_datetime_plus30 = timezone.make_aware(datetime_obj + timedelta(minutes=29))
        aware_datetime_minus30 = timezone.make_aware(datetime_obj - timedelta(minutes=31))

        objects_within_range1 = BookingModel.objects.filter(Q(meeting_time__gte=aware_datetime) & Q(meeting_time__lte=aware_datetime_plus30))
        objects_within_range2 = BookingModel.objects.filter(Q(meeting_time__lte=aware_datetime) & Q(meeting_time__gte=aware_datetime_minus30))
        
        date_msg = ''

        if not aware_datetime > time_24:
            is_valid = False
            date_msg = 'Meeting should be at least 24 hours from now'

        if objects_within_range1 or objects_within_range1:
            is_valid = False
            date_msg = 'We have a meeting at the specified time'

        form = BookingForm(request.POST)
        valid_options = service_valid_options(ServiceModel, SubService)

        if is_valid and form.is_valid():
            form.save()
            messages.success(request, 'The meeting has been booked')
            form = BookingForm()
            return render(request, 'main/booking.html', {"form": form, "valid_options": valid_options, **self.context})

        messages.error(request, date_msg or 'Invalid values filled try again', extra_tags='danger')
        return render(request, 'main/booking.html', {"form": form, "valid_options": valid_options, **self.context})


class EmailSubscribe(View):
    def get(self, request):
        referring_url = request.META.get('HTTP_REFERER')
        return redirect(referring_url or reverse('main:index'))

    def post(self, request):
        referring_url = request.META.get('HTTP_REFERER')
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email subscribed to newsletter')
            return redirect(referring_url or reverse('main:index'))

        messages.error(request, 'Email address is invalid or already exists', extra_tags='danger')
        return redirect(referring_url or reverse('main:index'))

