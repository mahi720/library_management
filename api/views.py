from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Book, Cart, Issue, SavedBook
from .serializers import UserSerializer, BookSerializer, CartSerializer, IssueSerializer, SavedBookSerializer
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Librarian: Add Book
class AddBookView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != 'librarian':
            return Response({"error": "Forbidden"}, status=403)
        return super().post(request, *args, **kwargs)

# Librarian: Delete Book
class DeleteBookView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if request.user.role != 'librarian':
            return Response({"error": "Forbidden"}, status=403)
        return super().delete(request, *args, **kwargs)

# Browse books (with sorting and filtering)
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        sort = self.request.query_params.get('sort')
        if author:
            queryset = queryset.filter(author=author)
        if sort == 'most_issued':
            queryset = queryset.order_by('-issued_count')
        elif sort == 'least_issued':
            queryset = queryset.order_by('issued_count')
        return queryset

# Add to cart
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        book_id = request.data['book_id']
        cart, created = Cart.objects.get_or_create(user=user)
        cart.books.add(book_id)
        cart.save()
        return Response({"detail": "Book added to cart"})

# Checkout
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart or cart.books.count() == 0:
            return Response({"error": "Cart is empty"}, status=400)
        books = list(cart.books.all())
        for book in books:
            book.issued_count += 1
            book.save()
        bill = {
            "items": [{"title": b.title, "price": b.price} for b in books],
            "total": sum(float(b.price) for b in books)
        }
        issue = Issue.objects.create(
            user=user,
            return_date=timezone.now() + timedelta(days=14),
            bill=bill
        )
        issue.books.set(books)
        cart.books.clear()
        return Response({
            "issue_id": issue.id,
            "bill": bill,
            "return_date": issue.return_date
        })

# Save for later
class SaveBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        book_id = request.data['book_id']
        saved, created = SavedBook.objects.get_or_create(user=user)
        saved.books.add(book_id)
        saved.save()
        return Response({"detail": "Book saved"})

# Librarian: Book Report
class BookReportView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'librarian':
            return Book.objects.none()
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        sort = self.request.query_params.get('sort')
        if author:
            queryset = queryset.filter(author=author)
        if sort == 'most_issued':
            queryset = queryset.order_by('-issued_count')
        elif sort == 'least_issued':
            queryset = queryset.order_by('issued_count')
        return queryset
