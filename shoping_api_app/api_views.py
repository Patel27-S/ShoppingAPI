from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer
from .models import Product


class ProductList(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Need to add the feature of being able to
    # filter the products on the basis of 'id'
    # Of course, the products are listed, so we'd
    # use ListAPIView. But, the only thing is that
    # we use a filter and search by 'id'. Hence, need to
    # write the code for so to happen.
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)
