from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import math
import uuid


FROM_EMAIL = 'khairnaryogesh259@gmail.com'
EMAIL_PASSWORD = 'lwcd rxpf pmsk hmzo'
def send_email_to_support(tomail , otp):
	try:
		subject = f"document editor Login OTP"
		msg_body = f'Your Login OTP is {otp}\n please Do not share anyone'
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From']    = FROM_EMAIL
		msg['To']      = tomail
		msg.attach(MIMEText(msg_body, 'html'))
		'''Connect smtp server'''
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(FROM_EMAIL , EMAIL_PASSWORD)
		server.sendmail(FROM_EMAIL, tomail, msg.as_string())
		return True
	except Exception as exp:
		return False
	

globle_otp_dict = {}
session_stored_uuid = {}

@csrf_exempt
def gentotp(request):
	global globle_otp_dict
	if request.method == "POST":
		email = request.POST.get("email")
		print(email,'-------------email')
		otp = str(random.randint(100000, 999999))
		globle_otp_dict[email] = otp
		print('--------OTP',otp)
		# send_email_to_support(email ,OTP)
		return JsonResponse({"status": "sent"})
	return JsonResponse({"status": "fail"})


@csrf_exempt
def login(request):
	global globle_otp_dict , session_stored_uuid
	if request.method == "POST":
		email = request.POST.get("email")
		otp = request.POST.get("otp")
		print(f"email : {email} otp : {otp}")
		# Validate OTP
		if str(otp) == str(globle_otp_dict[email]):  # Replace with real check
			new_uuid = uuid.uuid4()
			session_stored_uuid[str(new_uuid)] = email
			return JsonResponse({"status": "success","uuid":new_uuid})
		else:
			return JsonResponse({"status": "fail"})
	return JsonResponse({"status": "get request not allow"})
def loginpage(request):
	return render(request, 'login_page.html',{})


def homepage(request,uuid):
	print(f'uuid {uuid}')
	global session_stored_uuid
	print(session_stored_uuid, "session_stored_uuid")
	if uuid in session_stored_uuid:
		print(session_stored_uuid[uuid],"session_stored_uuid['User']")
		return render(request, 'homepage.html',{'User':session_stored_uuid[uuid]})
	return redirect("loginpage")


# @csrf_exempt
def ai_suggestion_view(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		text = data.get('text', '')
		response = requests.post("https://api.languagetoolplus.com/v2/check", data={'text': text,'language': 'en-US'})
		# print(response.json(), '---------------------')
		return JsonResponse(response.json(), safe=False)
