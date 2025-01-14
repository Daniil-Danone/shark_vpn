from django.shortcuts import render

def payment_success(request):
    return render(
        request=request, 
        template_name='payment.html'
    )
