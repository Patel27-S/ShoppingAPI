from pyexpat import model
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'price', 'sale_start', 'sale_end')

    # In serializers there is a method 'to_representation'

    def to_representation(self, instance):

        # Below 'data' variable is an ordered dictionary.
        data = super().to_representation(instance)

        # We are adding some key:value pairs to the dictionary,
        # as per our requirement.
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()

        return data
