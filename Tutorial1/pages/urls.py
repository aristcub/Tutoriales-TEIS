from django.urls import include, path

from pages.utils import ImageLocalStorage
from .views import CartRemoveAllView, CartView, HomePageView, AboutPageView, ContactPageView, ImageViewFactory, ImageViewNoDI, ProductCreatedView, ProductIndexView, ProductShowView, ProductCreateView

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('products/', ProductIndexView.as_view(), name='products.index'), 
    path('products/<str:id>', ProductShowView.as_view(), name='products.show'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
    path('products/create/', ProductCreateView.as_view(), name='products.create'),
    path('products/created/', ProductCreatedView.as_view(), name='product-created'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('accounts/', include('accounts.urls')),
    path('image/', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_index'), 
    path('image/save', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_save'),
    path('image/save', ImageViewNoDI.as_view(), name='imagenodi_save'),
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenotdi'),
]
