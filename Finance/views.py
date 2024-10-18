from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import *
from .forms import *


def income(request):
    inocme = Income.objects.all()

    context = {
        "income":inocme
    }
    return render(request,"finance/income.html",context)


def add_income(request):
    form = IncomeForm()

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Income record added successfully.")
            return redirect('income')  # Redirect to the same page or another view
 
    return render(request, 'finance/add-income.html', {'form': form})





def expence(request):
    ex = Expence.objects.all()

    context = {
        "expence":ex
    }
    return render(request,"finance/expence.html",context)


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


from django.shortcuts import render
from django.utils.timezone import now
from .models import Income, Expence
from itertools import chain
from operator import attrgetter

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


def reports(request):
    return render(request,"reports.html")



