from pyexpat import model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Product, ShoppingCartItem, ShoppingCart


class CartItemSerializer(serializers.ModelSerializer):
    '''
    This serializer class serializes the ShoppingCartItem's product
    and quantity fields.
    '''
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):

    # Below are validations or restrictions for the fields.
    # Check them in the frontend and you won't be able to violate them.
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    average_product_sold = serializers.SerializerMethodField()
    #price = serializers.FloatField(min_value=1.0, max_value=100000)
    price = serializers.DecimalField(
        min_value=1.0, max_value=100000,
        max_digits=None, decimal_places=2,)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'price', 'sale_start', 'sale_end',
                  'is_on_sale', 'current_price', 'average_product_sold', 'cart_items',)

    def get_cart_items(self, instance):
        '''
        This method would return a product X's quantity in each 
        shopping cart in which it is present.
        '''
        # A particular product is going to be in many shopping carts,
        # therefore, 'items' below would have multiple ShoppingCartItem
        # objects assigned to it. (Idea : Draw ShoppingCartItem Table
        # and Understand.)
        items = ShoppingCartItem.objects.filter(product=instance)
        # Below many model instances are serialized. A List is then returned.
        return CartItemSerializer(items, many=True).data

    def get_average_product_sold(self, instance):

        # It is the average of total number of a particular product
        # sold to the total number of shopping carts existing.

        # For total number of that product sold :-
        cart_items_list = self.get_cart_items(instance)

        total_products_sold = 0
        for i in range(len(cart_items_list)-1):
            total_products_sold += cart_items_list[i]['quantity']

        # For total number of Shopping Carts :-
        total_shopping_carts = ShoppingCart.objects.all().count()

        try:
            average = float(total_products_sold/total_shopping_carts)
            return average
        except:
            average = 0

        return average

        # except ZeroDivisionError:
        #     average = 0
        #     return average

        # raise ValidationError(
        #     {'average_product_sold': 'There are zero shopping carts with this product'})
        # except:
        #     average = 0
        #     return average
        # raise ValidationError(
        #     {'average_product_sold': 'There is some problem.'})

        # In serializers there is a method 'to_representation'

        # def to_representation(self, instance):

        #     # Below 'data' variable is an ordered dictionary.
        #     data = super().to_representation(instance)

        #     # We are adding some key:value pairs to the dictionary,
        #     # as per our requirement.
        #     data['is_on_sale'] = instance.is_on_sale()
        #     data['current_price'] = instance.current_price()

        #     return data
