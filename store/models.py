from django.db import models
from django.contrib.auth.models import User

import datetime

class Location(models.Model):
    locationCode = models.CharField(max_length=10, null=True, blank=True)
    locationName = models.CharField(max_length=100, null=True, blank=True)
    currency = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.locationName


class Region(models.Model):
    regioncode = models.CharField(max_length=10, null= False)
    regionname = models.CharField(max_length=200, null= False)
    description = models.CharField(max_length=500, null= True, blank= True)
    countrycode = models.ForeignKey(Location, on_delete= models.SET_NULL, null = True, blank = True)
    creationdate = models.DateTimeField(auto_now_add=True, blank = True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.regionname


class Area(models.Model):
    areaname = models.CharField(max_length=200, null= False)
    regioncode = models.ForeignKey(Region, on_delete= models.SET_NULL, null = True, blank = True)
    creationdate = models.DateTimeField(auto_now_add=True, blank = True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.areaname

class StatusInfo(models.Model):
    status = models.CharField(max_length=100, null= True, blank= True)
    statusfor = models.CharField(max_length=200, null= True, blank= True)
    isActive = models.BooleanField(default= True, null= True, blank= True)

    def __str__(self):
        return self.status


class Category(models.Model):
    categoryname = models.CharField(max_length= 200, null= False, blank= False)
    categorydesc = models.CharField(max_length=500, null= True, blank= True)
    categoryimage = models.ImageField(null= True, blank = True)
    creationdate = models.DateTimeField(auto_now_add=True, blank = True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    

    def __str__(self):
        return self.categoryname

    @property
    def CategoryImageURL(self):
        try:
            url = self.categoryimage.url 
        except:
            url = ''
        return url 


class Subcategory(models.Model):
    subcategoryname = models.CharField(max_length= 200, null= False, blank= False)
    subcatdesc = models.CharField(max_length=500, null= True, blank= True)
    categoryname = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, blank = True)
    parentsubcategory = models.ForeignKey('self', on_delete= models.SET_NULL, null = True, blank = True)
    subcategoryimage = models.ImageField(null= True, blank = True)
    creationdate = models.DateTimeField(auto_now_add=True, blank = True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    haveproducts = models.BooleanField(default= False, null= True, blank= True)
    

    def __str__(self):
        return self.subcategoryname

    @property
    def SubCategoryImageURL(self):
        try:
            url = self.subcategoryimage.url 
        except:
            url = ''
        return url 



class Supplier(models.Model):
    suppliername = models.CharField(max_length= 200, null= False, blank= False)
    suppliertype = models.CharField(max_length= 200, null= False, blank= True)
    supplierdesc = models.CharField(max_length=500, null= True, blank= True)
    supplieraddress = models.CharField(max_length=500, null= True, blank= True)
    suppliercountry = models.ForeignKey(Location, on_delete= models.SET_NULL, null = True, blank = True)
    suppliercontact = models.CharField(max_length=500, null= True, blank= True)

    def __str__(self):
        return self.suppliername
        

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null = True, blank = True)
    first_name = models.CharField(max_length=200, null= True)
    last_name = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null= True)

    def __str__(self):
        return self.first_name

    @property
    def get_customer_name(self):
        return self.first_name + ' ' + self.last_name

       

class Product(models.Model):
    name = models.CharField(max_length=200, null= True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    subcategory = models.ForeignKey(Subcategory, on_delete = models.SET_NULL, null = True)
    supplier = models.ForeignKey(Supplier, on_delete= models.SET_NULL, null = True)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank= True)
    purchase_date = models.DateField(null = True, blank = True)
    ispopular = models.BooleanField(default= False, null= True, blank= True)
    quantity = models.IntegerField(default= 0, null = True, blank = True)
    unit = models.CharField(max_length=200, null= True, blank= True)
    date_creation = models.DateTimeField(auto_now_add= True, null= True, blank= True)
    bengali_name = models.CharField(max_length=200, null= True, blank= True)

    def __str__(self):
        return self.name 

    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url 


    @property
    def get_prod_sold(self):
        orderitems = self.orderitem_set.all()
        stock = sum([item.quantity for item in orderitems])
        return stock

    @property
    def get_stock(self):
        stock = self.quantity - self.get_prod_sold
        return stock


    @property
    def get_discounted_price(self):
        disc = self.productoffers_set.all().order_by('-id')[:1]
        #disc_price = sum([disc_p.get_discount  for disc_p in disc])
        disc_price = sum([disc_p.get_discount for disc_p in disc])
        return disc_price 

class ProductOffers(models.Model):
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null = True)
    discount_prcnt = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(auto_now_add = False, null=True, blank=True)
    end_date = models.DateField(auto_now_add = False, null=True, blank=True)
    #date_created = models.DateField(auto_now_add = True, null=True, blank=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_discount(self):
        curdate = datetime.date.today()
        if curdate >= self.start_date and curdate <= self.end_date:
            discounted_price = self.product.price * ((100-self.discount_prcnt)/100)
        else:
            discounted_price = self.product.price
        return discounted_price

    @property
    def get_time_limit(self):
        enddate = datetime.datetime.strptime(str(self.end_date) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        diff= enddate - datetime.datetime.now()
        time = diff.seconds % (24*3600)
        hour = time // 3600
        time %= 3600
        minute = time // 60
        time %= 60
        second = time

        timestring = str(diff.days) +' days '+ str(hour) +' hours '+ str(minute) +' minutes left'
        return timestring


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null = True, blank =True)
    date_ordered = models.DateTimeField(auto_now_add= True)
    complete = models.BooleanField(default= False)
    transaction_id = models.CharField(max_length=100, null= True)
    order_status = models.ForeignKey(StatusInfo, on_delete= models.SET_NULL, null= True, blank= True)
    order_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank= True)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank= True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank= True)


    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        #shipping = False
        #orderitems = self.orderitem_set.all()
        #for i in orderitems:
            #if i.product.digital == False:
                #shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_shipping_area(self):
        areainfo = self.shippingaddress_set.all()
        area = ([ar.area + ', ' + ar.city for ar in areainfo])
        return area 

    @property
    def get_delivery_date(self):
        deliverydate = self.shippingaddress_set.all()
        d_date = ([d_date.delivery_date  for d_date in deliverydate])
        return d_date 

    @property
    def get_delivery_charge(self):
        deliv_charge = 100
        #cityinfo = self.shippingaddress_set.all()
        #city = ([ct.city for ct in cityinfo])
        
        #for i in city:
        #    if i == 'Dhaka':
        #        if self.get_cart_total >= 1000:
        #            deliv_charge = 50
        #        else:
        #            deliv_charge = 100
                    
        #    else:
        #        deliv_charge = 100

        if self.get_cart_total >= 1500:
            deliv_charge = 50
        else:
            deliv_charge = 100

        return deliv_charge




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL, null = True)
    quantity = models.IntegerField(default= 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add= True) 
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        #total = self.product.price * self.quantity
        if self.product.get_discounted_price != 0:
            if self.product.price == self.product.get_discounted_price:
                total = self.product.price * self.quantity
            else:
                total = self.product.get_discounted_price * self.quantity
        else:
            total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    area = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    #region = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=100, null=False, blank = True)
    delivery_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.order) + ', ' + self.area + ', ' + self.city

class BannerImages(models.Model):
    bannername = models.CharField(max_length=200, null= True, blank= True)
    bannerimage = models.ImageField(null = True, blank = True)
    bannertext = models.CharField(max_length=200, null= True, blank= True)
    isactive = models.BooleanField(default= True, null= True, blank= True)

    def __str__(self):
        return self.bannername

    @property
    def BannerimageURL(self):
        try:
            url = self.bannerimage.url 
        except:
            url = ''
        return url 

class DeliveryMan(models.Model):
    name = models.CharField(max_length=200, null= True)
    contactnumber = models.CharField(max_length=100, null= True, blank= True)

    def __str__(self):
        return self.name

class OrderDelivery(models.Model):
    deliveryman = models.ForeignKey(DeliveryMan, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True, blank= True)
    assignDate = models.DateTimeField(auto_now_add=True)
    deliveryDate = models.DateTimeField(null=True, blank= True)

    def __str__(self):
        return str(self.deliveryman)