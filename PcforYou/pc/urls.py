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
    

]