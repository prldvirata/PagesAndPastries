from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('search', views.search, name='search'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

]