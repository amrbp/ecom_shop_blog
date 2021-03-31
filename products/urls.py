from django.urls import path
from products.views import *

app_name = 'products'

urlpatterns = [
    path('', product_list, name="product_list"),
    path('cart/', cart , name='cart'),
    path('checkout/', checkout , name='checkout'),
    path('update_item/', updateItem , name='update_item'),
    path('process_order/', processOrder , name='process_order'),
    path('product/<int:pk>/', ProductDetailView, name='product_detail'),
]
