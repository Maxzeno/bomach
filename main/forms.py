from django import forms
from .models import PropertyCategory, Quote, Service, SubPropertyCategory, SubService, ContactUs, Booking, Email, Property, JobApplication
from django_summernote.widgets import SummernoteWidget

# Experimental feature

PROPERTY_COORDINATE_NUM = 50

def dynamic_field(val):
    return forms.CharField(required=False, label='', max_length=250,  widget=forms.TextInput(
        attrs={'placeholder': '{val}', 'id': '{val}'}))


class SearchForm(forms.Form):
    query = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Search by name, ID and Location', 'id': 'query',
        }))


class PropertyForm(forms.ModelForm):
    name = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Name', 'id': 'name'
        }))
    phone = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Phone', 'id': 'phone'
        }))
    email = forms.EmailField(required=True, label='', max_length=500,  widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'id': 'email'
        }))
    content = forms.CharField(required=True, label='', max_length=10000,  widget=forms.Textarea(attrs={
        'placeholder': 'Description of the property and purpose eg rent, sell', 'id': 'content'
        }))

    property_title = forms.CharField(required=True, label='', max_length=1000, widget=forms.TextInput(attrs={
        'placeholder': 'Property Title', 'id': 'location'
        }))

    location = forms.CharField(required=True, label='', max_length=1000, widget=forms.TextInput(attrs={
        'placeholder': 'Property Location', 'id': 'location'
        }))
    
    images = forms.ImageField(required=True, label='', widget=forms.ClearableFileInput(attrs={
        'multiple': True, 'class': '', 'id': 'image-input'
    }))

    property_category = forms.ModelChoiceField(required=False, label='Categories', queryset=PropertyCategory.objects.all().order_by('-priority'),
     initial=PropertyCategory.objects.none(), empty_label='select category')

    sub_property_category = forms.ModelChoiceField(required=False, label='Sub Categories', 
        queryset=SubPropertyCategory.objects.all().order_by('-priority'), 
        initial=SubPropertyCategory.objects.none(), empty_label='select sub category')

    class Meta:
        model = Property
        fields = ['name', 'phone', 'content', 'email', 'location', 'property_title', 'sub_property_category']


# in production

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='', max_length=1000,  widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address', 'class': 'form-control', 'id': 'emailAddress'
        }))

    class Meta:
        model = Email
        fields = ['email']


class QuoteForm(forms.ModelForm):
    name = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Full Name', 'id': 'name'
        }))
    phone = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Phone', 'id': 'phone'
        }))
    email = forms.EmailField(required=True, label='', max_length=500,  widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'id': 'email'
        }))
    message = forms.CharField(required=True, label='', max_length=10000, widget=forms.Textarea(attrs={
        'placeholder': 'Message', 'id': 'message'
        }))

    phone = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Phone', 'id': 'phone'
        }))

    location = forms.CharField(required=True, label='', max_length=1000, widget=forms.TextInput(attrs={
        'placeholder': 'Location', 'id': 'location'
        }))

    service = forms.ModelChoiceField(required=True, label='Service', queryset=Service.objects.all().order_by('-priority'),
     initial=Service.objects.order_by('-priority').first())

    sub_service = forms.ModelChoiceField(required=False, label='Service', 
        queryset=SubService.objects.all().order_by('-priority'), 
        initial=SubService.objects.filter(
            service=Service.objects.order_by('-priority').first().pk).order_by('-priority').first()
        )
    
    class Meta:
        model = Quote
        fields = ['name', 'phone', 'email', 'service', 'sub_service', 'location', 'message']


class ContactForm(forms.ModelForm):
    name = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Full Name', 'id': 'name'
        }))
    phone = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Phone', 'id': 'phone'
        }))
    email = forms.EmailField(required=True, label='', max_length=500,  widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'id': 'email'
        }))
    message = forms.CharField(required=True, label='', max_length=10000, widget=forms.Textarea(attrs={
        'placeholder': 'Message', 'id': 'message'
        }))

    location = forms.CharField(required=True, label='', max_length=1000, widget=forms.TextInput(attrs={
        'placeholder': 'Location', 'id': 'location'
        }))

    class Meta:
        model = ContactUs
        fields = ['name', 'phone', 'email', 'location', 'message']


class BookingForm(forms.ModelForm):
    name = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Full Name', 'id': 'name'
        }))
    phone = forms.CharField(required=True, label='', max_length=500,  widget=forms.TextInput(attrs={
        'placeholder': 'Phone', 'id': 'phone'
        }))
    email = forms.EmailField(required=True, label='', max_length=500,  widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'id': 'email'
        }))
    message = forms.CharField(required=True, label='', max_length=10000, widget=forms.Textarea(attrs={
        'placeholder': 'Reason', 'id': 'message'
        }))

    location = forms.ChoiceField(choices=Booking.BRANCH_CHOICES, initial='Enugu Branch')

    service = forms.ModelChoiceField(required=True, label='Service', queryset=Service.objects.all().order_by('-priority'),
     initial=Service.objects.order_by('-priority').first())

    sub_service = forms.ModelChoiceField(required=False, label='Service', 
        queryset=SubService.objects.all().order_by('-priority'), 
        initial=SubService.objects.filter(
            service=Service.objects.order_by('-priority').first().pk).order_by('-priority').first()
        )
    
    meeting_time = forms.DateTimeField(required=True, label='', widget=forms.DateTimeInput(attrs={
        'placeholder': 'Meeting time', 'id': 'meeting_time', 'type': 'datetime-local'
        })) 

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'service', 'sub_service', 'location', 'message', 'meeting_time']


class JobApplicationForm(forms.ModelForm):
    name = forms.CharField(required=True, label='', max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'Full Name', 'id': 'name', 'class': 'form-control'
    }))
    email = forms.EmailField(required=True, label='', max_length=500, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address', 'id': 'email', 'class': 'form-control'
    }))
    phone = forms.CharField(required=True, label='', max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number', 'id': 'phone', 'class': 'form-control'
    }))
    resume = forms.FileField(required=True, label='Resume (PDF, DOC, DOCX)', widget=forms.FileInput(attrs={
        'id': 'resume', 'class': 'form-control', 'accept': '.pdf,.doc,.docx'
    }))
    cover_letter = forms.FileField(required=False, label='Cover Letter (PDF, DOC, DOCX) - Optional', widget=forms.FileInput(attrs={
        'id': 'cover_letter', 'class': 'form-control', 'accept': '.pdf,.doc,.docx'
    }))
    message = forms.CharField(required=False, label='Additional Message', max_length=5000, widget=forms.Textarea(attrs={
        'placeholder': 'Tell us why you\'re interested in this position...', 'id': 'message', 'class': 'form-control', 'rows': 5
    }))

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume', 'cover_letter', 'message']

