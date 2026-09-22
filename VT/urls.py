from django.urls import path

from . import views

app_name = 'VTessential'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clothing/', views.list_page, name='list_page'),
    path('clothing/sort/', views.sort_price, name='sort'),
    path('clothing/tshirt/', views.sort_tshirt, name='sortrev'),
    path('clothing/rating/', views.sort_rating, name='rating'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart/item/', views.cart_item, name='cart_item'),
    path('store/admin/', views.admin_page, name='admin'),
    path('store/admin/add/', views.admin_add, name='admin_add'),
    path('store/admin/warning/', views.warning, name='warning'),
    path('store/admin/delete/', views.delete_item, name='delete'),
    path('store/admin/item/<int:item_id>/', views.admin_review, name='admin_review'),
    path('store/admin/edit/', views.edit, name='edit'),
    path('store/admin/edit/save/', views.edit_review, name='edit_review'),
]
