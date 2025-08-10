from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
import requests
from django.core.paginator import Paginator
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required


# Create your views here.

API_KEY = "AIzaSyDtMDChAEL5SWcnjx1IwtAhU2qDsWw0iNg"

@login_required
def index(request):
    popular_response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q=subject:*&orderBy=newest&maxResults=10&key={API_KEY}'
    )
    popular_books_raw = popular_response.json().get('items', [])
    popular_books = [book for book in popular_books_raw if book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail') and book.get('volumeInfo', {}).get('description')]

    latest_response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q=subject:*&orderBy=relevance&maxResults=10&key={API_KEY}'
    )
    latest_books_raw = latest_response.json().get('items', [])
    latest_books = [book for book in latest_books_raw if book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail') and book.get('volumeInfo', {}).get('description')]

    return render(request, 'index.html', {
        'popular_books': popular_books,
        'latest_books': latest_books,
    })

@login_required
def book_detail(request, book_id):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={API_KEY}')
    book = response.json()
    return render(request, 'description.html', {'book': book})




def signup(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm_password']


        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('index')
    return render(request, 'registration/registration.html')

@login_required
def search_books(request):
    query = request.GET.get('q', '')
    books = []

    if query:
        # Your Google Books API call or DB query
        service = build('books', 'v1', developerKey=API_KEY)
        result = service.volumes().list(q=query, maxResults=40).execute()
        books = result.get('items', [])

    # Pagination: Show 10 books per page
    paginator = Paginator(books, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'query': query,
        'books': page_obj,  # This is now paginated
        'page_obj': page_obj
    })
