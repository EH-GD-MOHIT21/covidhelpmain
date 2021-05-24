from django.http import request
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import userpersonal, User
from django.contrib.auth import authenticate, login as Login, logout
import smtplib
from email.message import EmailMessage
from random import choice
from datetime import datetime, timezone
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
# Create your views here.


class staticviews:
    faltu_items = ['!', '#', '$', '%', '^', '&', '*',
                   '(', ')', '{', '}', '[', ']', ';', ':', "'", '"', '<', '>', ',', '?', '/', '|', '`', '~', '+']

    def user_verify(self, username=None):
        # write user verification code here
        if username == None:
            return False
        if len(User.objects.filter(username=username)):
            return False
        if len(username) < 3:
            return False
        for word in username:
            if word in self.faltu_items:
                return False
        return True

    def verify_pass_cpass(self, pass1=None, pass2=None):
        # write pass verification here
        if pass1 != pass2:
            return False
        if len(pass1) <= 7:
            return False
        if pass1.isalnum() or pass1.isalpha() or pass1.isdigit():
            return False
        return True

    def verify_mail(self, email):
        # mail verification here
        try:
            a = email.split('@')
            if len(a) != 2 or email[-1] == '@' or email[-2] == '@' or email[0] == '@' or email[1] == '@':
                return False
            b = email.split('.')
            if len(b) > 3 or email[-1] == '.' or email[-2] == '.' or email[0] == '.' or email[1] == '.':
                return False
        except:
            return False

        return True

    def verify_mobile(self, phone=None):
        # phone verification here
        if '+91' in phone and len(phone) != 13:
            return False
        if len(phone) != 10:
            return False
        if not phone.isnumeric():
            return False
        return True

    def generate_random_unicode(self):
        # logic to generate code
        varsptoken = ''
        alphas = ['-', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(26):
            alphas.append(chr(65+i))
            alphas.append(chr(97+i))
        for i in range(89):
            varsptoken += choice(alphas)

        return varsptoken

    def send_mail(self, to, personalcode):
        # logic to send mail to user
        sender_mail = "no.reply.python.py@gmail.com"
        password_sender = "qwerty@123"
        message = EmailMessage()
        message['To'] = to
        message['From'] = sender_mail
        message['Subject'] = "Welcome User to CovidHelper.com"
        message.set_content(
            f"Hello User welcome to CovidHelper.com Your one time login link is\n https://help4covid.herokuapp.com/verify/{personalcode} \nvalid for next 15 minutes.. Thanks For support 🙏🙏\n Regards\n CovidHelper.com")
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_mail, password_sender)
            server.send_message(message)
            return True         # success
        except:
            return False        # failure


def user(request):
    if not request.user.is_authenticated:
        messages.info(request,'Welcome User to covidhelper.com')
        return render(request, 'login.html')
    else:
        return redirect('/')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        cpass = request.POST['repassword']
        email = request.POST['email']
        mobile = request.POST['mobile']

        myview = staticviews()
        # username verification
        if myview.user_verify(username):
            # print('ok')
            pass
        else:
            # print('no ok')
            messages.error(request,'Invalid Username.')
            return render(request, 'login.html')

        # mail id verification
        if myview.verify_mail(email):
            # print('ok')
            pass
        else:
            # print('no ok')
            messages.error(request,'Invalid Mail id.')
            return render(request, 'login.html')

        # password verification
        if myview.verify_pass_cpass(passwd, cpass):
            # print('ok')
            pass
        else:
            # print('no ok')
            messages.error(request,'Something wrong in Password Field.')
            return render(request, 'login.html')

        # mobile verification
        if myview.verify_mobile(mobile):
            # print('ok')
            pass
        else:
            # print('no ok')
            messages.error(request,'Invalid Phone Number.')
            return render(request, 'login.html')
        personalcode = myview.generate_random_unicode()
        mytimecalculator = 0
        while(len(userpersonal.objects.filter(unicode=personalcode))):
            personalcode = myview.generate_random_unicode()
            mytimecalculator += 1
            if mytimecalculator > 10000:
                # render(request,'logshower.html',{'formid': 'sorry but we are unable to process your request'})
                pass

        status = myview.send_mail(email, personalcode)

        user = User.objects.create_user(
            username=username, password=passwd, email=email)
        user.save()
        upes = userpersonal(user=user, phoneno=mobile, email=email,
                            unicode=personalcode, timestamp=datetime.now(timezone.utc))
        upes.save()
        return render(request, 'login.html')
    else:
        return redirect('/signup')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request,'Invalid Credentials...')
            return render(request, 'login.html')
        else:
            print('success')
            Login(request, user=user)
            messages.success(request,'Successfully logged in.')
            return render(request, 'form.html')
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        messages.info(request,'Please Login with your credentials...')
        return redirect('/signup')


@csrf_exempt
def verify(request, pid):
    return render(request, 'userverify.html', {'pid': pid})


@csrf_exempt
def updateuser(request, pid):
    if request.method == 'POST':
        phoneno = request.POST['phone']
        username = request.POST['username']
        me = userpersonal.objects.filter(unicode=pid, phoneno=phoneno)
        puser = User.objects.filter(username=username)
        if len(me) != 1 or len(puser) != 1:
            return HttpResponse({'user not exists'})
        for person in me:
            if person.verified == 0:
                # match timestamp code here
                cur_time = datetime.now(timezone.utc)
                pre_time = person.timestamp
                del_time = str(cur_time-pre_time)
                del_time = del_time.split(':')
                if del_time[0] != '0':
                    # delete entry from database
                    userpersonal.objects.filter(
                        unicode=pid, phoneno=phoneno).delete()
                    User.objects.filter(username=username).delete()
                    return HttpResponse({'Time Limit Exceed'})
                elif int(del_time[1]) > 14:     # 15 minutes time
                    # delete entry from database
                    userpersonal.objects.filter(
                        unicode=pid, phoneno=phoneno).delete()
                    User.objects.filter(username=username).delete()
                    return HttpResponse({'Time limit Excced'})
                person.verified = 1
                person.unicode = None
                person.save()
                return HttpResponse({'success'})
            else:
                return HttpResponse({'Already Verified.'})
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return HttpResponse({'user is not authenticated.'})


def logmeoutplease(request):
    logout(request)
    return redirect('/')


############################################################################################################################################

################################################                Axios Handler               ################################################

############################################################################################################################################


@csrf_exempt
def validate(request):
    if request.method == 'POST':
        uname = json.loads(request.body).get('uname')
        if len(User.objects.filter(username=uname)):
            return JsonResponse({"message": "username not available."})
        if len(uname) < 3 or len(uname) == 0:
            return JsonResponse({"message": "username min length should be 3."})
        if ' ' in uname:
            return JsonResponse({'message': 'username can not contain space'})
        if "'" in uname:
            return JsonResponse({'message': "username can not contain ' "})
        if '"' in uname:
            return JsonResponse({'message': 'username cannot contain " '})
        if "(" in uname or ")" in uname or "{" in uname or "}" in uname or "[" in uname or "]" in uname or "|" in uname or "/" in uname or "?" in uname or ">" in uname or "<" in uname or "," in uname or ":" in uname or ";" in uname or "=" in uname or "`" in uname:
            return JsonResponse({'message': 'username can contain @!&^%$#*'})

        if len(uname) > 15:
            return JsonResponse({'message': 'usernamelength should less than 15'})
        # databse connectivity here.

        return JsonResponse({"message": "success"})
    else:
        return redirect('/')


@csrf_exempt
def validate_pass(request):
    if request.method == 'POST':
        password = json.loads(request.body).get('password')
        if len(password) < 8 or len(password) == 0:
            return JsonResponse({'message': 'password should be atleast 8 characters.'})

        if len(password) > 25:
            return JsonResponse({'message': 'password should be max 25 characters.'})

        if password.isalpha() or password.isnumeric() or password.isalnum():
            return JsonResponse({'message': 'please use digits,special characters,alphabets'})

        return JsonResponse({'message': 'success'})
    else:
        return redirect('/')


@csrf_exempt
def validate_cpass(request):
    if request.method == 'POST':
        passw1 = json.loads(request.body).get('cpass')
        passw2 = json.loads(request.body).get('pass')

        if len(passw2) < 8:
            return JsonResponse({'message': 'Please make your password 8 characters long.'})

        if passw1 == passw2:
            return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'both password should be same.'})
    else:
        return redirect('/')


@csrf_exempt
def verify_mail(request):
    # mail sender code here
    if request.method == 'POST':
        mailid = json.loads(request.body).get('email')
        if not len(mailid):
            return JsonResponse({'message': 'mail id can not be blank.'})
        if mailid.count('.') == 0 or mailid.count('@') != 1 or '.@' in mailid or '@.' in mailid or '..' in mailid:
            return JsonResponse({'message': 'mail id not valid.'})
        if mailid.count('.') == 1 and mailid.index('@') - mailid.index('.') > 0 or not mailid[-1].isalpha():
            return JsonResponse({'message': 'mail id not valid.'})
        waste = "!#$%^&*()}{[];':?/`~,<>"
        for i in waste:
            if i in mailid:
                return JsonResponse({"message": "mail id not correct."})

        if len(User.objects.filter(email=mailid)):
            return JsonResponse({'message': 'This mail is already registerd.'})

        return JsonResponse({'message': 'success'})

    else:
        return redirect('/')


@csrf_exempt
def verify_phone(request):
    if request.method == 'POST':
        phone = json.loads(request.body).get('phone')
        if '+91' in phone:
            return JsonResponse({'message': 'please remove +91.'})
        if not phone.isnumeric():
            return JsonResponse({'message': 'phone number should be digits.'})
        if len(phone) != 10:
            return JsonResponse({'message': 'phone number should be length 10.'})
        if len(userpersonal.objects.filter(phoneno=phone)):
            return JsonResponse({'message': 'phone number already exists.'})
        return JsonResponse({'message': 'success'})
    else:
        return redirect('/')
