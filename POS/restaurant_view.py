from django.shortcuts import render, redirect, get_object_or_404
from Inventory.models import *
from django.http import JsonResponse
from datetime import datetime
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Finance.models import Income, Expence
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from Inventory.forms import ProductForm
from django.db import transaction


def POS_REST(request, pk):
    order = get_object_or_404(Order, id = pk )
    products = Product.objects.all().order_by("-id")
    category = ProductCategory.objects.all()
    order_items  = OrderItem.objects.filter(order = order)

    context = {
        "products":products,
        "category":category,
        "order":order,
        "order_items":order_items
    }
    return render(request,'restaurant/pos-rest-style.html',context)

@csrf_exempt
def search_product_pos(request):
    if request.method == "POST":
        val = request.POST.get("itemId")
        print(val, "---------------------------------------------------------------")
        
        # Check if val is not None or empty
        if not val:
            return JsonResponse({"success": True, "error": "No search term provided"})
        
        try:
            # Perform the query with the search term
            products = Product.objects.filter(name__contains=val)
            
            customer_details_html = render_to_string('ajaxtemplates/product-in-pos.html', {'products': products})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def search_product_pos_all(request):
    if request.method == "POST":
        # val = request.POST.get("itemId")
        # print(val, "---------------------------------------------------------------")
        
        # # Check if val is not None or empty
        # if not val:
        #     return JsonResponse({"success": True, "error": "No search term provided"})
        
        try:
            # Perform the query with the search term
            products = Product.objects.all()
            
            customer_details_html = render_to_string('ajaxtemplates/product-in-pos.html', {'products': products})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})


def generate_serial_number():
    with transaction.atomic():
        # Get the latest order based on ID to find the last invoice number
        last_order = Order.objects.order_by('-id').first()
        
        if last_order and last_order.invoice_number.startswith("SI-"):
            # Extract the numeric part, increment it, and format it with leading zeros
            last_number = int(last_order.invoice_number.split("-")[1])
            new_number = str(last_number + 1).zfill(5)  # Ensures it's 5 digits
        else:
            # Start from "SI-00001" if no previous order exists
            new_number = "00001"
        
        return f"SI-{new_number}"

@login_required(login_url='SignIn')
def CreateOrder_Rest(request):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(POS_REST,pk = order.id)


@login_required(login_url='SignIn')
@csrf_exempt
def add_order_item_rest_pos(request,pk):
    if request.method == 'POST':
        product_id = request.POST.get('itemid')
        print(product_id,")))))))))))))))))))))))))))))))))))))))))))")
        try:
            order = Order.objects.get(id=pk)
            if order.save_status == True:
                return JsonResponse({"success": False, "error": "Cannot Be added New Item to This order"})
            product = Product.objects.get(id=product_id)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                order_item.quantity += 1
                order_item.save()
            
            # Update order totals
            order.update_totals()
            order_items = OrderItem.objects.filter(order = order)
            
            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/invoice-table-pos.html', {'order': order,"order_items":order_items})
            return JsonResponse({"success": True, "html": order_items_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})





@login_required(login_url='SignIn')
@csrf_exempt
def delete_item_rest_pos(request,pk):
    if request.method == 'POST':
        product_id = request.POST.get('itemid')
        print(product_id,")))))))))))))))))))))))))))))))))))))))))))")
        try:
            order = Order.objects.get(id=pk)
            if order.save_status == True:
                return JsonResponse({"success": False, "error": "Cannot Be added New Item to This order"})
            order_item = OrderItem.objects.get(id=product_id)
            order_item.delete()
            
            # Update order totals
            order.update_totals()
            order_items = OrderItem.objects.filter(order = order)
            
            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/invoice-table-pos.html', {'order': order,"order_items":order_items})
            return JsonResponse({"success": True, "html": order_items_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})