from django.shortcuts import render, redirect
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unautenticated_user
from django.contrib.auth.decorators import login_required
import datetime
from Finance.models import Income, Expence
from django.db.models import Sum
from django.utils.timezone import now
from POS.models import Order
from Inventory.models import Product



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
