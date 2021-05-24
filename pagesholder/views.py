from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from userhandler.models import User,userpersonal
from .models import publicaccessdata as pad
from django.contrib import messages
# Create your views here.

def helpform(request):                  # check verified=1 for user
    if request.user.is_authenticated:
        return render(request,'form.html')
    else:
        return redirect('/login')

def home(request):
    return render(request,'home.html')

@csrf_exempt
def findnreg(request):
    if request.method == 'POST' and request.user.is_authenticated:      #write logic to check verified = 1 for user
        firstname = request.POST['fst_name']
        lastname = request.POST['lst_name']
        firstno = request.POST['1sthelp']
        secondno = request.POST['2ndhelp']
        state = request.POST['state']
        city = request.POST['city']
        facilities = []
        for i in range(1,7):
            try:
                facilities.append(request.POST[f'field{i}'])
            except:
                pass
        facilities = ', '.join(facilities)
        desc = request.POST['moreinfo']

        ## verification if needed
        myobj = pad(first_name=firstname,last_name=lastname,first_contact=firstno,second_contact=secondno,state=state,city=city,facilities=facilities,desc=desc)
        myobj.save()
        messages.success(request,'Your data has been sent for verification.')
        return redirect('/')
    else:
        return redirect('/login')

def find(request):
    tdata = pad.objects.all()
    data = []
    for tempdata in tdata:
        if tempdata.verified:
            data.append(tempdata)
        if len(data) == 20:
            return render(request,'find.html',{'data':data})
    return render(request,'find.html',{'data':data})

def filtersmohitmade(request):
    city = ''
    inpt = ''
    state = ''
    helptype = ''
    choice = ''
    try:
        city = request.GET['city']
    except:
        pass
    try:
        inpt = request.GET['input']
    except:
        pass
    try:
        state = request.GET['state']
    except:
        pass
    try:
        choice = request.GET['choice']
    except:
        pass
    try:
        helptype = request.GET['choice1']
    except:
        pass
    

    result = []

    if inpt!='':
        fres = pad.objects.filter(first_name__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(last_name__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(first_contact__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(second_contact__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(state__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(city__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(facilities__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
        fres = pad.objects.filter(desc__contains=inpt)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)

    if city != '' and helptype != '':
        fres = pad.objects.filter(city=city,facilities__contains=helptype)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)

    if city != '':
        fres = pad.objects.filter(city=city)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
    
    if state != '':
        fres = pad.objects.filter(state=state)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
    if helptype!= '':
        fres = pad.objects.filter(facilities__contains=helptype)
        for q in fres:
            if q not in result and q.verified:
                result.append(q)
    if not len(result):
        messages.error(request,'Sorry No data Found For your Filters')
    return render(request,'find.html',{'data':result})


def aboutus(request):
    return render(request,'about-us.html')