# library_management

   Features – Library Management API
   This backend project allows users and librarians to manage, browse, and issue books with secure authentication and a robust set of features.

1. Authentication

  User Registration: Any user can register using a username and password.
  User Login: Registered users can log in to receive a JWT token for secure access to protected routes.
  Role Management: Differentiates between regular users (customers) and librarians for authorization.

2. Librarian Features

   Add Book: Librarian can add a new book with details (Title, Author, ISBN, Price, Cover Image URL).
   Delete Book: Librarian has the ability to delete any book from the library.
   Book Issue Report: Generates a report showing how many times each book has been issued.
   Sort options: Most issued, Least issued, By author

3. Customer/General User Features

   Browse Books: Anyone can view the list of available books.
   Sort options: Most issued, Least issued, By author
   Add to Cart: Users can add books to their cart for later checkout.
   Checkout: Issue all books in the cart.
   Records issue date and sets a return date (e.g., 14 days later).
   Generates a simple bill summary highlighting essential info.
   Save for Later: Users can save books to a “view later” list.

4. Security
   
   JWT Token Authentication: All protected endpoints require a valid JWT access token in the Authorization header for every request.

5. Quick Test Endpoints

   Register: POST /api/register/
   Login: POST /api/login/
   List Books: GET /api/books/
   Add Book: POST /api/books/add/ (Librarian only)
   Delete Book: DELETE /api/books/{id}/ (Librarian only)
   Add to Cart: POST /api/cart/add/
   Checkout: POST /api/cart/checkout/
   Save for Later: POST /api/save-later/

6. Setup & Usage Summary

   Clone the repo, install dependencies, set up the database.
   Use registration and login to access your JWT token.

   Visit each endpoint using Postman or any HTTP client with your token.

