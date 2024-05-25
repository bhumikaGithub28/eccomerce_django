from django.shortcuts import render,redirect
from ecommerceapp.models import Contact, Product
from django.contrib import messages
from math import ceil
# Create your views here.
def index(request):
    allProds=[]
    catprods= Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    params={'allProds': allProds}

    return render(request,"index.html",params)
    
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")
def about(request):
    return render(request,"about.html")

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name= request.POST.get('name','')
        amount=request.POST.get('amt')
        email=request.POST.get('email','')
        address1=request.POST.get('address1','')
        address2=request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        Order=Orders(items_json=items_json,name=name,amount=amount,
        email=email,address1=address1,address2=address2,city=city,
        state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update= OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank= True



    