from django.shortcuts import render, redirect
from django.views import generic, View
from .form import CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import is_valid_path, reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from cart.carts import Cart
from django.utils.crypto import get_random_string
from .models import Order, OrderItem

from django.urls import reverse
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
            }
        return render(self.request, 'order/checkout.html', context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            # print(data)
            return JsonResponse({
                'success': True,
                "errors": None
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
                })

class InvoiceView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        order_id = self.generate_unique_order_id()
        
        context = {
            'cart': cart,
            'total': cart.total(),
            'order_id': order_id,
        }
        return render(request, 'order/invoice.html', context)

    def generate_unique_order_id(self):
        order_id = get_random_string(length=12)
        while Order.objects.filter(order_id=order_id).exists():
            order_id = get_random_string(length=12)
        return order_id
        

    

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
      
        host = request.get_host()
            
        cart = Cart(request)
        order_id = request.POST.get('order_id', '')
        total_amount = cart.total()

      
        total_amount_cents = int(total_amount * 100)

        checkout_session = stripe.checkout.Session.create(
            
            line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"Order {order_id}",
                },
                'unit_amount': total_amount_cents,
            },
            'quantity': 1,
            }],
        mode = 'payment',
        success_url = "http://{}{}".format(host, reverse('order:payment-success')),
        cancel_url = "http://{}{}".format(host, reverse('order:payment-cancel')),
        )

        return redirect(checkout_session.url, code=303)


    def paymentSuccess(request):
        cart = Cart(request)
        cart.clear()
        
        context = {'payment_status': "success"}
        return render(request, 'order/confirmation.html', context)


    def paymentCancel(request):
        context = {'payment_status': "cancel"}
        return render(request, 'order/cancellation.html', context)
    
    @csrf_exempt
    def my_webhook_view(request):
      payload = request.body
      print(payload)

      return HttpResponse(status=200)


@login_required
def OrderHistoryView(request):
    print("Current user:", request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_date')
    
    print("orders:", orders)
    context = {
        'orders': orders
        }
    print("Context", context)
    return render(request, 'order/order_history.html', context)
    
  
    