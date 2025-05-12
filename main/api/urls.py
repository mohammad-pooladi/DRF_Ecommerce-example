from django.urls import path, include

urlpatterns = [
    path('auth/', include(('main.auth.urls', 'auth'))),
    path('users/', include(('main.users.urls', 'users'))),
    path('payments/', include(('main.payments.urls', 'payments'))),
    path('orders/', include(('main.orders.urls', 'orders'))),
    path('products/', include(('main.products.urls', 'products'))),
]
