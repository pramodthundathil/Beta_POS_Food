from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import *
from POS.models import Order
from .forms import *
from django.shortcuts import render
from django.utils.timezone import now
from .models import Income, Expence
from itertools import chain
from operator import attrgetter
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required 
from Inventory.models import Purchase

@login_required(login_url="SignIn")
def income(request):
    income = Income.objects.all().order_by("-id")

    context = {
        "income":income
    }
    return render(request,"finance/income.html",context)


@login_required(login_url="SignIn")
def add_income(request):
    form = IncomeForm()

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Income record added successfully.")
            return redirect('income')  # Redirect to the same page or another view
 
    return render(request, 'finance/add-income.html', {'form': form})

@login_required(login_url="SignIn")
def update_income(request,pk):
    income  = get_object_or_404(Income,id = pk)
    form = IncomeForm(instance=income)

    if request.method == 'POST':
        form = IncomeForm(request.POST,instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Income Update successfully.")
            return redirect('income')  # Redirect to the same page or another view
 
    return render(request, 'finance/update-income.html', {'form': form})


@login_required(login_url="SignIn")
def delete_income(request,pk):
    income = get_object_or_404(Income,id = pk)
    income.delete()
    messages.success(request,"Income deleted success.....")
    return redirect("income")



@login_required(login_url="SignIn")
def expence(request):
    ex = Expence.objects.all().order_by("-id")
    context = {
        "expence":ex
    }
    return render(request,"finance/expence.html",context)


@login_required(login_url="SignIn")
def delete_expense(request,pk):
    expense = get_object_or_404(Expence,id = pk)
    expense.delete()
    messages.success(request,"Expense deleted success.....")
    return redirect("expence")


# View for adding expense
def add_expense(request):
    if request.method == 'POST':
        form = ExpenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense record added successfully.")
            return redirect('expence')  # Redirect to the same page or another view
    else:
        form = ExpenceForm()
    return render(request, 'finance/add-expense.html', {'form': form})

def update_expense(request,pk):
    expense = get_object_or_404(Expence, id = pk)
    if request.method == 'POST':
        form = ExpenceForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense record added successfully.")
            return redirect('expence')  # Redirect to the same page or another view
    else:
        form = ExpenceForm(instance=expense)
    return render(request, 'finance/update-expense.html', {'form': form})




def balance_sheet(request):
    # Get the current date
    current_date = now()
    month = current_date.strftime("%B")

    # Filter income and expenses for the current month
    income_list = Income.objects.filter(date__year=current_date.year, date__month=current_date.month)
    expense_list = Expence.objects.filter(date__year=current_date.year, date__month=current_date.month)

    # Convert to lists with 'type' field indicating credit (income) or debit (expense)
    income_data = [{'type': 'credit', 'date': income.date, 'perticulers': income.perticulers, 'amount': income.amount} for income in income_list]
    expense_data = [{'type': 'debit', 'date': expense.date, 'perticulers': expense.perticulers, 'amount': expense.amount} for expense in expense_list]

    # Combine both lists and order by date
    combined_list = sorted(
        chain(income_data, expense_data),
        key=lambda x: x['date']
    )

    # Calculate totals
    total_income = sum(income['amount'] for income in income_data)
    total_expense = sum(expense['amount'] for expense in expense_data)

    # Pass data to the template
    return render(request, "finance/balancesheet.html", {
        'combined_list': combined_list,
        'total_income': total_income,
        'total_expense': total_expense,
        "month":month
    })


from django.shortcuts import render
from django.utils.timezone import now
from .models import Income, Expence
from itertools import chain
from operator import attrgetter

def balance_sheet_selected(request):
    if request.method == "POST":
    # Get start and end dates from form submission (default to current month if not provided)
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')

    if start_date and end_date:
        # Filter by selected date range
        income_list = Income.objects.filter(date__range=[start_date, end_date])
        expense_list = Expence.objects.filter(date__range=[start_date, end_date])
    else:
        # Default to current month if no dates are provided
        current_date = now()
        income_list = Income.objects.filter(date__year=current_date.year, date__month=current_date.month)
        expense_list = Expence.objects.filter(date__year=current_date.year, date__month=current_date.month)

    # Convert to lists with 'type' field indicating credit (income) or debit (expense)
    income_data = [{'type': 'credit', 'date': income.date, 'perticulers': income.perticulers, 'amount': income.amount} for income in income_list]
    expense_data = [{'type': 'debit', 'date': expense.date, 'perticulers': expense.perticulers, 'amount': expense.amount} for expense in expense_list]

    # Combine both lists and order by date
    combined_list = sorted(
        chain(income_data, expense_data),
        key=lambda x: x['date']
    )

    # Calculate totals
    total_income = sum(income['amount'] for income in income_data)
    total_expense = sum(expense['amount'] for expense in expense_data)

    # Pass data to the template
    return render(request, "finance/balancesheet.html", {
        'combined_list': combined_list,
        'total_income': total_income,
        'total_expense': total_expense,
        'start_date': start_date,
        'end_date': end_date,
        "month": f"{start_date} to {end_date}"
    })



# in finance i am desided to add report generation through this application 
# below methods are the report generation 
from Inventory.models import Customer, Product
from Home.models import Staff


def reports(request):
    customer = Customer.objects.all()
    product = Product.objects.all()
    salesman  = Staff.objects.filter(designation = "Sales Man")

    context = {
        "customer":customer,
        "product":product,
        "salesman":salesman
    }
    return render(request,"reports.html",context)


from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
import pandas as pd
from openpyxl.styles import Border, Side


def expence_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']

        # Filter expenses based on the date range
        expenses = Expence.objects.filter(date__range=[start_date, end_date])

        # Convert expenses to a Pandas DataFrame
        data = {
            'Date': [exp.date for exp in expenses],
            'Particulars': [exp.perticulers for exp in expenses],
            'Amount': [exp.amount for exp in expenses],
            'Other': [exp.other for exp in expenses],
        }
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="expense_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response


def expence_report_pdf(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']

        # Filter expenses based on the date range
        expenses = Expence.objects.filter(date__range=[start_date, end_date])

        # Render the data to a template
        template_path = 'expence_report_pdf.html'
        context = {
            'expenses': expenses,
            'start_date': start_date,
            'end_date': end_date,
        }
        html = render_to_string(template_path, context)

        # Create a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="expense_report_{start_date}_to_{end_date}.pdf"'

        # Create PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        # If there's an error, show it in the response
        if pisa_status.err:
            return HttpResponse('We had some errors with the report')

        return response


def income_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']

        # Filter expenses based on the date range
        expenses = Income.objects.filter(date__range=[start_date, end_date])

        # Convert expenses to a Pandas DataFrame
        data = {
            'Date': [exp.date for exp in expenses],
            'Particulars': [exp.perticulers for exp in expenses],
            'Amount': [exp.amount for exp in expenses],
            'Other': [exp.other for exp in expenses],
        }
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Income_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response


def income_report_pdf(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']

        # Filter expenses based on the date range
        income = Income.objects.filter(date__range=[start_date, end_date])

        # Render the data to a template
        template_path = 'income_report_pdf.html'
        context = {
            'income': income,
            'start_date': start_date,
            'end_date': end_date,
        }
        html = render_to_string(template_path, context)

        # Create a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="income_report_{start_date}_to_{end_date}.pdf"'

        # Create PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        # If there's an error, show it in the response
        if pisa_status.err:
            return HttpResponse('We had some errors with the report')

        return response
    



def sale_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        category = request.POST.get("category")

        # Filter orders based on the date range
        if not category:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date], payment_status1=category)

        # Prepare data for the report
        data = {
            'Date': [order.order_date.replace(tzinfo=None) for order in orders],
            'Invoice Number': [order.invoice_number for order in orders],
            # Concatenate the product names from OrderItem for each order
            'Products': [', '.join([item.product.name for item in order.orderitem_set.all()]) for order in orders],
            'Amount': [order.total_amount for order in orders],
            'Paid Amount': [order.payed_amount for order in orders],
            'Balance Amount': [order.balance_amount for order in orders],
            'Payment Status': [order.payment_status1 for order in orders],
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)

        # Calculate totals
        totals = {
            'Date': 'Total',  # Label for the total row
            'Invoice Number': '',
            'Products': '',
            'Amount': df['Amount'].sum(),
            'Paid Amount': df['Paid Amount'].sum(),
            'Balance Amount': df['Balance Amount'].sum(),
            'Payment Status': '',
        }

        # Append total row to the DataFrame
        totals_df = pd.DataFrame([totals])
        df = pd.concat([df, totals_df], ignore_index=True)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')
        

        return response

    
def sale_report_pdf(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        category = request.POST.get("category")

        # Filter orders based on the date range
        if not category:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date], payment_status1=category)

        # Calculate totals
        total_amount = sum(order.total_amount for order in orders)
        total_paid = sum(order.payed_amount for order in orders)
        total_balance = sum(order.balance_amount for order in orders)

        # Prepare the context for the PDF template
        context = {
            'orders': orders,
            'start_date': start_date,
            'end_date': end_date,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_balance': total_balance,
        }

        # Load the HTML template
        template = get_template('sale_report_pdf.html')
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.pdf"'

        # Create the PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse(f'We had some errors: {pisa_status.err}')
        return response
    

def sale_report_excel_sales_man(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        sales_man = request.POST.get("sales_man")
        
        # Filter orders based on the date range and optionally by category (payment status)
        if not sales_man:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date], sales_man_id=sales_man)

        # Prepare data classified by Salesman
        data = {
            'Salesman': [order.sales_man.employee_name if order.sales_man else 'Unknown' for order in orders],
            'Customer': [order.customer.name if order.customer else 'Cash Customer' for order in orders],
            'Date': [order.order_date.replace(tzinfo=None) for order in orders],
            'Invoice Number': [order.invoice_number for order in orders],
            'Products': [', '.join([item.product.name for item in order.orderitem_set.all()]) for order in orders],
            'Amount': [order.total_amount for order in orders],
            'Payed Amount': [order.payed_amount for order in orders],
            'Balance Amount': [order.balance_amount for order in orders],
            'Payment Status': [order.payment_status1 for order in orders],
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)
        
        # Sort the DataFrame by Salesman and Customer
        df = df.sort_values(by=['Salesman', 'Customer'])

        # Calculate totals
        totals = {
            'Salesman': 'Total',
            'Customer': '',
            'Date': '',
            'Invoice Number': '',
            'Products': '',
            'Amount': df['Amount'].sum(),
            'Payed Amount': df['Payed Amount'].sum(),
            'Balance Amount': df['Balance Amount'].sum(),
            'Payment Status': '',
        }

        # Append total row to the DataFrame
        totals_df = pd.DataFrame([totals])
        df = pd.concat([df, totals_df], ignore_index=True)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response

    



def sale_report_excel_customer_wise(request):
    if request.method == "POST":
        # Get the start and end date from the form, along with the selected customer
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        selected_customer = request.POST.get("customer")  # Customer filter

        # Filter orders based on the date range and customer (if selected)
        if selected_customer:
            orders = Order.objects.filter(
                order_date__range=[start_date, end_date],
                customer_id=selected_customer
            )
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])

        # Prepare product-wise data
        data = {
            'Customer': [],
            'Product': [],
            'Quantity': [],
            'Total Price': [],
            'Order Date': [],
            'Invoice Number': [],
            'Paid Amount': [],
            'Discount': [],
            'Balance Amount': [],
            'Payment Status': [],
        }

        for order in orders:
            for item in order.orderitem_set.all():
                data['Customer'].append(order.customer.name if order.customer else 'Cash Customer')
                data['Product'].append(item.product.name)
                data['Quantity'].append(item.quantity)
                data['Total Price'].append(item.total_price)
                data['Order Date'].append(order.order_date.replace(tzinfo=None))
                data['Invoice Number'].append(order.invoice_number)
                data['Paid Amount'].append(order.payed_amount)
                data['Discount'].append(order.discount)
                data['Balance Amount'].append(order.balance_amount)
                data['Payment Status'].append(order.payment_status1)

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)

        # Calculate totals
        total_row = {
            'Customer': 'Total',
            'Product': '',
            'Quantity': '',
            'Total Price': df['Total Price'].sum(),
            'Order Date': '',
            'Invoice Number': '',
            'Paid Amount': df['Paid Amount'].sum(),
            'Discount': df['Discount'].sum(),
            'Balance Amount': df['Balance Amount'].sum(),
            'Payment Status': '',
        }

        # Convert total_row to DataFrame and concatenate
        total_df = pd.DataFrame([total_row])
        df = pd.concat([df, total_df], ignore_index=True)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Customer_sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response

    
from POS.models import OrderItem

def sale_report_product_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        product_id = request.POST.get("product")

        # Filter OrderItems based on the date range and optionally by product
        order_items = OrderItem.objects.filter(
            order__order_date__range=[start_date, end_date]
        )

        # If a product is specified, filter by product as well
        if product_id:
            order_items = order_items.filter(product_id=product_id)

        # Prepare data for the report
        data = {
            'Order Number': [order_item.order.invoice_number for order_item in order_items],
            'Date of Order': [order_item.order.order_date.replace(tzinfo=None) for order_item in order_items],
            'Product': [order_item.product.name for order_item in order_items],
            'Quantity': [order_item.quantity for order_item in order_items],
            'Unit Price': [order_item.unit_price for order_item in order_items],
            'Discount': [order_item.discount for order_item in order_items],
            'Total Price': [order_item.total_price for order_item in order_items],
            
        }

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response
    

# purchase reports 

def export_purchase_report_excel(request):
    if request.method == 'POST':
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        purchases = Purchase.objects.filter(bill_date__range=[start_date, end_date])

        # Prepare data for the report
        data = []
        for purchase in purchases:
            data.append({
                'Purchase Bill Number': purchase.purchase_bill_number,
                'Supplier': purchase.supplier.name if purchase.supplier else '',
                'Purchase Type': purchase.purchase_type,
                'Product':purchase.purchase_item,
                'Bill Date': purchase.bill_date.strftime('%Y-%m-%d'),
                'Amount': purchase.amount,
                'Paid Amount': purchase.paid_amount,
                'Balance Amount': purchase.balance_amount,
                'Payment Status': purchase.payment_status,
                'Shipping Cost': purchase.shipping_cost,
            })

        df = pd.DataFrame(data)

        # Create the response object
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=purchase_report_{start_date}_to_{end_date}.xlsx'

        # Write to the Excel file
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Purchases')

        return response
    

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def export_purchase_report_pdf(request):
    if request.method == 'POST':
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')

        purchases = Purchase.objects.filter(bill_date__range=[start_date, end_date])

        # Create the response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=purchase_report_{start_date}_to_{end_date}.pdf'

        # Create PDF canvas
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Draw header
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, height - 50, f"Purchase Report ({start_date} to {end_date})")

        # Draw table header
        y = height - 100
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Bill Number")
        p.drawString(150, y, "Supplier")
        p.drawString(250, y, "Product")
        p.drawString(350, y, "Bill Date")
        p.drawString(450, y, "Amount")
        p.drawString(500, y, "Paid")
        p.drawString(550, y, "Balance")

        # Draw data rows
        p.setFont("Helvetica", 10)
        for purchase in purchases:
            y -= 20

            # Use str() to ensure no None values are passed, provide defaults for None fields
            bill_number = purchase.purchase_bill_number if purchase.purchase_bill_number else "N/A"
            supplier_name = purchase.supplier.name if purchase.supplier and purchase.supplier.name else "Unknown"
            product_name = str(purchase.purchase_item) if purchase.purchase_item else "No Product"
            bill_date = purchase.bill_date.strftime('%Y-%m-%d') if purchase.bill_date else "N/A"
            amount = f"{purchase.amount}" if purchase.amount else "0.00"
            paid_amount = f"{purchase.paid_amount}" if purchase.paid_amount else "0.00"
            balance_amount = f"{purchase.balance_amount}" if purchase.balance_amount else "0.00"

            # Draw data
            p.drawString(50, y, bill_number)
            p.drawString(150, y, supplier_name)
            p.drawString(250, y, product_name)
            p.drawString(350, y, bill_date)
            p.drawString(450, y, amount)
            p.drawString(500, y, paid_amount)
            p.drawString(550, y, balance_amount)

        # Finalize the PDF
        p.showPage()
        p.save()

        return response

    


# db download

from django.http import HttpResponse, Http404
import os
from django.conf import settings

def download_db(request):
    # Path to your SQLite database file
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    
    # Check if the file exists
    if os.path.exists(db_path):
        with open(db_path, 'rb') as db_file:
            response = HttpResponse(db_file.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = 'attachment; filename="db.sqlite3"'
            return response
    else:
        raise Http404("Database not found.")






