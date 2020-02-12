from django.shortcuts import render
from models import Merchant


# Create your views here.
def merchant_step(request):
    merchants = Merchant.objects.filter(active=True)
    return render(request, 'merchant.html', {'merchants': merchants})


def booking_step(request, merchant_id):
    return render(request, 'book.html')
