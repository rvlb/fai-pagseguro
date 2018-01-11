from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings

from decimal import Decimal

from pagseguro.api import PagSeguroApiTransparent
from carton.cart import Cart

from products.models import Product, OrderProduct
from accounts.models import Order

class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'core/index.html'

class CartView(TemplateView):
    template_name = 'core/cart.html'

    def render_to_response(self, context):
        pagseguro_session = PagSeguroApiTransparent().get_session_id()
        response = super(CartView, self).render_to_response(context)
        response.set_cookie('pagseguro_session', value=pagseguro_session['session_id'])
        return response

    def post(self, request, *args, **kwargs):
        print(request.POST)

        cart = Cart(request.session)

        products = [
            OrderProduct(
                product=item.product,
                price=item.price,
                quantity=item.quantity
            ) for item in cart.items
        ]
        new_order = Order(owner=request.user)

        ### PagSeguro Begin
        api = PagSeguroApiTransparent()
        api.set_sender_hash(request.POST['sender-hash'])

        sender = {
            'name': 'Joãozinho do CITi', 
            'area_code': 81, 
            'phone': 21268430, 
            'email': settings.PAGSEGURO_TEST_BUYER_EMAIL, 
            'cpf': '10683924443'
        }
        api.set_sender(**sender)

        shipping = {
            'street': 'Av. Jornalista Aníbal Fernandes', 
            'number': 1, 
            'complement': 'Centro de Informática', 
            'district': 'Cidade Universitária', 
            'postal_code': '01452002', 
            'city': 'Recife', 
            'state': 'PE', 
            'country': 'BRA',
            'cost': Decimal('0.00')
        }
        api.set_shipping(**shipping)

        if 'bank-slip' in request.POST:
            # Boleto bancário
            api.set_payment_method('boleto')
        elif 'credit-card' in request.POST:
            # Cartão de crédito
            api.set_payment_method('creditcard')

            installments = 1
            installment_amount = cart.total # Deve ser o valor da parcela obtida no browser

            data = {
                'quantity': installments, 
                'value': installment_amount, 
                'name': 'Joãozinho do CITi', 
                'birth_date': '10/02/1995', 
                'cpf': '10683924443', 
                'area_code': 81, 
                'phone': 21268430
            }
            api.set_creditcard_data(**data)

            billing = {
                'street': 'Av. Jornalista Aníbal Fernandes', 
                'number': 1, 
                'complement': 'Centro de Informática', 
                'district': 'Cidade Universitária', 
                'postal_code': '01452002', 
                'city': 'Recife', 
                'state': 'PE', 
                'country': 'BRA',
            }
            api.set_creditcard_billing_address(**billing)

            api.set_creditcard_token(request.POST['card-token'])
        
        for p in products:
            api.add_item(p.to_pagseguro())

        checkout = api.checkout()

        if checkout['success']:
            print(checkout)
        ### PagSeguro End

        new_order.save()
        for p in products:
            p.save()
            new_order.products.add(p);
        
        cart.clear()
        return HttpResponseRedirect(reverse_lazy('core:index'))

def add_to_cart(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=int(request.GET.get('id')))
    cart.add(product, price=product.price)
    return HttpResponseRedirect(reverse_lazy('core:index'))