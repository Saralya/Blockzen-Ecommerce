from django.shortcuts import render, redirect
from store.models import *
from adminpanel.forms import  * #CreateRegionForm, CreateAreaForm, CreateCategoryForm, CreateSubcategoryForm
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

from store.utils import cookieCart, cookieData, guestOrder
from store.models import *

from adminpanel.decorators import allowed_users, admin_only

from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import datetime

import csv
from django.http import HttpResponse, JsonResponse

#####################################################################################################################

@login_required(login_url='login')
@admin_only
def dashboard(request):
    regions = Region.objects.all()
    areas = Area.objects.all()

    orders = Order.objects.filter(complete = True).order_by('-id')
    total_orders = orders.count()
    pending = StatusInfo.objects.get(status='Pending')
    delivered = StatusInfo.objects.get(status='Delivered')
    inprocess = StatusInfo.objects.get(status='In Process')

    pendingCount = pending.order_set.all().count()
    deliveredCount = delivered.order_set.all().count()
    inprocessCount = inprocess.order_set.all().count()

    pendingOrders = pending.order_set.all()
    readyforDelivery = inprocess.order_set.all().order_by('-id')

    deliveryInfo = ShippingAddress.objects.filter(order__order_status = pending)

    productlist = Product.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    
    #######################################
    ### Pie Chart Data
    varDate = datetime.datetime.today()
    varYear = varDate.year
    labels = []
    data = []
    

    status = StatusInfo.objects.all()

    for i in status:
        orderdata = i.order_set.filter(complete=True, order_status=i.id, date_ordered__year=varYear).count()
        labels.append(i.status)
        data.append(orderdata)
    ############################################

    context = {
        'regions': regions, 
        'areas': areas, 
        'orders': orders, 
        'total_orders': total_orders, 
        'pendingCount': pendingCount,
        'deliveredCount': deliveredCount,
        'inprocessCount': inprocessCount,
        'deliveryInfo': deliveryInfo,
        'pendingOrders': pendingOrders,
        'readyforDelivery' : readyforDelivery,
        'productlist' : productlist,
        'data': data,
        'cartItems': cartItems,
        'order' : order,
        'items' : items,
        'labels': labels,
        'data': data
        }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def adminpanel(request):
    regions = Region.objects.all()
    areas = Area.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    suppliers = Supplier.objects.all()
    products = Product.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    #######################################
    ### Pie Chart Data
    varDate = datetime.datetime.today()
    varYear = varDate.year
    labels = []
    data = []
    

    status = StatusInfo.objects.all()

    for i in status:
        orderdata = i.order_set.filter(complete=True, order_status=i.id, date_ordered__year=varYear).count()
        labels.append(i.status)
        data.append(orderdata)
    ############################################
    

    context = {
        'regions': regions, 
        'areas': areas, 
        'categories': categories, 
        'subcategories': subcategories, 
        'suppliers': suppliers, 
        'products': products,
        'data': data,
        'cartItems': cartItems,
        'order' : order,
        'items' : items,
        'labels': labels,
        'data': data
        }
    #return render(request, 'adminpanel/adminpanel.html', context)
    return render(request, 'adminpanel/dashboard.html', context)


@login_required(login_url='login')
@admin_only
def region(request):
    headertext = 'Region'
    regions = Region.objects.all()

    context ={
        'headertext': headertext,
        'regions': regions,
    }

    return render(request, 'adminpanel/adminview.html', context)


@login_required(login_url='login')
@admin_only
def createregion(request):
    form = CreateRegionForm()

    if request.method == "POST":
        form = CreateRegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')

    pagetitle = 'Region'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

@login_required(login_url='login')
@admin_only
def updateregion(request, rgnID):
    regions = Region.objects.get(id = rgnID)
    form = CreateRegionForm(instance = regions)

    if request.method == "POST":
        form = CreateRegionForm(request.POST, instance = regions)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')

    pagetitle = 'Region'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

##################################################################################
#########           AREA             #############################################
##################################################################################

@login_required(login_url='login')
@admin_only
def area(request):
    headertext = 'Area'
    areas = Area.objects.all()

    context ={
        'headertext': headertext,
        'areas': areas,
    }

    return render(request, 'adminpanel/adminview.html', context)

@login_required(login_url='login')
@admin_only
def createarea(request):
    form = CreateAreaForm()

    if request.method == "POST":
        form = CreateAreaForm(request.POST)
        if form.is_valid():
            areadata = form.save(commit=False)
            areadata.createdby = request.user
            areadata.save()
            return redirect('adminpanel')

    pagetitle = 'Area'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

@login_required(login_url='login')
@admin_only
def updatearea(request, areaID):
    areas = Area.objects.get(id = areaID)
    form = CreateAreaForm(instance = areas)

    if request.method == "POST":
        form = CreateAreaForm(request.POST, instance = areas)
        if form.is_valid():
            areadata = form.save(commit=False)
            areadata.createdby = request.user
            areadata.save()
            return redirect('adminpanel')

    pagetitle = 'Area'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


##################################################################################
#########           CATEGORY             #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def category(request):
    headertext = 'Category'
    categories = Category.objects.all()

    context ={
        'headertext': headertext,
        'categories': categories,
    }

    return render(request, 'adminpanel/adminview.html', context)

@login_required(login_url='login')
@admin_only
def createcategory(request):
    form = CreateCategoryForm()

    if request.method == "POST":
        form = CreateCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            categorydata = form.save(commit=False)
            categorydata.createdby = request.user
            categorydata.save()
            return redirect('adminpanel')

    pagetitle = 'Category'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updatecategory(request, categoryID):
    categories = Category.objects.get(id = categoryID)
    form = CreateCategoryForm(instance = categories)

    if request.method == "POST":
        form = CreateCategoryForm(request.POST, request.FILES, instance = categories)
        if form.is_valid():
            categorydata = form.save(commit=False)
            categorydata.createdby = request.user
            categorydata.save()
            return redirect('adminpanel')

    pagetitle = 'Category'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


##################################################################################
#########           SUB CATEGORY             #####################################
##################################################################################
@login_required(login_url='login')
@admin_only
def subcategory(request):
    headertext = 'Subcategory'
    subcategories = Subcategory.objects.all()

    context ={
        'headertext': headertext,
        'subcategories': subcategories,
    }

    return render(request, 'adminpanel/adminview.html', context)

@login_required(login_url='login')
@admin_only
def createsubcategory(request):
    form = CreateSubcategoryForm()

    if request.method == "POST":
        form = CreateSubcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategorydata = form.save(commit=False)
            subcategorydata.createdby = request.user
            subcategorydata.save()
            return redirect('adminpanel')

    pagetitle = 'Sub-category'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updatesubcategory(request, subcategoryID):
    subcats = Subcategory.objects.get(id = subcategoryID)
    form = CreateSubcategoryForm(instance = subcats)

    if request.method == "POST":
        form = CreateSubcategoryForm(request.POST, request.FILES, instance = subcats)
        if form.is_valid():
            subcategorydata = form.save(commit=False)
            subcategorydata.createdby = request.user
            subcategorydata.save()
            return redirect('adminpanel')

    pagetitle = 'Sub-category'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


##################################################################################
#########           SUPPLIER             #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def supplier(request):
    headertext = 'Supplier'
    suppliers = Supplier.objects.all()

    context ={
        'headertext': headertext,
        'suppliers': suppliers,
    }

    return render(request, 'adminpanel/adminview.html', context)

@login_required(login_url='login')
@admin_only
def createsupplier(request):
    form = CreateSupplierForm()

    if request.method == "POST":
        form = CreateSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')

    pagetitle = 'Supplier'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updatesupplier(request, supplierID):
    suppliers = Supplier.objects.get(id = supplierID)
    form = CreateSupplierForm(instance = suppliers)

    if request.method == "POST":
        form = CreateSupplierForm(request.POST, instance = suppliers)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')

    pagetitle = 'Supplier'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


##################################################################################
#########            PRODUCT             #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def product(request):
    headertext = 'Product'
    products = Product.objects.all()

    context ={
        'headertext': headertext,
        'products': products,
    }

    return render(request, 'adminpanel/adminview.html', context)


@login_required(login_url='login')
@admin_only
def createproduct(request):
    form = CreateProductForm()

    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            proddata = form.save(commit=False)
            #proddata.purchase_date = request.POST.get('purchasedate')
            proddata.save()
            #form.save()
            return redirect('product')

    pagetitle = 'Product'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updateproduct(request, productID):
    products = Product.objects.get(id = productID)
    form = CreateProductForm(instance = products)

    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance = products)
        if form.is_valid():
            proddata = form.save(commit=False)
            #proddata.purchase_date = request.POST.get('purchasedate')
            proddata.save()
            return redirect('product')

    pagetitle = 'Product'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

##################################################################################
#########            PROMOTIONS          #########################################
##################################################################################


@login_required(login_url='login')
@admin_only
def createproductoffer(request):
    form = CreateProductOfferForm()

    if request.method == "POST":
        form = CreateProductOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productoffers')

    pagetitle = 'Promotional Offers'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

@login_required(login_url='login')
@admin_only
def productoffers(request):
    headertext = 'Offers'
    offers = ProductOffers.objects.all()

    context ={
        'headertext': headertext,
        'offers': offers,
    }

    return render(request, 'adminpanel/adminview.html', context)

@login_required(login_url='login')
@admin_only
def updateproductoffer(request, productID):
    products = ProductOffers.objects.get(id = productID)
    form = CreateProductOfferForm(instance = products)

    if request.method == "POST":
        form = CreateProductOfferForm(request.POST, request.FILES, instance = products)
        if form.is_valid():
            form.save()
            return redirect('productoffers')

    pagetitle = 'Promotional Offers'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)

##################################################################################
#########            CUSTOMER            #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def customer(request):
    headertext = 'Customer'
    customers = Customer.objects.all()

    context ={
        'headertext': headertext,
        'customers': customers,
    }

    return render(request, 'adminpanel/adminview.html', context)

##################################################################################
#########            DELIVERY MAN        #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def deliveryman(request):
    headertext = 'Delivery Man'
    delvman = DeliveryMan.objects.all()

    context ={
        'headertext': headertext,
        'delvman': delvman,
    }

    return render(request, 'adminpanel/adminview.html', context)


@login_required(login_url='login')
@admin_only
def createdeliveryman(request):
    form = CreateDelvmanForm()

    if request.method == "POST":
        form = CreateDelvmanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('deliveryman')

    pagetitle = 'Delivery Man'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updatedeliveryman(request, ID):
    delvman = DeliveryMan.objects.get(id = ID)
    form = CreateDelvmanForm(instance = delvman)

    if request.method == "POST":
        form = CreateDelvmanForm(request.POST, request.FILES, instance = delvman)
        if form.is_valid():
            form.save()
            return redirect('deliveryman')

    pagetitle = 'Delivery Man'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)



##################################################################################
#########            BANNER IMAGE        #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def bannerimage(request):
    headertext = 'Banner Image'
    banner = BannerImages.objects.all()

    context ={
        'headertext': headertext,
        'banner': banner,
    }

    return render(request, 'adminpanel/adminview.html', context)


@login_required(login_url='login')
@admin_only
def createbanner(request):
    form = CreateBannerForm()

    if request.method == "POST":
        form = CreateBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('banner')

    pagetitle = 'Banner Image'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


@login_required(login_url='login')
@admin_only
def updatebanner(request, ID):
    banner = BannerImages.objects.get(id = ID)
    form = CreateBannerForm(instance = banner)

    if request.method == "POST":
        form = CreateBannerForm(request.POST, request.FILES, instance = banner)
        if form.is_valid():
            form.save()
            return redirect('bannerimage')

    pagetitle = 'Banner Image'
    context = {'form': form, 'pagetitle': pagetitle}
    return render(request, 'adminpanel/adminEntry.html', context)


##################################################################################
#########            USER                #########################################
##################################################################################
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)         
            return redirect('home')

        else:
            messages.info(request,'User name or password is incorrect.')
            

    context = {}
    return render(request, 'adminpanel/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')


def userregistration(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            uname = form.cleaned_data.get('username')
            
            # for Customer table
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            
            userinfo = Customer.objects.create(user=user, email = email, first_name = first_name, last_name = last_name)
            userinfo.save()
           

            messages.success(request, 'Account was created for ' + uname )    

            return redirect('login')
        
        else:
            messages.error(request, '')

    context = {'form': form}
    return render(request, 'adminpanel/registration.html', context)

@login_required(login_url='login')
@admin_only
def deliverydetails(request):
    deliveryman = DeliveryMan.objects.all()

    pending = StatusInfo.objects.get(status='Pending')

    pendingOrders = pending.order_set.all()

    

    form = OrderDeliveryForm()

    if request.method == "POST":
        form = OrderDeliveryForm(request.POST)

        if form.is_valid():
            orderNo = form.cleaned_data.get('order')

            ofdata = form.save(commit=False)
            ofdata.deliveryDate = request.POST.get('deliverydate')
            ofdata.save()

            status_info = StatusInfo.objects.get(status = 'In Process')
            updOrder = Order.objects.get(id = orderNo.id)
            updOrder.order_status = status_info
            updOrder.save()
            


        return redirect('delivery')


    context = {
        'deliveryman': deliveryman,
        'pendingOrders' : pendingOrders,
        'form' : form
    }

    return render(request, 'adminpanel/delivery.html', context)


##################################################################################
#########            REPORTS             #########################################
##################################################################################
@login_required(login_url='login')
@admin_only
def productstockrpt(request):
    reporttitle = 'Product Stock'
    reportdata = Product.objects.all()

    context ={
        'reporttitle': reporttitle,
        'reportdata': reportdata,
    }

    return render(request, 'adminpanel/report.html', context)



@login_required(login_url='login')
@admin_only
def exporttoexcel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Product Category', 'Purchase Quantity','Current Stock'])

    products = Product.objects.all()
    
    for prod in products:
        writer.writerow([prod.name,prod.subcategory.categoryname, prod.quantity, prod.get_stock])

    return response


@login_required(login_url='login')
@admin_only
def resultsData(request):
    chartdata = []


    status = StatusInfo.objects.all()

    for i in status:
        orderdata = i.order_set.filter(complete=True, order_status=i.id).count()
        chartdata.append({i.status: orderdata})

    return JsonResponse(chartdata, safe=False)


@login_required(login_url='login')
@admin_only
def revenueData(request):
    chartdata = []
    curdate = datetime.date.today()
    year = curdate.year
    vMonth = ''
    varAmount = 0
    month= [
        {'varMonth':1, 'name':'Jan'},
        {'varMonth':2, 'name':'Feb'},
        {'varMonth':3, 'name':'Mar'},
        {'varMonth':4, 'name':'Apr'},
        {'varMonth':5, 'name':'May'},
        {'varMonth':6, 'name':'Jun'},
        {'varMonth':7, 'name':'Jul'},
        {'varMonth':8, 'name':'Aug'},
        {'varMonth':9, 'name':'Sep'},
        {'varMonth':10, 'name':'Oct'},
        {'varMonth':11, 'name':'Nov'},
        {'varMonth':12, 'name':'Dec'},
    ]

    for vMon in month:
        orders = Order.objects.filter(complete=True,date_ordered__year= year,date_ordered__month=vMon['varMonth']).aggregate(total=Sum('total'))
        oCount =  Order.objects.filter(complete=True,date_ordered__year=year,date_ordered__month=vMon['varMonth']).count()
        if oCount != 0:
            varAmount = float(orders['total'])
            vMonth = vMon['name']
        else:
            varAmount = 0
            vMonth = vMon['name']
        chartdata.append({vMonth:varAmount})


    return JsonResponse(chartdata, safe=False)


@login_required(login_url='login')
@admin_only
def pieresultsData(request):
    chartdata = []
    labels = []
    data = []
    

    status = StatusInfo.objects.all()

    for i in status:
        orderdata = i.order_set.filter(complete=True, order_status=i.id).count()
        #chartdata.append({i.status: orderdata})
        labels.append(i.status)
        data.append(orderdata)


    
    return render(request, 'adminpanel/test.html', {'labels': labels, 'data': data})