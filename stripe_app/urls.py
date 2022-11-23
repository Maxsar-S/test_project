from django.urls import path

from . import views

app_name = 'stripe_app'

urlpatterns = [
    path('buy/<pk>/', views.CreateCheckoutSessionView.as_view(), name='create-session'),
    path('buy-order/', views.CreateCheckoutSessionOrderView.as_view(), name='create-order-session'),
    path('item/<pk>/', views.ItemLandingPageView.as_view(), name='item-template'),
    path('order-add/<int:item_id>/', views.add_to_order, name='add-to-order'),
    path('order-remove/<int:item_id>/', views.remove_from_order, name='remove-from-order'),
    path('order/', views.OrderLandingPageView.as_view(), name='order'),
]
