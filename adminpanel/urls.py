from django.urls import path
from adminpanel import views

urlpatterns = [
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('adminpanel', views.dashboard, name = 'adminpanel'),

    path('region', views.region, name = 'region'),
    path('createregion', views.createregion, name = 'createregion'),
    path('updateregion/<rgnID>', views.updateregion, name = 'updateregion'),

    path('area', views.area, name = 'area'),
    path('createarea', views.createarea, name = 'createarea'),
    path('updatearea/<areaID>', views.updatearea, name = 'updatearea'),

    path('category', views.category, name = 'category'),
    path('createcategory', views.createcategory, name = 'createcategory'),
    path('updatecategory/<categoryID>', views.updatecategory, name = 'updatecategory'),

    path('subcategory', views.subcategory, name = 'subcategory'),
    path('createsubcategory', views.createsubcategory, name = 'createsubcategory'),
    path('updatesubcategory/<subcategoryID>', views.updatesubcategory, name = 'updatesubcategory'),

    path('supplier', views.supplier, name = 'supplier'),
    path('createsupplier', views.createsupplier, name = 'createsupplier'),
    path('updatesupplier/<supplierID>', views.updatesupplier, name = 'updatesupplier'),

    path('customer', views.customer, name = 'customer'),

    path('product', views.product, name = 'product'),
    path('createproduct', views.createproduct, name = 'createproduct'),
    path('updateproduct/<productID>', views.updateproduct, name = 'updateproduct'),

    path('productoffers', views.productoffers, name = 'productoffers'),
    path('createproductoffers', views.createproductoffer, name = 'createproductoffers'),
    path('updateproductoffer/<productID>', views.updateproductoffer, name = 'updateproductoffer'),

    path('deliveryman', views.deliveryman, name = 'deliveryman'),
    path('createdeliveryman', views.createdeliveryman, name = 'createdeliveryman'),
    path('updatedeliveryman/<ID>', views.updatedeliveryman, name = 'updatedeliveryman'),

    path('banner', views.bannerimage, name = 'banner'),
    path('createbanner', views.createbanner, name = 'createbanner'),
    path('updatebanner/<ID>', views.updatebanner, name = 'updatebanner'),

    path('delivery', views.deliverydetails, name='delivery'),


    path('login', views.user_login, name = 'login'),
    path('logout', views.logout_user, name= 'logout'),
    path('register', views.userregistration, name = 'register'),

    # REPORTS
    path('productstock', views.productstockrpt, name = 'productstock'),
    path('resultdata', views.resultsData, name = 'resultdata'),
    path('revenuedata', views.revenueData, name = 'revenuedata'),
    path('pie-chart/', views.pieresultsData, name = 'pie-chart'),

    path('exportdata', views.exporttoexcel, name = 'exportdata'),

]