from django.http import HttpResponse
from django.conf import settings
from django.utils.crypto import get_random_string
from pyproj import Proj
import requests
from django.conf import settings
import re
import json
from django.conf import settings
from django.template.loader import render_to_string


def _chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def send_email_service(
    recipients: list,
    title: str = "Bomach",
    path: str = "main/email_template/custom.html",
    context_data: dict = {},
):
	# Normalize recipients to list if single string
	if isinstance(recipients, str):
		recipients = [recipients]

	# Convert string emails to dict format
	normalized_recipients = []
	for recipient in recipients:
		if isinstance(recipient, str):
			normalized_recipients.append({"email": recipient, "name": ""})
		else:
			normalized_recipients.append(recipient)

	# Render HTML content from template
	html_content = render_to_string(path, context_data)

	from_email: str = "noreply@bomachgroup.com"
	url = "https://api.zeptomail.com/v1.1/email"
	headers = {
		"accept": "application/json",
		"content-type": "application/json",
		"authorization": settings.ZOHOZEPTOMAIL_KEY,
	}

	responses = []
	# Process recipients in batches of 100 (ZeptoMail limit)
	for chunk in _chunk_list(normalized_recipients, 100):
		to_recipients = []
		for recipient in chunk:
			if recipient and recipient.get("email"):
				to_recipients.append({
					"email_address": {
						"address": recipient.get("email"),
						"name": recipient.get("name", ""),
					}
				})

		if not to_recipients:
			continue

		payload = {
			"from": {"address": from_email},
			"to": to_recipients,
			"subject": title,
			"htmlbody": html_content,
		}

		try:
			response = requests.post(
				url, data=json.dumps(payload), headers=headers, timeout=10
			)
			responses.append(response)
		except Exception as e:
			print(f"Error sending email via ZeptoMail: {str(e)}")
			responses.append(None)

	return responses  # returns a list of responses (one per batch)


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
	"""Send property submission notification to staff via send_email_service."""
	subject = 'User adds a property for review'
	context_data = {
		'header': 'New Property Submission',
		'title': subject,
		'sub_title': f"""<strong>Name:</strong> {property_model.name}<br/>
<strong>Phone:</strong> {property_model.phone}<br/>
<strong>Email:</strong> {property_model.email}<br/>
<strong>Location:</strong> {property_model.location}<br/>
<strong>Content:</strong> {property_model.short_content()}"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


def send_email_quote(email, quote_model):
	"""Send quote request notification to staff via send_email_service."""
	subject = 'New User wants Project Estimate'
	context_data = {
		'header': 'New Quote Request',
		'title': subject,
		'sub_title': f"""<strong>Name:</strong> {quote_model.name}<br/>
<strong>Phone:</strong> {quote_model.phone}<br/>
<strong>Email:</strong> {quote_model.email}<br/>
<strong>Location:</strong> {quote_model.location}<br/>
<strong>Service:</strong> {quote_model.service.name}<br/>
<strong>Sub Service:</strong> {quote_model.sub_service.name if quote_model.sub_service else 'N/A'}<br/>
<strong>Message:</strong> {quote_model.message}"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


def send_email_contact(email, contact_model):
	"""Send contact form notification to staff via send_email_service."""
	subject = 'User Contacts admin'
	context_data = {
		'header': 'New Contact Form Submission',
		'title': subject,
		'sub_title': f"""<strong>Name:</strong> {contact_model.name}<br/>
<strong>Phone:</strong> {contact_model.phone}<br/>
<strong>Email:</strong> {contact_model.email}<br/>
<strong>Location:</strong> {contact_model.location}<br/>
<strong>Message:</strong> {contact_model.message}"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


def send_booking_email(email, booking_model):
	"""Send booking notification to staff via send_email_service."""
	subject = 'New User booked an appointment with us'
	context_data = {
		'header': 'New Booking',
		'title': subject,
		'sub_title': f"""<strong>Name:</strong> {booking_model.name}<br/>
<strong>Phone:</strong> {booking_model.phone}<br/>
<strong>Email:</strong> {booking_model.email}<br/>
<strong>Location:</strong> {booking_model.location}<br/>
<strong>Service:</strong> {booking_model.service.name}<br/>
<strong>Sub Service:</strong> {booking_model.sub_service.name if booking_model.sub_service else 'N/A'}<br/>
<strong>Message:</strong> {booking_model.message}<br/>
<strong>Meeting time:</strong> {booking_model.meeting_time.strftime("%A %d %B %Y by %I:%M%p")}<br/>
<strong>Duration:</strong> {booking_model.duration_in_minutes} minutes"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


def send_user_booking_email(email, booking_model):
	"""Send booking confirmation to user via send_email_service."""
	subject = 'Your Appointment has been booked'
	context_data = {
		'header': 'Booking Confirmation',
		'title': subject,
		'sub_title': f"""Your appointment has been successfully booked for:<br/><br/>
<strong>{booking_model.meeting_time.strftime("%A, %d %B %Y at %I:%M %p")}</strong><br/><br/>
Thank you for choosing Bomach Group. We look forward to meeting you!"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


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
	sendchamp_token = settings.SENDCHAMP_TOKEN

	url = "https://api.sendchamp.com/api/v1/sms/send"

	payload = {
		"to": recipients,
		"message": message,
		"sender_name": "SC-OTP",
		"route": "dnd"
	}

	headers = {
		"Accept": "application/json",
		"Authorization": f"Bearer {sendchamp_token}",
		"Content-Type": "application/json"
	}

	response = requests.post(url, headers=headers, json=payload)

	return response.json()


def normalize_nigerian_number(raw_number: str) -> str:
    # Remove spaces, dashes, brackets, and leading +
    number = re.sub(r"[^\d]", "", raw_number)

    if number.startswith("234") and len(number) == 13:
        # Already in correct format
        return number
    elif number.startswith("0") and len(number) == 11:
        # Replace leading 0 with 234
        return "234" + number[1:]
    elif len(number) == 10:
        # Missing leading 0 → assume local number
        return "234" + number
    else:
        return None


def send_job_application_email(email, job_application_model):
	"""Send job application notification to staff via send_email_service."""
	subject = 'New Job Application Received'
	context_data = {
		'header': 'New Job Application',
		'title': subject,
		'sub_title': f"""<strong>Name:</strong> {job_application_model.name}<br/>
<strong>Phone:</strong> {job_application_model.phone}<br/>
<strong>Email:</strong> {job_application_model.email}<br/>
<strong>Job Title:</strong> {job_application_model.job.title}<br/>
<strong>Applied at:</strong> {job_application_model.applied_at.strftime("%A %d %B %Y by %I:%M%p")}<br/>
<strong>Message:</strong> {job_application_model.message if job_application_model.message else 'N/A'}<br/>"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)


def send_user_job_application_email(email, job_application_model):
	"""Send job application confirmation to user via send_email_service."""
	subject = 'Application Received - Bomach Group'
	context_data = {
		'header': 'Application Received',
		'title': subject,
		'sub_title': f"""Dear {job_application_model.name},<br/><br/>
Thank you for applying for the <strong>{job_application_model.job.title}</strong> position at Bomach Group. We have received your application and will review it carefully.<br/><br/>
We will get back to you soon with updates regarding your application.<br/><br/>
Best regards,<br/>
<strong>Bomach Group</strong>"""
	}
	send_email_service(
		recipients=email,
		title=subject,
		path='main/email_template/custom.html',
		context_data=context_data
	)
