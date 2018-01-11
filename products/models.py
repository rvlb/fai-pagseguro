from django.db import models

from pagseguro.api import PagSeguroItem

class Product(models.Model):
    name = models.CharField('Nome', max_length=100)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=100)

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=100)
    quantity = models.IntegerField('Quantidade')

    def to_pagseguro(self):
        return PagSeguroItem(
            id=self.product.id,
            description=self.product.name, 
            amount=self.price, 
            quantity=self.quantity
        )