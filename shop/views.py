from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ReviewRating
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse
from .forms import ReviewForm
from django.core.mail import send_mail
from django.contrib.auth.models import User


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart = Cart(request)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart': cart})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # set choices for quantity available based on inventory and items in this session's cart
    cart = Cart(request)
    cartquantity = 0
    # if item in cart, subtract the items in the cart from the quantity available
    for item in cart:
        cartproduct = get_object_or_404(Product, id=item['product'].id)
        if product == cartproduct:
            cartquantity = item['quantity']
            break
    if product.quantity - cartquantity > 0:
        choices = [(i, str(i)) for i in range(1, product.quantity - cartquantity + 1)]
    else:  # no items left in inventory for this session
        choices = [(1, 0)]

    cart_product_form = CartAddProductForm(my_choices=choices)
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'reviews': reviews,
                   'cart_product_form': cart_product_form,
                   'cart': cart})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched).order_by('-id')
        return render(request, 'shop/search.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'shop/search.html', {})


class ProductCreate(CreateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'available', 'quantity']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('shop:product_list'))


class ProductUpdate(UpdateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'available', 'quantity']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('shop:product_list'))


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        product.delete()
        messages.success(request, (product.name + ' ' + 'has been successfully deleted'))
        return HttpResponseRedirect(reverse('shop:product_list'))
    except:
        messages.success(request, ("Error." + ' ' + product.name + ' ' + "cannot deleted"))
        return HttpResponseRedirect(reverse('shop:product_list'))


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


# add send e-mail confirmation
# set up the subject, message, and user’s email address
subject = '{}, the email subject'.format
message = 'this is the message "{}"'.format

user = User
user_email = user.email

# try to send the e-mail – note you can send to multiple users – this just sends
# to one user.
try:
    send_mail(subject, message, 'unostudent99@gmail.com', [user_email])
    sent = True
except:
    print("Error sending e-mail")
