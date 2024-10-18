from django.urls import path 
from .import views  



urlpatterns = [

    path("POS/<int:pk>",views.POS,name="POS"),
    path("search_product",views.search_product,name="search_product"),
    path("CreateOrder",views.CreateOrder,name="CreateOrder"),
    path("list_sale",views.list_sale,name="list_sale"),
    path("update_order",views.update_order,name="update_order"),
    path('update_order_customer',views.update_order_customer, name='update_order_customer'),
    path('add_order_item/<int:pk>', views.add_order_item, name='add_order_item'),
    path('update_order_item_quantity', views.update_order_item_quantity, name='update_order_item_quantity'),
    path('update_order_payment/<int:order_id>/', views.update_order_payment, name='update_order_payment'),
    path("invoice/<int:pk>",views.invoice,name="invoice"),
    path('update_order_payment/<int:order_id>/', views.update_order_payment, name='update_order_payment'),
    path("AddDiscount",views.AddDiscount,name="AddDiscount"),
    path("Listdiscount",views.Listdiscount,name="Listdiscount"),
    path('update_order_item/<int:order_id>/', views.update_order_item, name='update_order_item'),
    path("save_order/<int:order_id>",views.save_order,name="order_id")

    

    
]