from pyexpat import model
from rest_framework import serializers

from .models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    '''
    This serializer class serializes the ShoppingCartItem's product
    and quantity fields.
    '''

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):

    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'price', 'sale_start', 'sale_end',
                  'is_on_sale', 'current_price', 'cart_items', )

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
            # Below many model instances are serialized.
            return CartItemSerializer(items, many=True).data

    # In serializers there is a method 'to_representation'

    # def to_representation(self, instance):

    #     # Below 'data' variable is an ordered dictionary.
    #     data = super().to_representation(instance)

    #     # We are adding some key:value pairs to the dictionary,
    #     # as per our requirement.
    #     data['is_on_sale'] = instance.is_on_sale()
    #     data['current_price'] = instance.current_price()

    #     return data
