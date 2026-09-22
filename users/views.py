from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.models import Action, create_action
from VT.models import comments, newitem

from .models import details


def _role(request):
    return request.session.get('role')


def register(request):
    if request.method != 'POST':
        return render(request, 'Users/register.html')
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    if not username or not password:
        messages.error(request, 'Username and password are required.')
        return render(request, 'Users/register.html')
    if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken.')
        return render(request, 'Users/register.html')
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=request.POST.get('first_name', ''),
        last_name=request.POST.get('last_name', ''),
        email=request.POST.get('email', ''),
    )
    details.objects.create(user=user, role=request.POST.get('role') or 'regular')
    create_action(user, 'was registered')
    messages.success(request, 'Account created. Log in to continue.')
    return redirect('VTessential:home_page')


def add_user(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    return render(request, 'Users/add_user.html')


@require_POST
def added(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    if not username or not password:
        messages.error(request, 'Username and password are required.')
        return render(request, 'Users/add_user.html')
    if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken.')
        return render(request, 'Users/add_user.html')
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=request.POST.get('first_name', ''),
        last_name=request.POST.get('last_name', ''),
        email=request.POST.get('email', ''),
    )
    details.objects.create(user=user, role=request.POST.get('role') or 'regular')
    if request.user.is_authenticated:
        create_action(user, 'was added by the admin', user)
    messages.success(request, 'User added.')
    return redirect('user:user_list')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    items = newitem.objects.all()
    recent = Action.objects.filter(user=user).select_related('user').order_by('-created')[:9]
    return render(
        request,
        'Users/profile.html',
        {'user': user, 'items': items, 'action': recent},
    )


@require_POST
def edit(request):
    request.session['user_id'] = request.POST.get('user_id')
    request.session['first_name'] = request.POST.get('first_name')
    request.session['last_name'] = request.POST.get('last_name')
    request.session['username'] = request.POST.get('username') or request.session.get('username')
    request.session['email'] = request.POST.get('email')
    return render(request, 'Users/edit.html')


@require_POST
def edit_preview(request):
    user_id = request.POST.get('user_id') or request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.POST.get('first_name'):
        user.first_name = request.POST.get('first_name')
    if request.POST.get('last_name'):
        user.last_name = request.POST.get('last_name')
    if request.POST.get('email'):
        user.email = request.POST.get('email')
    new_password = request.POST.get('new_password')
    if new_password:
        user.set_password(new_password)
    user.save()
    messages.success(request, 'Profile updated.')
    return redirect('user:profile', username=user.username)


def user_list(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    people = User.objects.select_related('details').all()
    return render(request, 'Users/user_list.html', {'user': people})


@require_POST
def edit_user(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    return render(request, 'Users/edit_user.html')


@require_POST
def admin_review(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    username = request.POST.get('username', '').strip()
    user = get_object_or_404(User, username=username)
    if request.POST.get('first_name'):
        user.first_name = request.POST.get('first_name')
    if request.POST.get('last_name'):
        user.last_name = request.POST.get('last_name')
    if request.POST.get('email'):
        user.email = request.POST.get('email')
    new_password = request.POST.get('new_password')
    if new_password:
        user.set_password(new_password)
    user.save()
    messages.success(request, 'User updated.')
    return redirect('user:user_list')


def review(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    review_list = comments.objects.select_related('user', 'item').order_by('-time')
    return render(request, 'Users/review_list.html', {'comment': review_list})


@require_POST
def comment(request):
    request.session['title'] = request.POST.get('title')
    request.session['user'] = request.POST.get('username') or request.session.get('username')
    return render(request, 'Users/comment.html')


@require_POST
def comment_added(request):
    user = get_object_or_404(User, pk=request.POST.get('user_id'))
    item = get_object_or_404(newitem, pk=request.POST.get('item_id'))
    comments.objects.create(
        user=user,
        item=item,
        description=request.POST.get('comment', ''),
    )
    create_action(user, 'Added a new Review for', item)
    messages.success(request, 'Review added.')
    return redirect('VTessential:item_detail', item_id=item.id)


@require_POST
def edit_review(request):
    request.session['comment_id'] = request.POST.get('comment_id')
    request.session['user_id'] = request.POST.get('user_id')
    request.session['item_id'] = request.POST.get('item_id')
    return render(request, 'Users/comment_preview.html')


@require_POST
def comment_edited(request):
    review_obj = get_object_or_404(comments, pk=request.POST.get('comment_id') or request.session.get('comment_id'))
    text = request.POST.get('review')
    if text is not None:
        review_obj.description = text
        review_obj.save(update_fields=['description'])
    messages.success(request, 'Review updated.')
    return redirect('user:review')


@require_POST
def delete_comment(request):
    if _role(request) != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('VTessential:home_page')
    item_id = request.POST.get('item_id')
    comment_id = request.POST.get('comment_id')
    qs = comments.objects.all()
    if comment_id:
        qs = qs.filter(pk=comment_id)
    elif item_id:
        qs = qs.filter(item_id=item_id)
    else:
        qs = qs.none()
    qs.delete()
    messages.success(request, 'Review deleted.')
    return redirect('user:review')
