from django.urls import path 
from .import views

urlpatterns = [
    path("income",views.income, name= "income"),
    path("expence",views.expence, name= "expence"),
    path("balance_sheet",views.balance_sheet, name= "balance_sheet"),
    path("balance_sheet_selected",views.balance_sheet_selected, name= "balance_sheet_selected"),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),


    # reports
    path("reports",views.reports,name="reports")
]