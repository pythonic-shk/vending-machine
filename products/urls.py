from django.urls import path
from .views import ProductCreateView, ProductShowView,\
    ProductUpdateView, ProductDeleteView, ProductBuyView

urlpatterns = [
    path('show', ProductShowView.as_view()),
    path('create', ProductCreateView.as_view()),
    path('delete', ProductDeleteView.as_view()),
    path('update', ProductUpdateView.as_view()),
    path('buy', ProductBuyView.as_view()),
]