from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.utils.crypto import get_random_string

# Create your models here.


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

