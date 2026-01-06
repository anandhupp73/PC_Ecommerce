from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='home'), 

    # admin section 

    path('admin-login/',views.admin_login,name="admin_login"),
    path('admin-logout/',views.admin_logout,name="admin_logout"),
    path('admin/',views.admin_dashboard,name="admin_dashboard"),
    path('admin/view-products/',views.viewproducts,name="view_products"),
    path('admin/add-products/',views.add_product,name="add_products"),
    path("products/<int:product_id>/edit/", views.update_product, name="update_product"),
    path("products/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path('admin/prebuilt-view/',views.prebuiltview,name="prebuilt_view"),
    path('admin/prebuilt-detail/<slug:slug>/', views.prebuilt_pc_detail, name='prebuilt_pc_detail'),
    path('admin/add-prebuilt/',views.add_prebuilt,name="add_prebuilt"),
    path('admin/order-manage/', views.admin_order_manage, name='admin_order_manage'),
    path('admin/update_status/', views.update_order_status, name='update_order_status'),

    #users section

    path("profile/", views.profile_view, name="profile"),

    path('prebuilt-pcs/', views.prebuilt_list, name='prebuilt_list'),
    path('prebuilt/<int:id>/', views.prebuilt_detail, name='prebuilt_detail'),
    path('buy-prebuilt/<int:pc_id>/', views.buy_prebuilt, name='buy_prebuilt'),
    path('cabinets/', views.cabinets, name="cabinets"),
    path('cooling/',views.cooling,name="cooling"),
    path('ram/',views.ram,name="ram"),
    path('gpu/',views.gpu,name="gpu"),
    path('processor/',views.processors,name="processors"),
    path('monitors/',views.monitors,name="monitors"),
    path('motherboards/',views.motherboards,name="motherboards"),
    path('powersupply/',views.powersupply,name="powersupply"),
    path('storages/',views.storages,name="storages"),
    path('accessories/',views.accessories,name="accessories"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("cart/", views.cart_view, name="cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("cart/update/<int:cart_id>/<str:action>/", views.update_cart_quantity, name="update_cart"),
    path("cart/remove/<int:cart_id>/", views.remove_from_cart, name="remove_cart_item"),
    path('checkout/', views.checkout_cart, name='checkout_cart'),
    path("checkout/buy/<int:product_id>/",views.checkout_cart, name="buy_now_checkout"),
    path("orders/", views.orders_list, name="orders_list"),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path("pc-builder/", views.pc_builder, name="pc_builder"),
    path('api/gemini-compat-check/', views.gemini_compat_check, name='gemini-compat-check'),
    # ---------------------pdf-------------
    path("generate-pdf/",views.generate_report_pdf, name="generate_pdf"),


]