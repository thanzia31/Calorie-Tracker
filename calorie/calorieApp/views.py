from django.shortcuts import render,redirect
from calorieApp.forms import SignUp,UserDetailForm,AddItemForm
from calorieApp.compute import foods,return_unit,return_recepie
from calorieApp import models
from django.db.models import Q
from datetime import date,datetime,timedelta
from calorieApp import graph,recommend
import warnings
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import random
import json
from django.contrib.auth.models import User
warnings.filterwarnings("ignore")

  
def index(request):
    
    return render(request,'calorieApp/index.html')

def index1(request):
    
    breakfast=models.AddItems.objects.filter(Q(user=request.user) & Q(date=date.today()) & Q(meal_time='breakfast'))
    lunch=models.AddItems.objects.filter(Q(user=request.user) & Q(date=date.today()) & Q(meal_time='lunch'))
    snack=models.AddItems.objects.filter(Q(user=request.user) & Q(date=date.today()) & Q(meal_time='snack'))
    dinner=models.AddItems.objects.filter(Q(user=request.user) & Q(date=date.today()) & Q(meal_time='dinner'))
    
    tbf=0
    tln=0
    tsn=0
    tdn=0
    for i in breakfast:
        tbf=tbf+i.calorie
    for i in lunch:
        tln=tln+i.calorie
    for i in snack:
        tsn=tsn+i.calorie
    for i in dinner:
        tdn=tdn+i.calorie
    tcal=tbf+tln+tsn+tdn
    try:
        user_detail=models.UserDetails.objects.get(name=request.user)
        
        cal_needed=user_detail.calorie_needed-tcal
    except Exception:
        print("hi")
        user_detail='null'
        cal_needed=0
        return redirect("/userdetail/")
    
    print(user_detail)
    return render(request,'calorieApp/index1.html',{'user_detail':user_detail,'bf':breakfast,'ln':lunch,'sn':snack,'dn':dinner,
                                                    'tbf':tbf,'tln':tln,'tsn':tsn,'tdn':tdn,"tcal":tcal,'calneed':cal_needed})
def Register(request):
    form=SignUp()
    if request.method=='POST':
        form=SignUp(request.POST)
        if form.is_valid():
            
            otp=random.randint(1000,9999)
            Email=request.POST.get('email')
            username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            print(Email)
            send_mail("Calorie Tracker Verification",f"Verify your account by OTP:{otp}",settings.EMAIL_HOST_USER,[Email],fail_silently=False)
            #user = form.save()
            #login(request, user)
            
            return render(request,'calorieApp/verifyOtp.html',{'otp':otp,'email':Email,'username':username,'first_name':first_name,'last_name':last_name,'password1':password1,'password2':password2})
            
    return render(request,'calorieApp/register.html',{'form':form})


@csrf_exempt
def verify_otp(request):
    if request.method=='POST':
        userotp=request.POST.get('otp')
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        if password1==password2:
            form=User(first_name=first_name,username=username,last_name=last_name,email=email,password=password1)
            form.save()
            #messages.success("Account Created Successfully!!!Login")
            return redirect("/userdetail")
    return JsonResponse({'data':'hello'},status=200)

def UserDetailView(request):
    form=UserDetailForm(initial={'name':request.user})
    if request.method == "POST":
        form=UserDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/index1/")
        else:
            print(form.errors.values())
            print("no")
            
            
    return render(request,'calorieApp/UserDetail.html',{'form':form})

def AddItemView(request):
    form=AddItemForm(initial={'user':request.user})
    data=models.AddItems.objects.filter(Q(user=request.user) & Q(date=date.today()))
    print(data)

    food=foods()
    if request.method == "POST":
        form=AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/additem")
        else:
            print(form.errors)
    return render(request,'calorieApp/additem.html',{'form':form,'food':food,'data':data})

def get_food_item(request):
    item_name = request.GET.get('item_name', '')
    print('itemnameeee',item_name)
    unit=return_unit(item_name)
    return JsonResponse({'unit_of_measurement': unit})


def delete_item(request,id):
    item=models.AddItems.objects.get(id=id)
    item.delete()
    return redirect("/additem")

def update_item(request,id):
    item=models.AddItems.objects.get(id=id)
    form=AddItemForm(instance=item)
    if request.method =="POST":
        form=AddItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect("/additem")
    return render(request,'calorieApp/update.html',{'form':form})

def profile(request):
    data=models.User.objects.get(username=request.user)
    data1=models.UserDetails.objects.get(name=request.user)
    if data1.gender=='F':
        gender='Female'
        logo=True
    else:
        gender='Male'
        logo=False
    if data1.activity_factor=='1':
        activity='Little/No Exercise'
    elif data1.activity_factor=='2':
        activity='light exercise/sports 1-3 days per week'
    elif data1.activity_factor=='3':
        activity='moderate exercise/sports 3-5 days per week'
    elif data1.activity_factor=='4':
        activity='hard exercise/sports 6-7 days per week'
    else:
        activity='very hard exercise/sports & a physical job'
    
    
    

    return render(request,'calorieApp/profile.html',{'data':data,'data1':data1,'gender':gender,'activity':activity,'logo':logo})

def trackrecord(request):
    user=models.UserDetails.objects.get(name=request.user)
    d1 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    d2 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    d3 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    d4 = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    d5 = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    d6 = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    d7 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    item1=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d1))
    cal1=0
    for i in item1:
        cal1=cal1+i.calorie
    item2=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d2))
    cal2=0
    for i in item2:
        cal2=cal2+i.calorie
    item3=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d3))
    cal3=0
    for i in item3:
        cal3=cal3+i.calorie
    item4=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d4))
    cal4=0
    for i in item4:
        cal4=cal4+i.calorie
    item5=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d5))
    cal5=0
    for i in item5:
        cal5=cal5+i.calorie
    item6=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d6))
    cal6=0
    for i in item6:
        cal6=cal6+i.calorie
    item7=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d7))
    cal7=0
    for i in item7:
        cal7=cal7+i.calorie
    
    return render(request,'calorieApp/trackrecord.html',{'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'d6':d6,'d7':d7,'item1':item1,
                                        'item2':item2,'item3':item3,'item4':item4,'item5':item5,'item6':item6,'item7':item7,
                                        'cal1':cal1,'cal2':cal2,'cal3':cal3,'cal4':cal4,'cal5':cal5,'cal6':cal6,'cal7':cal7,
                                        'user':user})

def visualize(request):
    user=models.UserDetails.objects.get(name=request.user)
    d1 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    d2 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    d3 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    d4 = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    d5 = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    d6 = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    d7 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    calories=[]
    cal_needed=user.calorie_needed
    
    item1=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d1))
    cal1=0
    for i in item1:
        cal1=cal1+i.calorie
    calories.append(cal1)
    item2=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d2))
    cal2=0
    for i in item2:
        cal2=cal2+i.calorie
    calories.append(cal2)
    item3=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d3))
    cal3=0
    for i in item3:
        cal3=cal3+i.calorie
    calories.append(cal3)
    item4=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d4))
    cal4=0
    for i in item4:
        cal4=cal4+i.calorie
    calories.append(cal4)
    item5=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d5))
    cal5=0
    for i in item5:
        cal5=cal5+i.calorie
    calories.append(cal5)
    item6=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d6))
    cal6=0
    for i in item6:
        cal6=cal6+i.calorie
    calories.append(cal6)
    item7=models.AddItems.objects.filter(Q(user=request.user) & Q(date=d7))
    cal7=0
    for i in item7:
        cal7=cal7+i.calorie
    calories.append(cal7)
    graph_all_7=graph.graphfun(calories,cal_needed)
    graph1=graph.single_point(cal1,cal_needed)
    graph2=graph.single_point(cal2,cal_needed)
    graph3=graph.single_point(cal3,cal_needed)
    graph4=graph.single_point(cal4,cal_needed)
    graph5=graph.single_point(cal5,cal_needed)
    graph6=graph.single_point(cal6,cal_needed)
    graph7=graph.single_point(cal7,cal_needed)
    
    return render(request,'calorieApp/visualize.html',{'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'d6':d6,'d7':d7,
                                        'cal1':cal1,'cal2':cal2,'cal3':cal3,'cal4':cal4,'cal5':cal5,'cal6':cal6,'cal7':cal7,
                                        'cal_needed':cal_needed,'graph':graph_all_7,'graph1':graph1,'graph2':graph2,'graph3':graph3,
                                        'graph4':graph4,'graph5':graph5,'graph6':graph6,'graph7':graph7
                                        })


def recc_item(request):
    user=models.UserDetails.objects.get(name=request.user)
    bk_key = 'Breakfast'
    ln_key='Lunch'
    dn_key='Dinner'
    sn_key='Snack'
    last_update_date = request.session.get('last_update_date')
    
    print(last_update_date)
    current_date = date.today().isoformat()
    
    print(current_date)
    
    food_breakfast=list(models.AddItems.objects.filter(Q(user=request.user) & Q(meal_time='breakfast')).values_list('food',flat=True))
    food_lunch=list(models.AddItems.objects.filter(Q(user=request.user) & Q(meal_time='lunch')).values_list('food',flat=True))
    food_dinner=list(models.AddItems.objects.filter(Q(user=request.user) & Q(meal_time='dinner')).values_list('food',flat=True))
    food_snack=list(models.AddItems.objects.filter(Q(user=request.user) & Q(meal_time='snack')).values_list('food',flat=True))
    
    #request.session.clear()
    
  
    
    
    if not last_update_date or last_update_date != current_date:
        breakfast_recc = recommend.input_recc(food_breakfast,type='Breakfast')
        lunch_recc = recommend.input_recc(food_lunch,type='Lunch')
        dinner_recc = recommend.input_recc(food_dinner,type='Dinner')
        snack_recc = recommend.input_recc(food_snack,type='Snack')
        request.session[bk_key] = breakfast_recc
        request.session[ln_key] = lunch_recc
        request.session[dn_key] = dinner_recc
        request.session[sn_key] = snack_recc
        request.session['last_update_date'] = current_date
    else:
        breakfast_recc = request.session.get(bk_key, [])
        lunch_recc = request.session.get(ln_key, [])
        dinner_recc = request.session.get(dn_key, [])
        snack_recc = request.session.get(sn_key, [])
    
    #print(breakfast_recc)
       
    return render(request,'calorieApp/recc_item.html',{'user':user,'breakfast_recc':breakfast_recc,'lunch_recc':lunch_recc,
                                                       'snack_recc':snack_recc,'dinner_recc':dinner_recc
                                                       })

def get_recepie(request):
    
    item_name = request.GET.get('item_name', '')
    #print('itemnameeee',item_name)
    recepie=return_recepie(item_name)
    return JsonResponse({'recepie': recepie})