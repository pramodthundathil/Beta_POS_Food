
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import ProductForm, InventoryStockForm, PurchaseOrderForm, PurchaseForm, VendorForm, CustomerForm
from django.http import HttpResponse
from POS.models import *
from django.contrib.auth.decorators import login_required
from Finance.models import Income, Expence



# Create your views here.

# units add updating funtions#####################################################

def list_units(request):
    units = Units.objects.all()
    return render(request,"list-units.html",{"units":units})
# View for adding a unit

def add_unit(request):
    if request.method == 'POST':
        unit_name = request.POST['unit']
        description = request.POST['description']
        new_unit = Units(unit=unit_name, description=description)
        new_unit.save()
        messages.success(request, 'Unit added successfully!')
        return redirect('list_units')  # Assume you have a unit list page
    return render(request, 'add-units.html')


# View for updating a unit
def update_unit(request, unit_id):
    unit = get_object_or_404(Units, pk=unit_id)
    if request.method == 'POST':
        unit.unit = request.POST['unit']
        unit.description = request.POST['description']
        unit.save()
        messages.success(request, 'Unit updated successfully!')
        return redirect('update_unit', unit_id = unit_id)  # Redirect to unit list after update
    return render(request, 'update-units.html', {'unit': unit})


def delete_unit(request,pk):
    Units.objects.get(id = pk).delete()
    messages.error(request,"unit deleted")
    return redirect("list_units")
########################################## vendor management ############################################
# 

@login_required(login_url='SignIn')
def add_vendor(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gst_number = request.POST['gst_number']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        contact_info = request.POST.get('contact_info', '')
        supply_product = request.POST['supply_product']

        vendor = Vendor(
            name=name,
            email=email,
            phone_number=phone,
            gst_number=gst_number,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            contact_info=contact_info,
            supply_product=supply_product,
        )
        vendor.save()
        messages.success(request, 'Vendor added successfully')
        return redirect('list_vendor')
    return render(request,"add-vendor.html") 

@login_required(login_url='SignIn')
def list_vendor(request):
    vendor = Vendor.objects.all()

    context = {
        "vendor":vendor
    }
    return render(request,'list-vendors.html',context)


@login_required(login_url='SignIn')
def update_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('list_vendor')  # Redirect to a list or relevant page
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_update.html', {'form': form})


@login_required(login_url='SignIn')
def delete_vendor(request,pk):
    vendor = Vendor.objects.get(id = pk)
    vendor.delete()
    messages.info(request,"vendor deleted....")
    return redirect("list_vendor")


############################ Inventory Management #################################


@login_required(login_url='SignIn')
def add_inventory(request):
    if request.method == "POST":
        form = InventoryStockForm(request.POST)
        if form.is_valid():
            inventory = form.save()
            inventory.save()  # Save the inventory stock to the database
            messages.success(request, 'Inventory added successfully')
            return redirect('list_inventory')
        else:
            # If form is invalid, render the same page with error messages
            messages.error(request, 'Error adding inventory. Please check the form and try again.')
            return render(request, 'inventory/add-inventory.html', {'forms': form})
    else:
        form = InventoryStockForm()
    return render(request, 'inventory/add-inventory.html', {'forms': form})



@login_required(login_url='SignIn')
def edit_inventory(request,pk):
    inventory  = get_object_or_404(InventoryStock,id = pk)
    purchase = Purchase.objects.filter(purchase_item = inventory)
    form = InventoryStockForm(instance=inventory)
    if request.method == "POST":
        form = InventoryStockForm(request.POST,instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory Updated successfully')
            return redirect('list_inventory')  # Adjust this based on your URLs
        else:
            messages.error(request, 'Failed to add Purchase Order. Please check the details.')
    
    context = {
        'form': form,
        "inventory":inventory,
        "purchase":purchase
    }
    return render(request, 'inventory/update-inventory.html', context)




@login_required(login_url='SignIn')
def list_inventory(request):
    product = InventoryStock.objects.all()
    context = {
        "product":product
    }
    return render(request,'inventory/list-inventory.html',context)

@login_required(login_url='SignIn')
def delete_inventory(request,pk):
    inventory = get_object_or_404(InventoryStock,id = pk)
    inventory.delete()
    messages.success(request,"Inventory Deleted successfully....")
    return redirect(list_inventory)


@login_required(login_url='SignIn')
def add_purchase_order(request):
    form = PurchaseOrderForm()
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase Order added successfully')
            return redirect('list_purchase_order')  # Adjust this based on your URLs
        else:
            messages.error(request, 'Failed to add Purchase Order. Please check the details.')
    
    context = {
        'form': form
    }
    return render(request, 'inventory/add-purchase-order.html', context)



@login_required(login_url='SignIn')
def list_purchase_order(request):
    order = PurchaseOrder.objects.all()
    context = {
        "order":order
    }
    return render(request,'inventory/list-purchase-order.html',context)


@login_required(login_url='SignIn')
def edit_purchase_order(request,pk):
    purchase_order  = get_object_or_404(PurchaseOrder,id = pk)

    form = PurchaseOrderForm(instance=purchase_order)
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST,instance=purchase_order)
        if form.is_valid():
            form.save()


            messages.success(request, 'Purchase Order Updated successfully')
            return redirect('list_purchase_order')  # Adjust this based on your URLs
        else:
            messages.error(request, 'Failed to add Purchase Order. Please check the details.')
    
    context = {
        'form': form,
        "purchase_order":purchase_order
    }
    return render(request, 'inventory/update-purchase-order.html', context)


@login_required(login_url='SignIn')
def purchase_order_invoice(request):
    return render(request,"purchase_order.html")


@login_required(login_url='SignIn')
def purchase_from_order(request, order_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=order_id)
    purchase_order.create_purchase()
    purchase_order.order_status = "Closed"
    purchase_order.save()
    messages.info(request,"Purchase Created....")


    return redirect("purchase")

@login_required(login_url='SignIn')
def purchase(request):
    purchase = Purchase.objects.all()
    context = {
       "purchase":purchase 
    }
    return render(request,'purchase.html',context)
import datetime

@login_required(login_url='SignIn')
def edit_purchase(request,pk):
    purchase  = get_object_or_404(Purchase,id = pk)
    paid_amount = purchase.paid_amount
    form = PurchaseForm(instance=purchase)
    if request.method == "POST":
        form = PurchaseForm(request.POST,instance=purchase)
        if form.is_valid():
            new_purchase = form.save()
            new_purchase.save()
            now_paid = new_purchase.paid_amount - paid_amount
            if now_paid != 0:
                expence = Expence(
                    perticulers = f"Amount Paid to  {new_purchase.supplier} towerd purchase {new_purchase.purchase_bill_number}",
                    date = datetime.datetime.now(),
                    amount = now_paid
                )
                expence.save()

            messages.success(request, 'Purchase Updated successfully')
            return redirect('purchase')  # Adjust this based on your URLs
        else:
            messages.error(request, 'Failed to add Purchase Order. Please check the details.')
    
    context = {
        'form': form,
        "purchase":purchase
    }
    return render(request, 'inventory/update-purchase.html', context)


@login_required(login_url='SignIn')
def deletepurchase(request,pk):
    purchase  = get_object_or_404(Purchase,id = pk)
    purchase.delete()
    messages.error(request, 'Purchase Deleted.....')
    return redirect("purchase")


@login_required(login_url='SignIn')
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            item = form.save()
            item.save()
            stock = item.purchase_item
            if item.paid_amount > 0:
                expence = Expence(
                    perticulers = f"Amount Paid to  {item.supplier} towerd purchase {item.purchase_bill_number}",
                    date = datetime.datetime.now(),
                    amount = item.paid_amount
                )
                expence.save()

            if not stock:
                raise ValueError("No inventory item selected for purchase.")

            # Adjust quantity based on the units in PurchaseOrder and InventoryStock
            purchase_quantity = item.quantity

            # If stock is in grams but purchase is in kilograms, convert purchase to grams
            if stock.unit == 'g' and item.unit == 'kg':
                purchase_quantity *= 1000  # Convert kilograms to grams

            # If stock is in kilograms but purchase is in grams, convert purchase to kilograms
            elif stock.unit == 'kg' and item.unit == 'g':
                purchase_quantity /= 1000  # Convert grams to kilograms

            stock.product_stock += purchase_quantity
            stock.last_purchase_date = item.bill_date
            stock.last_purchase_amount = item.amount
            stock.save()

            return redirect('purchase')  
    else:
        form = PurchaseForm()
    return render(request,'inventory/add-purchase.html',{"form":form})


############################ Product Management #################################


@login_required(login_url='SignIn')
def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        active = 'active' in request.POST

        category = ProductCategory(
            name=name,
            active=active,
        )
        category.save()
        messages.success(request, 'Category added successfully')
        return redirect('list_category')

    return render(request, 'add-category.html')


@login_required(login_url='SignIn')
def list_category(request):
    category = ProductCategory.objects.all()
    context = {
        "category":category
    }
    return render(request,"list-category.html",context)

@login_required(login_url='SignIn')
def delete_category(request,pk):
    cat =get_object_or_404(ProductCategory,id = pk)
    cat.delete()
    messages.success(request,"Category Deleted...")
    return redirect("list_category")



@login_required(login_url='SignIn')
def list_products(request):
    product = Product.objects.all()
    context = {
        "product":product
    }
    return render(request,'list-product.html',context)


@login_required(login_url='SignIn')
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')  # Redirect to the product list or another page
    
    context = {
        "form":form

    }
    return render(request,'add-product.html',context)

@login_required(login_url='SignIn')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    food_category = ProductCategory.objects.all()
    tax = Tax.objects.all()
    form = ProductForm(instance=Product)


    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.tax = request.POST['tax']
        # product.tax_value_id = request.POST['tax_value']
        product.description = request.POST['description']

        # Handle image upload if a new image is provided
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        # Save updated product
        product.save()

        messages.success(request, 'Product updated successfully!')
        return redirect('product_update', product_id = product_id)  # Redirect to product list or any desired page

    context = {
        'product': product,
        'food_category': food_category,
        'tax': tax,
    }
    return render(request, 'update-product.html', context)



@login_required(login_url='SignIn')
def incresse_product_stock(request, product_id):
    if request.method == 'POST':
        # Get the product and inventory
        product = get_object_or_404(Product, id=product_id)
        inventory = product.inventory  # Get the linked inventory
        
        try:
            # Fetch the number of units added from the form
            units_to_add = float(request.POST['stock'])

            # Calculate the total increase in stock based on product's unit_quantity
            total_increase = units_to_add * product.unit_quantity  # For example, 100g * 10 = 1000g
            
            # Convert the total increase to kilograms if inventory is in kg
            if inventory.unit == 'kg':
                total_increase_kg = total_increase / 1000  # Convert grams to kilograms
                inventory.reduce_stock(total_increase_kg)  # Reduce inventory stock by this amount
            else:
                # If the inventory unit is in grams, reduce directly
                inventory.reduce_stock(total_increase)
            
            # Increase the product stock
            product.Number_of_stock += int(units_to_add)
            product.save()
            inventory.save()
            
            messages.success(request, f"Successfully increased stock for {product.name} by {units_to_add} units.")
        except (ValueError, KeyError):
            messages.error(request, "Invalid input. Please enter a valid stock number.")

    return redirect('product_update', product_id=product.id)


@login_required(login_url='SignIn')
def delete_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    try:
        product.image.delete()
    except:
        pass
    product.delete()
    messages.success(request,"Product Deleted")
    return redirect("list_products")



@login_required(login_url='SignIn')
def disable_product(request,pk):
    try:
        product = Product.objects.get(id = pk)
        if product.status == True:
            product.status = False
        else:
            product.status = True
        product.save()
    except:
        messages.info(request,"Product is not accessible")
    return redirect("list_products")


@login_required(login_url='SignIn')
def AddTax(request):
    if request.method == "POST":
        name = request.POST.get('name')
        tax_rate = request.POST.get('tax')
        tax = Tax.objects.create(tax_name = name,tax_percentage = tax_rate )
        tax.save()
        messages.success(request,'Tax Value Added Success')
        return redirect("ListTax")
    return render(request,"add-tax-slab.html")

@login_required(login_url='SignIn')
def ListTax(request):
    tax = Tax.objects.all()
    context = {
        "tax":tax
    }
    return render(request,"list-tax.html",context)




@login_required(login_url='SignIn')
def add_customer(request,pk):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gst = request.POST.get('gst')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        contact_info = request.POST.get('contact_info')

        # Creating a new Customer object
        customer = Customer(
            name=name,
            phone=phone,
            email=email,
            gst_number=gst,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            contact_info=contact_info
        )

        try:
            # Saving the object to the database
            customer.save()
            messages.info(request, "customer addedd.............")
            order = Order.objects.get(id = pk)
            order.customer = customer
            order.save()
            return redirect("POS",pk = pk)

        # Redirect to a success page or the customer's detail page
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return redirect("POS")


@login_required(login_url='SignIn')
def list_customer(request):
    customer = Customer.objects.all()
    context = {
        "customer":customer
    }
    return render(request,"list-customers.html",context)



@login_required(login_url='SignIn')
def add_customers(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Customer Added.....")
            return redirect('list_customer')  # Redirect to the customer list or relevant page
    else:
        form = CustomerForm()
    return render(request, 'add-customers.html', {'form': form})

# Update customer
@login_required(login_url='SignIn')
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,"Customer Updated.....")

            return redirect('list_customer')  # Redirect to the customer list or relevant page
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'form': form})

# Delete customer
@login_required(login_url='SignIn')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    customer.delete()
    messages.success(request,"Customer deleted.....")

    return redirect('list_customer')  # Redirect to the customer list after deletion
    


# Purchases.................................................









