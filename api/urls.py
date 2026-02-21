from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_index(request):
    return Response({
        "message": "Welcome to the Credit Approval System API",
        "endpoints": {
            "register": "/api/register/",
            "check_eligibility": "/api/check-eligibility/",
            "create_loan": "/api/create-loan/",
            "view_loan": "/api/view-loan/<loan_id>/",
            "view_loans": "/api/view-loans/<customer_id>/"
        }
    })

urlpatterns = [
    path('', api_index),
    path('register/', views.register),
    path('check-eligibility/', views.check_eligibility),
    path('create-loan/', views.create_loan),
    path('view-loan/<int:loan_id>/', views.view_loan),
    path('view-loans/<int:customer_id>/', views.view_loans),
]
