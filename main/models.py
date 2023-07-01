from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django_summernote.fields import SummernoteTextField
import bleach
from .utils import (
    send_email_quote, send_email_contact, send_booking_email, send_user_booking_email, unique_id)

# Create your models here.

STAFF_EMAILS = ['benantoto@gmail.com', 'contact@bomachgroup.com', 'bomachgroupmanagement@gmail.com']

class ImageUrl:
    def image_url(self):
        if self.image:
            return self.image.url

        # this has the potential to fail when i use cloudinary to host static files
        return '/static/assets/img/logo/bomach-logo-hd.jpeg'


class CustomBaseModel:
    def short_content(self):
        if self.content:
            rich_text = self.content.replace('&nbsp;', '')
            text = bleach.clean(rich_text, tags=[], strip=True)
            cleaned_string = ' '.join(list(text.split()))
            return f"{cleaned_string[:50]}.."
        return ''

    def save(self, *args, **kwargs):
        self.content = self.content.replace('&lt;o:p&gt;&lt;/o:p&gt;', '')
        super().save(*args, **kwargs)


class Service(CustomBaseModel, models.Model, ImageUrl):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to='images/')
    content = SummernoteTextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0, message='Value cannot be less than 0.'),
            MaxValueValidator(100, message='Value cannot be greater than 100.')
        ],
        default=80) # ranting over 100%
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class SubService(CustomBaseModel, models.Model, ImageUrl):
    name = models.CharField(max_length=250, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    slug = models.CharField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to='images/')
    content = SummernoteTextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0, message='Value cannot be less than 0.'),
            MaxValueValidator(100, message='Value cannot be greater than 100.')
        ],
        default=80) # ranting over 100%
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Project(CustomBaseModel, models.Model, ImageUrl):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, unique=True, blank=True)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    content = SummernoteTextField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ProductImage(models.Model, ImageUrl):
    name = models.CharField(max_length=250, default='N/A')
    priority = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    date = models.DateTimeField(default=timezone.now)


def product_id():
    return unique_id(Product)

class Product(CustomBaseModel, models.Model):
    id = models.CharField(primary_key=True, max_length=6, default=product_id)
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True, blank=True)
    content = SummernoteTextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    video = models.URLField(max_length=500, null=True)
    product_images = models.ManyToManyField(ProductImage)
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def video_url(self):
        if self.video:
            return (
                f"https://www.youtube.com/embed/{self.video.split('/')[-1].split('v=')[-1].split('&')[0].split('?')[0]}?rel=0"
            )
        return ''

    def image_url(self):
        """
            Gets the first product image NOTE they can be more that one product image
        """
        product_image = self.product_images.order_by('-priority').first()
        if product_image:
            return product_image.image_url()
        return '/static/assets/img/logo/bomach-logo-full.jpeg'

    def __str__(self):
        return self.name


class Blog(CustomBaseModel, models.Model, ImageUrl):
    title = models.CharField(max_length=250, null=True, blank=True)
    author = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    content = SummernoteTextField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class HomeSlider(models.Model, ImageUrl):
    # title = models.CharField(max_length=500)
    big_text = models.CharField(max_length=500)
    small_text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.big_text


class CustomerReview(models.Model):
    name = models.CharField(max_length=250)
    review = models.CharField(max_length=2000)
    occupation = models.CharField(max_length=500)
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Employee(models.Model, ImageUrl):
    name = models.CharField(max_length=250)
    job_title = models.CharField(max_length=250)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class PartnerSlider(models.Model, ImageUrl):
    company = models.CharField(max_length=250, default="N/A")
    image = models.ImageField(upload_to='images/')
    priority = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company


class Quote(models.Model):
    name = models.CharField(max_length=250, default="N/A")
    phone = models.CharField(max_length=250, default="N/A")
    email = models.CharField(max_length=250, default="N/A")
    message = models.CharField(max_length=10000, default="N/A")
    location = models.CharField(max_length=1000, default="N/A")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service Quote' 
        verbose_name_plural = 'Service Quote'


class ContactUs(models.Model):
    name = models.CharField(max_length=250, default="N/A")
    phone = models.CharField(max_length=250, default="N/A")
    email = models.CharField(max_length=250, default="N/A")
    message = models.CharField(max_length=10000, default="N/A")
    location = models.CharField(max_length=1000, default="N/A")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact us' 
        verbose_name_plural = 'Contact us'


class Booking(models.Model):
    BRANCH_CHOICES = [
        ('Enugu Branch', 'Enugu Branch'),
        ('Port Harcourt Branch', 'Port Harcourt Branch'),
    ]
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message = models.CharField(max_length=10000)
    location = models.CharField(max_length=1000, choices=BRANCH_CHOICES, default='Enugu Branch')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE, blank=True, null=True)
    meeting_time = models.DateTimeField()
    duration_in_minutes = models.IntegerField(default=30)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Booking' 
        verbose_name_plural = 'Booking'


class Email(models.Model):
    email = models.EmailField(unique=True, null=False)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Email Subscriber' 
        verbose_name_plural = 'Email Subscribers'
    


# django signal
def create_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)

def create_slug_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)

def send_quote_email_signal(sender, instance, *args, **kwargs):
    send_email_quote(STAFF_EMAILS, instance)

def send_contact_email_signal(sender, instance, *args, **kwargs):
    send_email_contact(STAFF_EMAILS, instance)

def send_booking_email_signal(sender, instance, *args, **kwargs):
    send_booking_email(STAFF_EMAILS, instance)

def send_user_booking_email_signal(sender, instance, *args, **kwargs):
    send_user_booking_email(instance.email, instance)


pre_save.connect(create_slug, sender=Service)
pre_save.connect(create_slug, sender=SubService)
pre_save.connect(create_slug, sender=Project) # note this is proJEct
pre_save.connect(create_slug, sender=Product) # and this is proDUct
pre_save.connect(create_slug_title, sender=Blog)

post_save.connect(send_booking_email_signal, sender=Booking)
post_save.connect(send_user_booking_email_signal, sender=Booking)
post_save.connect(send_quote_email_signal, sender=Quote)
post_save.connect(send_contact_email_signal, sender=ContactUs)


# <o:p></o:p>
# <o:p></o:p>