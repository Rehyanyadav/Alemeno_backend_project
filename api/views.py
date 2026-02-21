from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from datetime import date
import math

@api_view(['POST'])
def register(request):
    data = request.data
    monthly_income = data.get('monthly_income')
    
    # Rule: approved_limit = 36 * monthly_salary (rounded to nearest lakh)
    approved_limit = round((36 * monthly_income) / 100000) * 100000
    
    customer = Customer.objects.create(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        phone_number=data.get('phone_number'),
        monthly_income=monthly_income,
        approved_limit=approved_limit
    )
    
    return Response({
        "customer_id": customer.customer_id,
        "name": f"{customer.first_name} {customer.last_name}",
        "age": customer.age,
        "monthly_income": customer.monthly_income,
        "approved_limit": customer.approved_limit,
        "phone_number": customer.phone_number
    }, status=status.HTTP_201_CREATED)

def calculate_credit_score(customer):
    all_loans = Loan.objects.filter(customer=customer)
    if not all_loans.exists():
        return 100
    
    # 1. Punctuality (50% weight)
    total_emis = sum(l.tenure for l in all_loans)
    if total_emis > 0:
        paid_on_time_ratio = sum(l.emis_paid_on_time for l in all_loans) / total_emis
    else:
        paid_on_time_ratio = 1.0
    
    # 2. Experience (25% weight)
    # Scoring 5 points per loan, max 25
    experience_score = min(all_loans.count(), 5) * 5
    
    # 3. Current Activity (25% weight)
    # Check loans tagken in the current year
    current_year_loans = all_loans.filter(start_date__year=date.today().year).count()
    # 25 points if 0-1 loans, decreasing by 5 for each additional loan
    activity_score = max(0, 25 - (current_year_loans * 5))
    
    score = (paid_on_time_ratio * 50) + experience_score + activity_score
    
    # Safety Kill Switch: Current Debt > Approved Limit
    active_loans = all_loans.filter(end_date__gte=date.today())
    current_debt = sum(l.loan_amount for l in active_loans)
    
    if current_debt > customer.approved_limit:
        return 0
    
    return min(100, score)

def get_eligibility(customer_id, requested_loan_amount, interest_rate, tenure):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    credit_score = calculate_credit_score(customer)
    
    approval = False
    corrected_interest_rate = interest_rate
    
    if credit_score > 50:
        approval = True
    elif 50 >= credit_score > 30:
        approval = True
        corrected_interest_rate = max(interest_rate, 12)
    elif 30 >= credit_score > 10:
        approval = True
        corrected_interest_rate = max(interest_rate, 16)
    else:
        approval = False
        
    # Check if sum of all current EMIs > 50% of monthly income
    active_loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    total_current_emis = sum(l.monthly_repayment for l in active_loans)
    
    monthly_rate = corrected_interest_rate / (12 * 100)
    if monthly_rate > 0:
        new_emi = (requested_loan_amount * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)
    else:
        new_emi = requested_loan_amount / tenure

    if total_current_emis + new_emi > (0.5 * customer.monthly_income):
        approval = False

    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": round(new_emi, 2),
        "credit_score": round(credit_score, 1)
    }

@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    res = get_eligibility(
        data.get('customer_id'),
        data.get('loan_amount'),
        data.get('interest_rate'),
        data.get('tenure')
    )
    if res is None:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(res)

@api_view(['POST'])
def create_loan(request):
    data = request.data
    resp = get_eligibility(
        data.get('customer_id'),
        data.get('loan_amount'),
        data.get('interest_rate'),
        data.get('tenure')
    )
    
    if resp is None:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    if resp.get('approval'):
        customer = Customer.objects.get(customer_id=resp['customer_id'])
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data['loan_amount'],
            tenure=data['tenure'],
            interest_rate=resp['corrected_interest_rate'],
            monthly_repayment=resp['monthly_installment'],
            start_date=date.today(),
            end_date=date.today(), 
            emis_paid_on_time=0
        )
        return Response({
            "loan_id": loan.loan_id,
            "customer_id": loan.customer.customer_id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": loan.monthly_repayment
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "loan_id": None,
            "customer_id": data['customer_id'],
            "loan_approved": False,
            "message": "Loan not approved based on credit score or income",
            "monthly_installment": 0
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        customer = loan.customer
        return Response({
            "loan_id": loan.loan_id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure
        })
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer_id=customer_id)
    data = []
    for l in loans:
        data.append({
            "loan_id": l.loan_id,
            "loan_amount": l.loan_amount,
            "interest_rate": l.interest_rate,
            "monthly_installment": l.monthly_repayment,
            "repayments_left": l.tenure - l.emis_paid_on_time
        })
    return Response(data)
