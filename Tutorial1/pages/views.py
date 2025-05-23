from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError

from pages.utils import ImageLocalStorage
from .models import Product

# ------------------ Static Pages ------------------

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView): 
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            "title": "About us - Online Store", 
            "subtitle": "About us",
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name",
        })
        return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
        })
        return context

# ------------------ Product Views ------------------

class ProductIndexView(View):
    template_name = 'pages/products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'pages/products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

# ------------------ Product Creation Form ------------------

class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price


class ProductCreateView(View):
    template_name = 'pages/products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-created')
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)


class ProductCreatedView(TemplateView):
    template_name = 'pages/products/success.html'


# ------------------ Cart Views ------------------

class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')


class CartView(View):
    template_name = 'pages/cart/index.html'

    def get(self, request):
        all_products = Product.objects.all()
        cart_product_data = request.session.get('cart_product_data', {})

        cart_products = []
        for product_id_str, quantity in cart_product_data.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                cart_products.append({
                    'product': product,
                    'quantity': quantity
                })
            except Product.DoesNotExist:
                continue

        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'available_products': all_products,
            'cart_products': cart_products
        }
        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        cart_product_data = request.session.get('cart_product_data', {})
        product_id_str = str(product_id)
        if product_id_str in cart_product_data:
            cart_product_data[product_id_str] += 1
        else:
            cart_product_data[product_id_str] = 1
        request.session['cart_product_data'] = cart_product_data
        return redirect('cart_index')

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'pages/images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View):
    template_name = 'pages/imagesnotdi/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('imagenotdi')  