from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Generate counts for genres that have the word "fiction"
    num_genres = Genre.objects.count()

    # Generate counts for books that have the word "the"
    num_books_with_the = Book.objects.filter(title__iregex=r'the').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_the': num_books_with_the,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# def books_list(request):
#     """Books list (index) using function based view"""

#     # Generate book list
#     book_list = Book.objects.all()
    
#     context = {'book_list': book_list}
#     return render(request, 'book_list.html', context=context)

class BookListView(generic.ListView):
    """Class Based View for books"""
    model = Book
    context_object_name = 'books'   # your own name for the list as a template variable

    # def get_queryset(self): # can override queryset and get list of books from a certain author instead
    #     return Book.objects.filter(author=Author.objects.get(last_name="Riordan"))

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["num_books"] = Book.objects.count()
        return context
    
# def book_detail(request, pk):
#     """Book details using function based view"""

#     # Generate book details
#     book = Book.objects.get(pk=pk)
#     context = {"book": book}
#     return render(request, "catalog/book_detail.html", context=context)

class BookDetailView(generic.DetailView):
    model = Book