from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    product_items = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': product_items})


def customer(request, pk_test):
    customer_item = Customer.objects.get(id=pk_test)

    orders = customer_item.order_set.all()
    order_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {'customer': customer_item, 'orders': orders, 'order_count': order_count, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer_item = Customer.objects.get(id=pk)
    form_set = OrderFormSet(queryset=Order.objects.none(), instance=customer_item)
    if request.method == 'POST':
        form_set = OrderFormSet(request.POST, instance=customer_item)
        if form_set.is_valid():
            form_set.save()
            return redirect('/')
    context = {'formset': form_set}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
