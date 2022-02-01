from django.urls import path
from . import views

from .views import change_password

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('shop', views.shop, name = 'shop'),
    path('cart', views.cart, name= 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('update_item/', views.updateItem, name = 'update_item'),
    path('process_order/', views.processOrder, name = 'process_order'),

    path('subcategories/<str:varID>', views.subcategories, name = 'subcategories'),
    path('subcategoryviews/<str:varID>/<str:varName>', views.subcategoryviews, name = 'subcategoryviews'),
    path('productsview/<str:varID>/<str:varName>', views.productviews, name = 'productsview'),
    path('productdetails/<str:prodID>', views.productdetails, name = 'productdetails'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('userpanel', views.userpanel, name='userpanel'),
    path('orderdetails/<str:varOrder>', views.orderdetails, name= 'orderdetails'),

    path('changepassword', change_password.as_view(template_name='store/changepassword.html'), name = 'changepassword'),

    # Bangla
    path('homebangla', views.homeBangla, name = 'homebangla'),

    # Search
    path('searchresult', views.search, name = 'searchresult'),

    # Testing
    path('test', views.test, name = 'test'),

    path('privacypolicy', views.privacypolicy, name = 'privacypolicy'),
    path('refundpolicy', views.refundpolicy, name = 'refundpolicy'),
    path('termsandconditions', views.termsandconditions, name = 'termsandconditions'),
]
