from django.utils import timezone
from django.db import models


class Product(models.Model):

    # One of the attributes in class.
    DISCOUNT_RATE = 0.10

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    sale_start = models.DateTimeField(blank=True, null=True, default=None)
    sale_end = models.DateTimeField(blank=True, null=True, default=None)
    photo = models.ImageField(blank=True, null=True,
                              default=None, upload_to='products')

    def is_on_sale(self):
        '''
        Returns True if there is Sale,
        False otherwise.
        '''
        now = timezone.now()
        if self.sale_start:
            if self.sale_end:
                return self.sale_start <= now <= self.sale_end
            return self.sale_start <= now
        return False

    def get_rounded_price(self):
        '''
        Returns the rounded price of the product.
        '''
        return round(self.price, 2)

    def current_price(self):
        '''
        Returns the current price of a product.
        If it is on sale, then its sale price or 
        else it's regular price is returned.
        '''
        if self.is_on_sale():
            discounted_price = float(self.price * (1 - self.DISCOUNT_RATE))
            return round(discounted_price, 2)
        return self.get_rounded_price()

    def __repr__(self):
        '''
        Representation of the object.
        '''
        return '<Product object ({}) "{}">'.format(self.id, self.name)


class ShoppingCart(models.Model):
    TAX_RATE = 0.13

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def subtotal(self):
        '''
        Returns only the total price exclusive of taxes.
        '''
        amount = 0.0
        for item in self.shopping_cart_items:
            amount += item.quantity * item.product.get_price()
        return round(amount, 2)

    def taxes(self):
        '''
        Returns only the tax price of the Shopping cart.
        '''
        return round(self.TAX_RATE * self.subtotal(), 2)

    def total(self):
        '''
        Returns the total price inclusive of taxes.
        '''
        return round(self.subtotal() * self.taxes(), 2)

    def __repr__(self):
        name = self.name or '[Guest]'
        address = self.address or '[No Address]'
        return '<ShoppingCart object ({}) "{}" "{}">'.format(self.id, name, address)


class ShoppingCartItem(models.Model):
    # If the shopping cart is deleted, obviously the items inside it are also going to be deleted or gone.
    shopping_cart = models.ForeignKey(
        ShoppingCart, related_name='items', related_query_name='item', on_delete=models.CASCADE)
    # If the product gets deleted, then obviously that ShoppingCartItem would be deleted.
    product = models.ForeignKey(
        Product, related_name='+', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total(self):
        return round(self.quantity * self.product.current_price())

    def __repr__(self):
        return '<ShoppingCartItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.product.name)
