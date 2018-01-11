from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from pagseguro.api import PagSeguroApiTransparent

from carton.cart import Cart
from products.models import Product

class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'core/index.html'

class CartView(TemplateView):
    template_name = 'core/cart.html'

    def render_to_response(self, context):
        pagseguro_api = PagSeguroApiTransparent()
        pagseguro_session = pagseguro_api.get_session_id()
        
        response = super(DeliveryView, self).render_to_response(context, **kwargs)
        response.set_cookie(
            'pagseguro_session', 
            value=pagseguro_session['session_id']
        )
        return response

    def post(self, request, *args, **kwargs):
        cart = Cart(request.session)
        print('POST')
        cart.clear()
        return HttpResponseRedirect(reverse_lazy('core:index'))

def add_to_cart(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=int(request.GET.get('id')))
    cart.add(product, price=product.price)
    return HttpResponseRedirect(reverse_lazy('core:index'))