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


def POS_REST(request):
    return render(request,'restaurant/POS.html')