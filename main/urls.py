from django.urls import path
from django.views.generic.base import TemplateView
from .import views

app_name = 'main'

urlpatterns = [
    # experimental feature
    path('property', views.Property.as_view(), name='property'),
    path('property/create', views.PropertyCreate.as_view(), name='property-create'),
    path('property/<slug:slug>', views.PropertyDetail.as_view(), name='property-details'),
    # in production
    path('', views.Index.as_view(), name='home'),
    path('index', views.Index.as_view(), name='index'),
    path('about', views.About.as_view(), name='about'),
    path('services', views.Service.as_view(), name='services'),
    path('email-subscribe', views.EmailSubscribe.as_view(), name='email-subscribe'),
    path('services/<slug:slug>', views.ServiceDetail.as_view(), name='service-details'),
    path('get-sub-service', views.GetSubService.as_view(), name='get-sub-service'),
    path('get-sub-property-category', views.GetSubPropertyCategory.as_view(), name='get-sub-property-category'),
    path('available-datetime', views.AvailableDatetime.as_view(), name='available-datetime'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('booking', views.Booking.as_view(), name='booking'),
    path('team', views.Team.as_view(), name='team'),
    # path('product', views.Products.as_view(), name='product'),
    # path('product/<slug:slug>', views.ProductDetail.as_view(), name='product-details'),
    path('blog', views.Blogs.as_view(), name='blog'),
    path('blog/<slug:slug>', views.BlogDetail.as_view(), name='blog-details'),
    path('project', views.Projects.as_view(), name='project'),
    path('project/<slug:slug>', views.ProjectDetail.as_view(), name='project-details'),

]
