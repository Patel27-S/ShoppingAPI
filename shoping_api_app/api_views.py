from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    # Below will enable search on the basis of name and
    # description for client.
    search_fields = ('name', 'description')

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        # If on_sale is Not defined in the URL, i.e. in the case
        # when client does not want results on the basis of
        # on_sale or not.
        if on_sale is None:
            return super().get_queryset()
        else:
            queryset = Product.objects.all()
            if on_sale.lower() == 'true':
                from django.utils import timezone
                now = timezone.now()
                return queryset.filter(
                    sale_start__lte=now,
                    sale_end__gte=now,
                )
            return queryset
