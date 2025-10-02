from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.utils.crypto import get_random_string
from pyproj import Proj
import requests
from django.conf import settings

# Create your models here.

# notes Lat/long can be in: deg/min/sec  or  decimal degrees
# UTM can be in:  m  or  mm

def convert_easting_northing_to_lon_lat(easting, northing, zone=32):
    # Define the projection system for Nigeria
    nigeria_proj = Proj(proj='utm', zone=zone, ellps='WGS84', south=False)
    
    # Convert Easting/Northing to Longitude/Latitude
    lon, lat = nigeria_proj(easting, northing, inverse=True)
    return lon, lat


def convert_decimal_to_dms(decimal, flag=''):
	if flag:
		flag = f" {flag}"
	degrees = int(decimal)
	decimal_minutes = abs(decimal - degrees) * 60
	minutes = int(decimal_minutes)
	seconds = (decimal_minutes - minutes) * 60
	return f"{degrees}° {minutes}' {seconds}\"{flag}"


def unique_id(model, col='id', length=6):
	val = {}
	while True:
		random = get_random_string(length=length)
		val[col] = random
		if not model.objects.filter(**val).exists():
			break
	return random


def service_valid_options(service_model, sub_service_model):
	try:
		service_pk = service_model.objects.order_by('-priority').first().pk
		sub_services = sub_service_model.objects.filter(service=service_pk).order_by('-priority')
		return [ sub_service.name for sub_service in sub_services ]
	except:
		return []

def property_category_valid_options(property_category_model, sub_property_category_model):
	try:
		property_category_pk = property_category_model.objects.order_by('-priority').first().pk
		sub_property_categorys = sub_property_category_model.objects.filter(property_category=property_category_pk).order_by('-priority')
		return [ sub_property_category.name for sub_property_category in sub_property_categorys ]
	except:
		return []
	

def send_email_property(email, property_model):
	if not isinstance(email, list):
		email = [email]
	subject = 'User adds a property for review'
	message = f"""Name: {property_model.name}
Phone number: {property_model.phone}
Email: {property_model.email}
Location: {property_model.location}
Content: {property_model.short_content()}
"""
	send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False)


def send_email_quote(email, quote_model):
	if not isinstance(email, list):
		email = [email]
	subject = 'New User wants Project Estimate'
	message = f"""Name: {quote_model.name}
Phone number: {quote_model.phone}
Email: {quote_model.email}
Location: {quote_model.location}
Service: {quote_model.service.name}
Sub Service: {quote_model.sub_service.name if quote_model.sub_service else ''}
Message: {quote_model.message}
"""
	send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False)


def send_email_contact(email, contact_model):
	if not isinstance(email, list):
		email = [email]
	subject = 'User Contacts admin'
	message = f"""Name: {contact_model.name}
Phone number: {contact_model.phone}
Email: {contact_model.email}
Location: {contact_model.location}
Message: {contact_model.message}
"""
	send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False)


def send_booking_email(email, booking_model):
	if not isinstance(email, list):
		email = [email]
	subject = 'New User booked an appointment with us'
	message = f"""Name: {booking_model.name}
Phone number: {booking_model.phone}
Email: {booking_model.email}
Location: {booking_model.location}
Service: {booking_model.service.name}
Sub Service: {booking_model.sub_service.name if booking_model.sub_service else ''}
Message: {booking_model.message}
Meeting time: {booking_model.meeting_time.strftime("%A %d %B %Y by %I:%M%p")}
Duration in minutes: {booking_model.duration_in_minutes}
"""
	send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False)


def send_user_booking_email(email, booking_model):
	if not isinstance(email, list):
		email = [email]
	subject = 'Your Appointment has been booked'
	message = f"""Your Appointment is on {booking_model.meeting_time.strftime("%A %d %B %Y by %I:%M%p")}
Best regards Bomach Group.
"""
	send_mail(subject, message, settings.EMAIL_HOST_USER, email, fail_silently=False)


def verify_google_recaptcha(recaptcha_token):
	data = {
		'secret': settings.RECAPTCHA_SECRET_KEY,
		'response': recaptcha_token
	}

	verify_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
	result = verify_response.json()
	print(result)
	# Step 2: Check success and score
	if not result.get('success') or result.get('score', 0) < 0.80:
		return False
	return True


def send_sms_service(recipients, message):
    username = settings.USERNAME_80KOBO
    password = settings.PASSWORD_80KOBO
    sender_name_10_characters_long = "Bomach"
    recipients_str = ''
    for recipient in recipients:
        if recipient != None:
            recipients_str += f'{recipient},'
    
    if not recipients_str:
        return None

    params = {
        "email":username,
        "password":password,
        "message":message,
        "sender_name":sender_name_10_characters_long,
        "recipients":recipients_str,
        "forcednd":1,
    }
    url= f"https://api.80kobosms.com/v2/app/sms" 

    response = requests.get(url, params=params)
    return response.json()
