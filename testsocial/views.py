from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout,settings
from django.contrib.auth.models import User
from simplejson import dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from twilio import twiml
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
from twilio.rest import TwilioRestClient 

# Create your views here.

def hello(request):
    print 'hi'
    return render(request,'home.html')

def home(request):
    args={}
    args['username']=request.user
    contact_list = User.objects.all().values('username')
    paginator = Paginator(contact_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    args['contacts']=contacts
    return render(request,'login.html',args)

def logout(request):
    #request.session.flush()
    #response = logout(request)
    del request.COOKIES
    #response.delete_cookie('user_location')
    return HttpResponse("You're logged out.")

def users(request):
    search = request.GET.get('term','')
    userslist=[]
    print search
    print 'search'
    users=User.objects.filter(username__icontains=search).values('username')
    print users
    for i in users:
        userslist.append(str(i["username"]))

    return HttpResponse(dumps(userslist), content_type = 'application/javascript; charset=utf8')

@twilio_view
def reply_to_sms_messages(request):
    r = twiml.Response()
    r.message('Thanks for the SMS message!')
    return r

@twilio_view
def inbound_view(request):

    response = twiml.Response()

    # Create a new TwilioRequest object
    twilio_request = decompose(request)

    # See the Twilio attributes on the class
    twilio_request.to
    # >>> '+44123456789'

    # Discover the type of request
    if twilio_request.type is 'message':
        response.message('Thanks for the message!')
        return response

    # Handle different types of requests in a single view
    if twilio_request.type is 'voice':
        return voice_view(request)

    return response

@twilio_view
def gather_digits(request):
 
    twilio_response = Response()
 
    with twilio_response.gather(action='/respond/', numDigits=2) as g:
        g.say('Press one to hear a song, two to receive an SMS')
        g.pause(length=1)
        g.say('Press one to hear a song, two to receive an SMS')
        """
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to="+917205771877", 
            from_="+18329813555", 
            body="thanks for showing interest",  
        )
        """
 
    return twilio_response

@twilio_view
def handle_response(request):
 
    digits = request.POST.get('Digits', '')
    print 'sjkdhfkjsdfjksdf'
    print request.POST
    twilio_response = Response()
 
    if digits == '1':
        twilio_response.play('http://bit.ly/phaltsw')
 
    if digits == '2':
        number = request.POST.get('From', '')
        twilio_response.say('A text message is on its way')
        twilio_response.sms('You looking lovely today!', to=number)
        
 
    return twilio_response


@twilio_view
def callnumber(request):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to="+919440247341", 
        from_="+18329813555", 
        url="http://127.0.0.1:8000/gather/",  
        method="GET",  
        fallback_method="GET",  
        status_callback_method="GET",    
        record="false"
    ) 
    return HttpResponse("You're using twillio.")

def hello_monkey():
    """Respond to incoming requests."""
    resp = twiml.Response()
    resp.say("Hello Monkey")
 
    return str(resp)