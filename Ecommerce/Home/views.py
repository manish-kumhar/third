from urllib import request
import json
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout

from . models import Mens as mensboy
from . models import order as Orderdone
# from . models import Mens,Womens,Kids as AllProducts


# Create your views here.
def Home1(request):
    return render(request,"homepage/index.html")

def Signin(request):
    return render(request,"homepage/signin.html")

def Signindo(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email= username
        pass1= request.POST.get("password")
        pass2= request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        
        # validationssssss
        if (User.objects.filter(username=username).exists()): 
            # messages.add_message(request, messages.INFO, 'Username already exist.')
            return redirect("/signin/")           
            

        if(not(len(pass1)>7 and not pass1.isalnum())):
            # messages.add_message(request, messages.INFO, 'Password must belonger then 8 characters and should contain a symbol.')
            return redirect("/signin/")
        
        if(not(pass1==pass2)):
            # messages.add_message(request, messages.INFO, 'Both the password must be same.')
            return redirect("/signin/")

        else:
            try:
                newUser = User.objects.create_user(username,email,pass1)
                newUser.first_name = first_name
                newUser.last_name = last_name
                newUser.save()
                # messages.add_message(request, messages.SUCCESS, 'Account succsessfully Created. Please Login to continue.')
                return redirect("/login/")
            except Exception as e:
                # messages.add_message(request, messages.ERROR, e)
                return redirect("/signin/")            
    else:
        # messages.add_message(request, messages.ERROR, 'Please SignIn.')
        return redirect("/login/")



def Login(request):
    return render(request,"homepage/login.html")

def Logindo(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(username = username , password = password )

        if user is not None:
            login(request,user)
            # messages.add_message(request, messages.SUCCESS, 'LOGIN successfull!!')
            return redirect("/")

        else:
            # messages.add_message(request, messages.ERROR, 'Email or password is not valid. ')
            return redirect("/login/")
    else:
        # messages.add_message(request, messages.ERROR, 'Please Login.')
        return redirect("/login/")
    




def Mens(request):
    Mens_products=mensboy.objects.all()
    params = {
        "data":Mens_products
    }
    
    
    return render(request,"homepage/mens.html",params)


def Womens(request):
    Womens_products=mensboy.objects.all()
    params = {
        "data":Womens_products
    }
    return render(request,"homepage/womens.html",params)
    

def Kids(request):
    Kids_products=mensboy.objects.all()
    params = {
        "data":Kids_products
    }
    return render(request,"homepage/kids.html",params)


def Accessories(request):
    Accessories_products=mensboy.objects.all()
    params = {
        "data":Accessories_products
    }
    return render(request,"homepage/Accessories.html",params)




def Detail_mens(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_mens.html",params)


def Detail_womens(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_womens.html",params)

    

def Detail_kids(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_kids.html",params)
    

def Detail_accessories(request,id):
    # name = request.GET.get("id")

    try:
        params = {"data":mensboy.objects.get(id=id),"error":"null"}
    except:
        params = {"data":{},"error":"Product not found"}

    return render(request,"homepage\details_accessories.html",params)



def Cartpage(request):
    return render(request,"homepage/cart.html")



def Checkout(request):
    str = request.POST.get("cartJson")
    cart = json.loads(str)
    currentCart = cart

    
    totalPrice = 0 
    for id in cart:
        temp= cart[id]
        # tempOb0 = mensboy.objects.get(id=id)
        tempOb =mensboy.objects.get(id=id)
        # tempOb2 = kidschild.objects.get(id=id)
        # tempOb=tempOb0+tempOb1+tempOb2
        

        price = tempOb.price
        temp["price"]=price
        temp["totalItemPrice"] = price * temp["value"]
        totalPrice = totalPrice + temp["totalItemPrice"]
        currentCart[id] = temp 
    
    params = {
        "totalPrice" : totalPrice,
        "data": currentCart
    }
    print("this is cart") 
  

    return render(request,"homepage/checkout.html",params)


def submitcheckout(request):
    if(request.method=="POST"):
        jsonCart= request.POST.get("jsonCart")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        email= request.POST.get("email")
        address= request.POST.get("address")
        state= request.POST.get("state")
        zip= request.POST.get("zip")
        isSameBillingAddress= request.POST.get("isSameBillingAddress")
        if(isSameBillingAddress=="on"):
            isSameBillingAddress = True
        else:
            isSameBillingAddress = False
        newOrder = Orderdone(jsonCart=jsonCart,email=email, first_name=first_name ,last_name=last_name,state=state,zip=zip,address=address,isSameBillingAddress=isSameBillingAddress)
        newOrder.save()
        return render(request,"homepage/submitcheckout.html")
    else:
        return HttpResponse("You are on a wrong page. please <a href='/course/list'>Click here</a> to add items")

    return HttpResponse("Thank you")
    # return render(request,"course\contactus.html")




def ContactUs(request):
    return render(request,"homepage/contact.html")





    