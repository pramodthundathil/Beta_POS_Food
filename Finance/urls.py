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
    path("reports",views.reports,name="reports"),
    path('expence_report_excel/', views.expence_report_excel, name='expence_report_excel'),
    path('expence_report_pdf/', views.expence_report_pdf, name='expence_report_pdf'),
    path('income_report_excel/', views.income_report_excel, name='income_report_excel'),
    path('income_report_pdf/', views.income_report_pdf, name='income_report_pdf'),
    path('sale_report_excel/', views.sale_report_excel, name='sale_report_excel'),
    path('sale_report_pdf/', views.sale_report_pdf, name='sale_report_pdf'),
    
    
]