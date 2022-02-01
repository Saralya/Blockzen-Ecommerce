from django.shortcuts import render, redirect
from store.models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cookieData, guestOrder
from adminpanel.forms import UserProfileForm, ChangePasswordForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse_lazy

#from hitcount.models import HitCount
#from hitcount.views import HitCountMixin

from django.db.models import Sum




def home(request):

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    curdate = datetime.date.today()
    #visitor_count = HitCountMixin.hit_count()



    #itemcount = OrderItem.objects.values('product__name','product__price', 'product__image').annotate(items = Sum('quantity')).order_by('-items')[:3]
    topProds = Product.objects.all().annotate(quantity_sum=Sum('orderitem__quantity')).order_by('-quantity_sum')[:20]

    newProds = Product.objects.all().order_by('-date_creation')[:50]

    categories = Category.objects.all()[:6]
    products = Product.objects.filter(ispopular=True)
    bannerimgs = BannerImages.objects.filter(isactive=True) 
    minID = bannerimgs.order_by('id').first()

    prodoffers = ProductOffers.objects.filter(start_date__lte = curdate, end_date__gte = curdate)

    context = {
        'bannerimgs': bannerimgs, 
        'minID': minID, 
        'categories': categories, 
        'products': products, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        #'itemcount' : itemcount,
        'topProds' : topProds,
        'prodoffers': prodoffers,
        'newProds' : newProds,
        #'visitor_count': visitor_count,
        }
    return render(request, 'store/home.html', context)


def search(request):
    varText = request.GET.get('txtSearch','')
    if varText:
        result = Product.objects.filter(name__contains = varText).distinct()
    else:
        result = []

    categories = Category.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    
        
    context = {
        'categories': categories, 
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'varText': varText,
        'products' : result
    }
    return render(request, 'store/products.html', context)

def homeBangla(request):
    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    curdate = datetime.date.today()

    #itemcount = OrderItem.objects.values('product__name','product__price', 'product__image').annotate(items = Sum('quantity')).order_by('-items')[:3]
    topProds = Product.objects.all().annotate(quantity_sum=Sum('orderitem__quantity')).order_by('-quantity_sum')[:10]

    categories = Category.objects.all()[:6]
    products = Product.objects.filter(ispopular=True)
    bannerimgs = BannerImages.objects.filter(isactive=True) 
    minID = bannerimgs.order_by('id').first()

    prodoffers = ProductOffers.objects.filter(start_date__lte = curdate, end_date__gte = curdate)

    context = {'bannerimgs': bannerimgs, 'minID': minID, 'categories': categories, 'products': products, 'items': items, 'order': order, 
    'cartItems': cartItems,
    #'itemcount' : itemcount,
    'topProds' : topProds,
    'prodoffers': prodoffers,
    }
    return render(request, 'store/homeBangla.html', context)

def test(request):
    context = {}
    return render(request, 'adminpanel/test.html', context)


def shop(request):
    categories = Category.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    
    context = {'categories': categories, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/categories.html', context)


def cart(request):
    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    
    if request.user.is_authenticated:
        grandTotal = order.get_cart_total + order.get_delivery_charge

    else:
        total = data["total"]
        delvcharge = data["delvcharge"]
        grandTotal = total + delvcharge

    # Get area list values
    cities = Region.objects.all()
    #area = cities.area_set.all()
    area = Area.objects.all()
    

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'cities': cities, 'area': area, 'grandTotal': grandTotal}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product id: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False) 
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
		
	########################################################################
    # Added 22-Nov-20
    unitPrice = 0
    if orderItem.product.get_discounted_price == 0:
        unitPrice = orderItem.product.price
    elif orderItem.product.price == orderItem.product.get_discounted_price:
        unitPrice = orderItem.product.price
    else:
        unitPrice = orderItem.product.get_discounted_price

    orderItem.unit_price = unitPrice
    #########################################################################

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    
    return JsonResponse('Item was added', safe = False)


def processOrder(request):
    #transaction_id = datetime.datetime.now().timestamp()
    transaction_id = int(str(datetime.datetime.now().timestamp()).replace('.', ''))
    data = json.loads(request.body)
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) 
        
    else:
        customer, order = guestOrder(request, data)

    grandTotal = order.get_cart_total + order.get_delivery_charge

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    orderStatus = StatusInfo.objects.get(status = 'Pending')

    if total == float(order.get_cart_total):
        order.complete = True
        order.order_amount = order.get_cart_total
        order.delivery_charge = order.get_delivery_charge
        order.total = grandTotal
        order.date_ordered = datetime.datetime.now()
        order.order_status = orderStatus 
        
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            area = data['shipping']['area'],
            zipcode = data['shipping']['zipcode'],
            delivery_date = data['shipping']['deliverydate']
        )

    return JsonResponse('Payment complete', safe = False)


def subcategories(request, varID):
    category = Category.objects.get(id = varID)
    subcategories = category.subcategory_set.all().filter(parentsubcategory_id__isnull = True)

    categories = Category.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'categories' : categories, 'category': category, 'subcategories': subcategories, 'cartItems': cartItems, 'items': items, 'order': order}

    return render(request, 'store/subcategories.html', context)


def subcategoryviews(request, varID, varName):    
    subcategories = Subcategory.objects.filter(parentsubcategory = varID)
    category = varName

    categories = Category.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'categories' : categories, 'category': category, 'subcategories': subcategories, 'cartItems': cartItems, 'items': items, 'order': order}

    return render(request, 'store/subcategories.html', context)


def productviews(request, varID, varName):
    products = Product.objects.filter(subcategory_id=varID) 
    category = varName

    categories = Category.objects.all()

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'categories' : categories, 'category': category, 'products': products, 'cartItems': cartItems, 'items': items, 'order': order}

    return render(request, 'store/products.html', context)


def productdetails(request, prodID):
    products = Product.objects.filter(id=prodID) 
    

    data = cookieData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'products': products, 'cartItems': cartItems, 'items': items, 'order': order}

    return render(request, 'store/productdetails.html', context)


def userprofile(request):
    customer = Customer.objects.get(user = request.user)

    orders = customer.order_set.filter(complete = True)
    orderCount = orders.count()

    form = UserProfileForm(instance = customer)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance= customer)
        if form.is_valid():
            form.save()
            return redirect('userprofile')

    context = {
        'form': form, 
        'customer': customer,
        'orderCount': orderCount
        }
    return render(request, 'store/userprofile.html', context)

def userpanel(request):
    customer = Customer.objects.get(user = request.user)
    orders = customer.order_set.filter(complete = True)
    orderCount = orders.count()

    context = {
        'orders': orders,
        'orderCount': orderCount
    }

    return render(request, 'store/userpanel.html', context)


def orderdetails(request, varOrder):
    items = OrderItem.objects.filter(order=varOrder)

    itemTotal = items.aggregate(total = Sum('unit_price'))

    context = {
        'items': items,
        'orderNo' : varOrder,
        'itemTotal': itemTotal
    }

    return render(request, 'store/orderdetails.html', context)


class change_password(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url= reverse_lazy('userprofile')


def privacypolicy(request):
    

    context = {
        
    }

    return render(request, 'store/privacy.html', context)

def refundpolicy(request):
    

    context = {
        
    }

    return render(request, 'store/refund.html', context)

def termsandconditions(request):
    

    context = {
        
    }

    return render(request, 'store/terms.html', context)