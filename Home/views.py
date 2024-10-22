from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unautenticated_user
from django.contrib.auth.decorators import login_required
import datetime
from Finance.models import Income, Expence
from django.db.models import Sum
from django.utils.timezone import now
from POS.models import Order
from Inventory.models import Product, Purchase
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from .models import Staff, StaffSalary
from .forms import StaffForm, StaffSalaryForm



def get_current_month_income_and_expense():
    # Get current year and month
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
    # Filter and aggregate total income for the current month
    total_income = Income.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter and aggregate total expenses for the current month
    total_expense = Expence.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return total_income, total_expense


def get_current_month_orders():
    # Get current year and month
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)

    # Filter orders for the current month and count them
    total_orders = Order.objects.filter(
        order_date__gte=current_month_start,
        order_date__lte=current_month_end
    ).count()

    return total_orders

def get_top_selling_products():
    # Annotate the total quantity sold for each product through OrderItem
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')  # Sum quantity from related OrderItem model
    ).order_by('-total_sold')[:5]  # Order by total_sold in descending order and limit to 5

    return top_products


# for chat js function 

def get_monthly_data(request):
    # Get data for Orders grouped by month
    order_data = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
        total_order_amount=Sum('total_amount')).order_by('month')

    # Get data for Purchases grouped by month
    purchase_data = Purchase.objects.annotate(month=TruncMonth('bill_date')).values('month').annotate(
        total_purchase_amount=Sum('amount')).order_by('month')

    # Prepare data for response
    response_data = {
        "months": [order['month'].strftime("%B %Y") for order in order_data],
        "orders": [order['total_order_amount'] for order in order_data],
        "purchases": [purchase['total_purchase_amount'] for purchase in purchase_data],
    }

    return JsonResponse(response_data)

def get_monthly_revenue_expense(request):
    # Aggregate Income data by month
    income_data = Income.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_income=Sum('amount')).order_by('month')

    # Aggregate Expence data by month
    expense_data = Expence.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_expense=Sum('amount')).order_by('month')

    # Prepare response data (months, income, expense)
    response_data = {
        "months": [income['month'].strftime("%B %Y") for income in income_data],
        "incomes": [income['total_income'] for income in income_data],
        "expenses": [expense['total_expense'] for expense in expense_data],
    }

    return JsonResponse(response_data)

@login_required(login_url='SignIn')
def Index(request):
    month = now().strftime("%B")

    total_income, total_expense = get_current_month_income_and_expense()
    total_orders = get_current_month_orders()
    top_products = get_top_selling_products()

    context = {
        "total_income":total_income,
        "total_expense":total_expense,
        "total_orders":total_orders,
        "top_products":top_products,
        "month":month
    }
    return render(request,"index.html",context)


@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')

# In views.py
from django.shortcuts import render

def custom_500(request):
    return render(request, 'errorpage/pages-error-500.html', status=404)

def custom_404(request, exception):
    return render(request, 'errorpage/pages-error.html', status=500)


def add_customers(request):
    return render(request, "add_customers.html")



@login_required(login_url="SignIn")
def list_staff(request):
    staff = Staff.objects.all()

    context = {
        "staff":staff
    }
    return render(request,"list-staff.html",context)


@login_required(login_url="SignIn")
def add_staff(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Staff Created Success.....")
            return redirect("list_staff")
    context = {
        "form":form
    }
    return render(request,"add-staff.html",context)


@login_required(login_url="SignIn")
def delete_staff(request,pk):
    staff = get_object_or_404(Staff,id = pk)
    staff.delete()
    messages.success(request,"employee deleted success.....")
    return redirect("list_staff")


@login_required(login_url="SignIn")
def update_staff(request,pk):
    staff = get_object_or_404(Staff,id = pk)
    salary = StaffSalary.objects.filter(staff = staff)
    form = StaffForm(instance=staff)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.info(request,"Staff Updated")
            return redirect("update_staff", pk = pk)
    
    return render(request,"update_staff.html",{"form":form, "staff":staff,"salary":salary})




# finance salary calculation associated functions gos here

@login_required(login_url="SignIn")
def list_salary(request):
    salary = StaffSalary.objects.all()
    return render(request,"list-salaries.html",{"salary":salary})

@login_required(login_url="SignIn")
def add_salary(request):
    form = StaffSalaryForm()
    if request.method == "POST":
        form = StaffSalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            salary.save()
            expense = Expence(
                        perticulers = f"Paid to  {salary.staff} as Salary Slip No {salary.slip_no}",
                        date = datetime.datetime.now(),
                        amount = salary.amount
                    )
            expense.save()
            messages.success(request,"Salary was added to Staff account")
            return redirect("list_salary")
        else:
            messages.error(request,"Some thing Wrong")
            return redirect("list_salary")
        
    return render(request,"add-salary.html",{"form":form})
