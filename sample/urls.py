from django.urls import path
from . import views
from .views import CustomLoginView, SignUpView, CustomLogoutView, budget_create, password_reset

app_name = 'sample'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),   
    path('', views.home_view, name='home'),
    
    path('password_reset/', password_reset, name='password_reset'),
    
    
    #推し作成
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/create/', views.favorite_create, name='favorite_create'),
    path('favorite/edit/<int:favorite_id>/', views.favorite_edit, name='favorite_edit'),
    path('favorite/delete/<int:favorite_id>/', views.favorite_delete, name='favorite_delete'),

   
    #アイテム作成  
    path('item/create/<int:favorite_id>/', views.item_create, name='item_create'),
    
    path('item/list/<int:favorite_id>/', views.item_list_with_favorite, name='item_list_with_favorite'),
    
    path('item/edit/<int:item_id>/', views.item_edit, name='item_edit'),
    path('item/delete/<int:item_id>/', views.item_delete, name='item_delete'),
    path('share/<int:item_id>/', views.share_item, name='share_item'),
    path('shared_items/<int:favorite_id>/', views.shared_items, name='shared_items'),  # 共有されたアイテムの表示
    path('budget/create/', budget_create, name='budget_create'),

    
    path('items/purchased/', views.purchased_items, name='purchased_items'),
    path('item/purchased/<int:item_id>/', views.mark_item_purchased, name='mark_item_purchased'),  # 追加

    # 他のURLパターンもここに追加
]
