from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='home'), 

    # admin section 

    path('admin-login/',views.admin_login,name="admin_login"),
    path('admin-logout/',views.admin_logout,name="admin_logout"),
    path('admin-dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('admin-dashboard/view-products/',views.viewproducts,name="view_products"),
    path('admin-dashboard/add-products/',views.add_product,name="add_products"),
    path('admin-dashboard/prebuilt-view/',views.prebuiltview,name="prebuilt_view"),
    path('admin-dashboard/prebuilt-detail/<slug:slug>/', views.prebuilt_pc_detail, name='prebuilt_pc_detail'),
    path('admin-dashboard/add-prebuilt/',views.add_prebuilt,name="add_prebuilt"),

    #users section

    path('cabinets/', views.cabinets, name="cabinets"),
    

]