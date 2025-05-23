from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

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

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1500},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 49},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 199},
    ]



class ProductIndexView(View):
    template_name = 'pages/products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'pages/products/show.html'

    def get(self, request, id):
        product = Product.products[int(id) - 1]
        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)
