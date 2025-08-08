from django.urls import path
from .views import (
    RegisterView, AddBookView, DeleteBookView, BookListView, AddToCartView,
    CheckoutView, SaveBookView, BookReportView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('books/', BookListView.as_view()),
    path('books/add/', AddBookView.as_view()),
    path('books/<int:pk>/delete/', DeleteBookView.as_view()),

    path('cart/add/', AddToCartView.as_view()),
    path('cart/checkout/', CheckoutView.as_view()),
    path('saved/add/', SaveBookView.as_view()),

    path('report/books/', BookReportView.as_view()),
]
