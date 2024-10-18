from django.urls import path, include
from .import views 
from .api import api_views
from django.urls import path 
# serializer view__________________________________

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    #units management ...............................
    path("list_units",views.list_units,name="list_units"),
    path('add_unit/', views.add_unit, name='add_unit'),
    path('update_unit/<int:unit_id>/', views.update_unit, name='update_unit'),
    path("delete_unit/<int:pk>",views.delete_unit,name="delete_unit"),

    # vendor management ......................................

    path("add_vendor",views.add_vendor,name="add_vendor"),
    path("list_vendor",views.list_vendor,name="list_vendor"),

    # inventory management ....................................

    path("add_inventory",views.add_inventory,name="add_inventory"),
    path("edit_inventory/<int:pk>",views.edit_inventory,name="edit_inventory"),
    path("list_inventory",views.list_inventory,name="list_inventory"),
    path("add_purchase_order",views.add_purchase_order,name="add_purchase_order"),
    path("list_purchase_order",views.list_purchase_order,name="list_purchase_order"),
    path("purchase_order_invoice",views.purchase_order_invoice,name="purchase_order_invoice"),
    path("edit_purchase_order/<int:pk>",views.edit_purchase_order,name="edit_purchase_order"),
    # ###### purchases....................

    path("purchase",views.purchase,name="purchase"),
    path("add_purchase",views.add_purchase,name="add_purchase"),
    path("purchase_from_order/<int:order_id>",views.purchase_from_order,name="purchase_from_order"),
    path("edit_purchase/<int:pk>",views.edit_purchase,name="edit_purchase"),
    path("deletepurchase/<int:pk>",views.deletepurchase,name="deletepurchase"),
    
    #product management........................................

    path('add-category/', views.add_category, name='add_category'),
    path("list_category/",views.list_category,name="list_category"),
    path("list_products",views.list_products,name="list_products"),
    path("add_product",views.add_product,name="add_product"),

    path("disable_product/<int:pk>",views.disable_product,name="disable_product"),
    path("product_update/<int:product_id>",views.product_update,name="product_update"),
    path("incresse_product_stock/<int:product_id>",views.incresse_product_stock,name="incresse_product_stock"),
    path("delete_product/<int:pk>",views.delete_product,name="delete_product"),
    path('AddTax', views.AddTax, name='AddTax'),
    path('ListTax', views.ListTax, name='ListTax'),

    path("add_customer/<int:pk>",views.add_customer,name="add_customer"),
    path("list_customer",views.list_customer,name="list_customer"),

    

    #api datas

    path("product_list",api_views.product_list,name="product_list"),
    path("product_detail/<int:pk>",api_views.product_detail,name="product_detail"),
    path("product_add",api_views.product_add,name="product_add"),
    path("product_add_new",api_views.ProductListCreateView.as_view(),name="product_add_new"),

]

urlpatterns += [
    path('api/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
