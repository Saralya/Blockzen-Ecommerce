from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from store.models import *

from django.contrib.admin import widgets


class CreateRegionForm(ModelForm):
    regioncode = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    regionname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))
    #countrycode = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Region
        fields = ['regioncode', 'regionname', 'description', 'countrycode']

    def __init__(self, *args, **kwargs):
        super(CreateRegionForm, self).__init__(*args, **kwargs)

        self.fields['countrycode'].widget.attrs['class'] = 'form-control'


class CreateAreaForm(ModelForm):
    areaname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Area
        fields = ['areaname', 'regioncode']

    def __init__(self, *args, **kwargs):
        super(CreateAreaForm, self).__init__(*args, **kwargs)

        self.fields['regioncode'].widget.attrs['class'] = 'form-control'
        #self.fields['createdby'].widget.attrs['class'] = 'form-control'


class CreateCategoryForm(ModelForm):
    categoryname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    categorydesc = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))
    
    class Meta:
        model = Category
        #fields = ['categoryname', 'categorydesc', 'categoryimage', 'createdby']
        fields = ['categoryname', 'categorydesc', 'categoryimage']

    def __init__(self, *args, **kwargs):
        super(CreateCategoryForm, self).__init__(*args, **kwargs)

        self.fields['categoryimage'].widget.attrs['class'] = 'form-control'
        #self.fields['createdby'].widget.attrs['class'] = 'form-control'
    

class CreateSubcategoryForm(ModelForm):
    subcategoryname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    subcatdesc = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control', 'rows':2}))
    
    class Meta:
        model = Subcategory
        fields = ['subcategoryname', 'subcatdesc', 'categoryname', 'subcategoryimage', 'parentsubcategory', 'haveproducts']

    def __init__(self, *args, **kwargs):
        super(CreateSubcategoryForm, self).__init__(*args, **kwargs)

        self.fields['categoryname'].widget.attrs['class'] = 'form-control'
        self.fields['parentsubcategory'].widget.attrs['class'] = 'form-control'
        self.fields['subcategoryimage'].widget.attrs['class'] = 'form-control'
        #self.fields['createdby'].widget.attrs['class'] = 'form-control'
        self.fields['haveproducts'].widget.attrs['class'] = 'form-control'



class CreateSupplierForm(ModelForm):
    suppliername = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    suppliertype = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    supplierdesc = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))
    supplieraddress = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    suppliercontact = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))
    
    class Meta:
        model = Supplier
        fields = ['suppliername', 'suppliertype', 'supplierdesc', 'supplieraddress', 'suppliercountry', 'suppliercontact']

    def __init__(self, *args, **kwargs):
        super(CreateSupplierForm, self).__init__(*args, **kwargs)

        self.fields['suppliercountry'].widget.attrs['class'] = 'form-control'


class CreateProductForm(ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.DecimalField(max_digits=8, widget=forms.TextInput(attrs={'class':'form-control'}))
    purchase_price = forms.DecimalField(max_digits=8, widget=forms.TextInput(attrs={'class':'form-control'}))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs = {'class':'form-control', 'placeholder': 'YYYY-MM-DD'}))
    quantity = forms.DecimalField(max_digits=8, widget=forms.TextInput(attrs={'class':'form-control'}))
    unit = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    bengali_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = Product
        fields = ['name', 'price', 'purchase_price', 'image', 'subcategory', 'supplier', 'ispopular', 'quantity', 'unit', 'purchase_date', 'bengali_name']

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['subcategory'].widget.attrs['class'] = 'form-control'
        self.fields['supplier'].widget.attrs['class'] = 'form-control'
        self.fields['ispopular'].widget.attrs['class'] = 'form-control'
        #self.fields['purchase_date'].widget.attrs['class'] = 'form-control'

class CreateProductOfferForm(ModelForm):
    discount_prcnt = forms.DecimalField(max_digits=8, widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs = {'class':'form-control', 'placeholder': 'YYYY-MM-DD'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs = {'class':'form-control', 'placeholder': 'YYYY-MM-DD'}))
    

    class Meta:
        model = ProductOffers
        fields = ['product', 'discount_prcnt', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(CreateProductOfferForm, self).__init__(*args, **kwargs)

        self.fields['product'].widget.attrs['class'] = 'form-control'
        #self.fields['start_date'].widget.attrs['class'] = 'form-control'
        #self.fields['end_date'].widget.attrs['class'] = 'form-control'

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserProfileForm(ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))    
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class OrderDeliveryForm(ModelForm):
    order = forms.ModelChoiceField(queryset=Order.objects.filter(order_status = 1))  
        
    class Meta:
        model = OrderDelivery
        fields = ['deliveryman', 'order','deliveryDate']

    def __init__(self, *args, **kwargs):
        super(OrderDeliveryForm, self).__init__(*args, **kwargs)

        self.fields['deliveryman'].widget.attrs['class'] = 'form-control'
        self.fields['order'].widget.attrs['class'] = 'form-control'
        
class CreateDelvmanForm(ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    contactnumber = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = DeliveryMan
        fields = ['name', 'contactnumber']


class CreateBannerForm(ModelForm):
    bannername = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    bannertext = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = BannerImages
        fields = ['bannername', 'bannerimage', 'bannertext', 'isactive']

    def __init__(self, *args, **kwargs):
        super(CreateBannerForm, self).__init__(*args, **kwargs)

        self.fields['bannerimage'].widget.attrs['class'] = 'form-control'
        self.fields['isactive'].widget.attrs['class'] = 'form-control'