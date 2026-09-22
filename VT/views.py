from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.models import Action, create_action
from .models import comments, newitem


def _role(request):
    return request.session.get('role')


def home_page(request):
    items = newitem.objects.all()
    if _role(request) == 'admin':
        return redirect('VTessential:admin')
    if request.session.get('username'):
        recent = Action.objects.select_related('user').order_by('-created')[:9]
        return render(request, 'VT/pages/home.html', {'items': items, 'action': recent})
    return render(request, 'VT/pages/index.html', {'items': items})


@require_POST
def login_view(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is None:
        messages.error(request, 'Invalid username or password.')
        return redirect('VTessential:home_page')
    auth_login(request, user)
    role = getattr(getattr(user, 'details', None), 'role', 'regular')
    request.session['username'] = user.username
    request.session['role'] = role
    create_action(user, 'was logged in')
    if role == 'admin':
        return redirect('VTessential:admin')
    return redirect('VTessential:home_page')


def logout_view(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'Logged out.')
    return redirect('VTessential:home_page')


def list_page(request):
    items = newitem.objects.all()
    return render(request, 'VT/pages/list.html', {'items': items})


def sort_price(request):
    items = newitem.objects.order_by('price')
    return render(request, 'VT/pages/list_sort.html', {'items': items})


def sort_tshirt(request):
    items = newitem.objects.filter(type__in=['T-shirt', 'Tshirt', 't-shirt'])
    return render(request, 'VT/pages/list.html', {'items': items})


def sort_rating(request):
    items = newitem.objects.order_by('-rating')
    return render(request, 'VT/pages/list_sort.html', {'items': items})


def item_detail(request, item_id):
    item = get_object_or_404(newitem, pk=item_id)
    review_list = comments.objects.filter(item=item).select_related('user').order_by('-time')
    return render(
        request,
        'VT/pages/detail.html',
        {'item': item, 'comment': review_list, 'user': [request.user] if request.user.is_authenticated else []},
    )


@require_POST
def cart_item(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(newitem, pk=item_id)
    item.cart_items = (item.cart_items or 0) + 1
    item.save(update_fields=['cart_items'])
    return JsonResponse({'ok': True, 'cart_items': item.cart_items})


def admin_page(request):
    items = newitem.objects.all()
    return render(request, 'VT/pages/admin.html', {'items': items})


@require_POST
def admin_add(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    item = newitem.objects.create(
        title=request.POST.get('product_name', '').strip() or 'Untitled',
        type=request.POST.get('product_type', '').strip(),
        price=int(request.POST.get('price') or 0),
        rating=int(request.POST.get('rating') or 0),
        description=request.POST.get('description', ''),
        cart_items=0,
    )
    if request.user.is_authenticated:
        create_action(request.user, 'Added new product', item)
    messages.success(request, 'Product added.')
    return redirect('VTessential:admin')


def warning(request):
    if request.method == 'POST':
        request.session['delete_price'] = request.POST.get('price')
    return render(request, 'VT/pages/warning.html')


@require_POST
def delete_item(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    name = request.POST.get('product_name', '').strip()
    item = newitem.objects.filter(title=name).first()
    if item:
        item.delete()
        messages.success(request, 'Product deleted.')
    else:
        messages.error(request, 'No product matched that name.')
    return redirect('VTessential:admin')


def admin_review(request, item_id):
    item = get_object_or_404(newitem, pk=item_id)
    return render(request, 'VT/pages/detail_admin.html', {'item': item})


@require_POST
def edit(request):
    if _role(request) != 'admin' and request.session.get('username') != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    request.session['product_id'] = request.POST.get('product_id')
    request.session['product_name'] = request.POST.get('product_name')
    request.session['price'] = request.POST.get('price')
    request.session['rating'] = request.POST.get('rating')
    request.session['description'] = request.POST.get('description')
    return render(request, 'VT/pages/edit.html')


@require_POST
def edit_review(request):
    if _role(request) != 'admin' and request.session.get('username') != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    item_id = request.POST.get('product_id') or request.session.get('product_id')
    item = get_object_or_404(newitem, pk=item_id)
    title = request.POST.get('product_name', '').strip()
    if title:
        item.title = title
    if request.POST.get('price'):
        item.price = int(request.POST['price'])
    if request.POST.get('rating'):
        item.rating = int(request.POST['rating'])
    if request.POST.get('product_type'):
        item.type = request.POST.get('product_type', '').strip()
    if request.POST.get('description') is not None:
        item.description = request.POST.get('description', '')
    item.save()
    if request.user.is_authenticated:
        create_action(request.user, 'edited the product details', item)
    messages.success(request, 'Product updated.')
    return redirect('VTessential:admin')
