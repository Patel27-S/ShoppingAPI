from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError

from .serializers import ProductSerializer
from .models import Product


class ProductsPagination(LimitOffsetPagination):
    '''
    Setting the default and maximum limit a client can request
    for number of response objects on a single page.
    '''
    default_limit = 10
    max_limit = 100


class ProductList(ListAPIView):
    '''
    This view/endpoint is to list the all the products
    or as per the client's demand, if a certain filtered products
    are required to be returned.
    '''

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
    pagination_class = ProductsPagination

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        # If on_sale is Not defined in the URL, i.e. in the case
        # when client does not want results on the basis of
        # on_sale or not.
        # request.get_params() is the dictionary that is used to
        # pull out data from URL query.
        print(self.request.query_params.get('search'))
        # If the client wants to see all the products :
        if on_sale is None:
            return super().get_queryset()
        # If he/she mentioned on_sale=true in query:
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


class ProductCreate(CreateAPIView):
    '''
    This view/endpoint is so that the client 
    can create products.
    '''
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        '''
        The only purpose of this method's overriding is
        that it'll check if the price entered is less than or equal
        to 0.0 & also if it is at least a number. If so, validation error will
        be raised and shown to the end-user. Otherwise, super().create() would
        anyways be executed.
        '''
        try:
            # One things to remember here is that,
            # we are requesting that the data be posted and
            # stored in the database.
            # All the data is at first when posted by user is in the
            # 'request.data' named dictionary.
            price = request.data.get('price')
            if price and float(price) <= 0.0:
                # This will be shown to the client/end user, if entered is not
                # a value number for price.
                raise ValidationError(
                    {'price': 'Product cannot be free in price.'})
        except ValidationError:
            raise ValidationError({'price': 'Price has to be a number.'})
        # Returning the super().create() method eventually, meaning the data would
        # be stored in the database. And, create() returns the created object. So,
        # the client would be able to see the created object on UI. Can check
        # super().create() of parents from the source code.
        return super().create(request, *args, **kwargs)


# First thing that should come to the mind when wanting to destroy a resource is using
# DestroyAPIView.

class ProductDestroy(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    # We want to clear the cache when deleting an object from,
    # the Product Model so that the space can be used.
    # We override the delete method and put the logic for clearing the cache
    # for that particular product as well.
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f'product_data_{product_id}')
        return response


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''
    Three endpoints in a single view. A product can be retrieved, 
    updated and deleted.
    '''

    queryset = Product.objects.all()
    lookup_field = 'id'

    serializer_class = ProductSerializer

    # We want to clear the cache when deleting an object from,
    # the Product Model so that the space can be used.
    # We override the delete method and put the logic for clearing the cache
    # for that particular product as well.
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f'product_data_{product_id}')
        return response

    # Overriding the default update() method, in order to
    # update the cache of the product object which is updated.
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        # If the product was successfully updated, then adding the
        # updated cache or updating the cache.
        if response.status_code == 204:
            from django.core.cache import cache
            product = response.data
            cache.set('product_data_{}'.format(product['id']), {
                      'name': product['name'],
                      'description': product['description'],
                      'price': product['price']})
        return response
