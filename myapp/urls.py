from django.urls import path
from myapp.views.cart_link_product_Views import show_user_cart_and_create_user_cart , modify_user_cart_item 
from myapp.views.categoryViews import categories_preview_and_or_creation, categories_modification_and_or_deletion
from myapp.views.paymentView import create_payment , delete_payment , retrieve_payment ,list_payments , update_payment
from myapp.views.productViews import modifying_existing_products, creation_of_products_and_preview_products
from myapp.views.registerViews import register
from myapp.views.shipping import shipping_detail, shipping_orders_adresses_preview_or_creation
from myapp.views.supplierViews import supplier_detail, supplier_list
from myapp.views.userView import UserViewSet
from myapp.views.loginView import CustomTokenObtainPairView
from myapp.views.cartViews import Show_cart_and_create_cart, Show_cart_and_modify_cart, lock_cart

# User view set
user_list = UserViewSet.as_view({
    'get': 'list',   
    'post': 'update', 
    'delete': 'destroy' 
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',  
    'put': 'update',    
})

urlpatterns = [
    # Authentication and registration URLs
    path('register/', register, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # User management URLs
    path('users/', user_list, name='user-list'),  
    path('users/<int:pk>/', user_detail, name='user-detail'), 

    # Category URLs
    path('categories/', categories_preview_and_or_creation, name='category-list'),
    path('categories/<int:pk>/', categories_modification_and_or_deletion, name='category-detail'),
    
    # Supplier URLs
    path('suppliers/', supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
    
    # Product URLs
    path('products/', creation_of_products_and_preview_products, name='product-list'),
    path('products/<int:pk>/', modifying_existing_products, name='product-detail'),
    
    # Cart URLs
    path('carts/', Show_cart_and_create_cart, name='cart-list'),
    path('carts/<int:pk>/', Show_cart_and_modify_cart, name='cart-detail'),
    path('carts/<int:cart_id>/lock/', lock_cart, name='lock_cart'),
    
    # CartItem URLs
    path('cart_link_products/' ,show_user_cart_and_create_user_cart, name='cart-item-list'),
    path('cart_link_products/<int:pk>/', modify_user_cart_item, name='cart-item-detail'),
    

    # Shipping URLs
    path('shippings/', shipping_orders_adresses_preview_or_creation, name='shipping-list'),
    path('shippings/<int:pk>/', shipping_detail, name='shipping-detail'),
    
    path("payments/", list_payments, name="list_payments"),
    path("payments/<int:payment_id>/", retrieve_payment, name="retrieve_payment"),
    path("payments/create/", create_payment, name="create_payment"),
    path("payments/<int:payment_id>/update/", update_payment, name="update_payment"),
    path("payments/<int:payment_id>/delete/", delete_payment, name="delete_payment"),

    ]
