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




# Create your views here.

def generate_serial_number():
    while True:
        random_number = random.randint(1000, 9999999)  # 5-digit random number
        order_number = f"SI-{random_number}"
        if not Order.objects.filter(invoice_number=order_number).exists():
            return order_number


@login_required(login_url='SignIn')
def CreateOrder(request):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(POS,pk = order.id)
     

@login_required(login_url='SignIn')
def POS(request,pk):
    customer = Customer.objects.all()
    order = Order.objects.get(id = pk)
    product = Product.objects.all()
    invoice = Order.objects.all().order_by('-id')[:6]
    salesmans = Staff.objects.filter(designation = "Sales Man")

    context = {
        "customer":customer,
        "order":order,
        'product':product,
        "invoice":invoice,
        "salesmans":salesmans
    }
    return render(request,'pos.html',context)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def search_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'search' in request.GET:
        query = request.GET.get('search', '')
        products = Product.objects.filter(name__icontains=query, status=True)
        product_list = [{
            'name': product.name,
            'price': product.price,
            'tax': product.tax_amount,
            'stock': product.stock,
        } for product in products]
        return JsonResponse({'products': product_list})
    return JsonResponse({'products': []})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            # Assuming you have a way to get the current order, e.g., through session or context
            order = Order.objects.get(id = order_id)
            order.customer = customer
            order.save()
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Customer.objects.get(id=customer_id)
            order.customer = customer
            order.save()
            customer_details_html = render_to_string('ajaxtemplates/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_salesman(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Staff.objects.get(id=customer_id)
            order.sales_man = customer
            order.save()
            customer_details_html = render_to_string('ajaxtemplates/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})



@login_required(login_url='SignIn')
def AddItemsToorder(request):
     return redirect('POS',pk=10)



@login_required(login_url='SignIn')
def list_sale(request):
    order = Order.objects.all().order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale.html',context)


@login_required(login_url='SignIn')
def list_sale_pending(request):
    order = Order.objects.filter(payment_status1 = "UNPAID" ).order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale-pending.html',context)

@login_required(login_url='SignIn')
def list_sale_partial(request):
    order = Order.objects.filter(payment_status1 = "PARTIALLY" ).order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale-partial.html',context)

def delete_invoice(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale")

def delete_invoice_partial(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale_partial")

def delete_invoice_pending(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale_pending")



@login_required(login_url='SignIn')
@csrf_exempt
def add_order_item(request,pk):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
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
            
            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
            return JsonResponse({"success": True, "html": order_items_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_item(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        if order.save_status == False:
            item_id = request.POST.get('item_id')
            unit_price = float(request.POST.get('unit_price', 0))
            discount = float(request.POST.get('discount', 0))
            quantity = int(request.POST.get('quantity', 1))

            # Find the OrderItem to update
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)

            # Update the OrderItem fields
            order_item.unit_price = unit_price
            order_item.discount = discount
            order_item.quantity = quantity
            order_item.save()  # This will also update the total_price based on save() logic
        try:
        # Update order totals
            order.update_totals()
            order.calculate_balance()

        # Prepare the updated data to return as a JSON response
            return JsonResponse({
                'success': True,
                'total_amount': order.total_amount,
                'balance_amount': order.balance_amount,
                'payment_status': order.payment_status1
            })
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required(login_url='SignIn')
@csrf_exempt
def update_order_item_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        try:
            order_item = OrderItem.objects.get(id=item_id)
            order = order_item.order
            order_item.delete()

            # Update order totals
            order_item.order.update_totals()

            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
            return JsonResponse({"success": True, "html": order_items_html})
        except OrderItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def update_order_payment(request, order_id):
    if request.method == 'POST':
        payed_amount = float(request.POST.get('payed_amount'))
        discount = float(request.POST.get('discount'))
        
        try:
            order = Order.objects.get(id=order_id)    
            order.payed_amount = payed_amount
            order.discount = discount
            order.balance_amount = order.total_amount - payed_amount

            
                        
            if payed_amount == 0:
                order.payment_status1 = 'UNPAID'
            elif payed_amount >= order.total_amount:
                order.payment_status1 = 'PAID'
            else:
                order.payment_status1 = 'PARTIALLY'
                
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='SignIn')
def save_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    previous_paid_amount = order.payed_amount
    # Save the order and calculate totals
    order.update_totals()
    order.calculate_balance()
    new_payedamount =  order.payed_amount - previous_paid_amount
    print(new_payedamount,"----------------------------------------")
    if Income.objects.filter(bill_number = order.invoice_number).exists():
        expense = Income.objects.filter(bill_number = order.invoice_number)
        total = 0
        
        for ex in expense:
            total = total + ex.amount
        
        amount = order.payed_amount - total
        if amount > 0:
            expense = Income(
                perticulers = f"Amount Against order {order.invoice_number}",
                amount =  amount,
                bill_number = order.invoice_number
            
            )
        
            expense.save() 
    else:
        if order.payed_amount > 0:
            expense = Income(
                    perticulers = f"Amount Against order {order.invoice_number}",
                    amount =  order.payed_amount,
                    bill_number = order.invoice_number
                
                )
            
            expense.save()   
    
    # Adjust stock
    try:
        if order.save_status == False:
            order.adjust_stock()  # Deduct the stock
            order.save_status = True
            order.save()
            return redirect("POS",pk = order_id)

        else:
            messages.info(request,"Cannot be save it is alredy saved the item")

            return redirect("POS",pk = order_id)
    except ValueError as e:
        messages.info(request,"Not Enough stock...")
        return redirect("POS",pk = order_id)
    
from io import BytesIO

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from num2words import num2words

@login_required(login_url='SignIn')
def invoice(request,pk):
    order = get_object_or_404(Order, id=pk)
    
    # Save the order and calculate totals
    order.update_totals()
    order.calculate_balance()
    order_items = order.orderitem_set.all()
    # Adjust stock
    try:
        if order.save_status == False:
            order.adjust_stock()  # Deduct the stock
            order.save_status = True
            order.save()

        if Income.objects.filter(bill_number = order.invoice_number).exists():
            expense = Income.objects.filter(bill_number = order.invoice_number)
            total = 0
            
            for ex in expense:
                total = total + ex.amount
            
            amount = order.payed_amount - total
            if amount > 0:
                expense = Income(
                    perticulers = f"Amount Against order {order.invoice_number}",
                    amount =  amount,
                    bill_number = order.invoice_number
                
                )
            
                expense.save() 
        else:
            expense = Income(
                    perticulers = f"Amount Against order {order.invoice_number}",
                    amount =  order.payed_amount,
                    bill_number = order.invoice_number
                
                )
            
            expense.save()

        # order = Order.objects.get(pk=pk)
        # context = {
        #     'order': order
        # }
        # pdf = render_to_pdf('invoice_template.html', context)
        # if pdf:
        #     return HttpResponse(pdf, content_type='application/pdf')
        # return HttpResponse("Error generating PDF")
        context = {
        "order": order,
        "order_items": order_items,
        "total_in_words": num2words(order.total_amount).title()
        }
        return render(request,'invoice_template.html',context)

      # Get all OrderItems for the specific order
    except ValueError as e:
        messages.info(request,"Not Enough stock...")
        return redirect("POS",pk = pk)

    


# @csrf_exempt
# def update_order_payment(request, order_id):
#     if request.method == 'POST':
#         order = Order.objects.get(id=order_id)
#         payed_amount = float(request.POST.get('payed_amount', 0))
#         discount = float(request.POST.get('discount', 0))

#         # Update the order
#         order.payed_amount = payed_amount
#         order.discount = discount
#         order.total_amount -= order.discount
#         order.calculate_balance()
        
#          # Render the order items table
#         order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
#         return JsonResponse({"success": True, "html": order_items_html})
        
#     return JsonResponse({"success": False, "error": "Invalid request"})


def AddDiscount(request):
    return render(request,"add-discount.html")


def Listdiscount(request):
    return render(request,"list-discount.html")


