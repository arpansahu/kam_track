from django.shortcuts import render

from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import base64
import pyotp
import traceback
from mailjet_rest import Client  # Import Mailjet client
from datetime import datetime
import random
from django.shortcuts import get_object_or_404


# Set up logging
import logging
logger = logging.getLogger('django')

from django.core.exceptions import PermissionDenied
    
           

def terms_and_condition_view(request):
    return render(request, 'extras/terms_and_conditions.html')

def privacy_policy_view(request):
    return render(request, 'extras/privacy_policy.html')

def data_protection_policy_view(request):
    return render(request, 'extras/data_protection_policy.html')

def data_processing_agreement_view(request):
    return render(request, 'extras/data_processing_agreement.html')

def affiliate_program_view(request):
    return render(request, 'extras/coming_soon.html')

def home_view(request):
    return render(request, 'home.html')

