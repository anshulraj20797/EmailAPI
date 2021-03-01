from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from boto3.session import Session
import os

@csrf_exempt
def email(request):
     to = request.POST.get('to')
     recipients = list([to])
     sender = request.POST.get('sender')
     subject = request.POST.get('subject')
     body = request.POST.get('body')
     file_name = request.POST.get('file_name')
     #session for using bucket       
     session = Session(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
     s3 = session.resource('s3')
     bucket = settings.AWS_STORAGE_BUCKET_NAME
     my_bucket = s3.Bucket(bucket)
     my_bucket.download_file(file_name,file_name)
     #sending email
     msg = EmailMessage(subject,body,sender,recipients)
     msg.content_subtype = "html"  
     location = os.path.abspath("./") #generting current path
     msg.attach_file(location+'\\'+file_name)
     msg.send()
     response = JsonResponse({ 'recipients': recipients,'sender': sender,'subject': subject, 'body': body, 'file_name': file_name})
     return response
 