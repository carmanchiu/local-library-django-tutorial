from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
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

class BookListView(LoginRequiredMixin, generic.ListView):
    """Class Based View for books"""
    model = Book
    context_object_name = 'books'   # your own name for the list as a template variable
    paginate_by = 10

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

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('books')

# def author_list(request):
#     """Author list based on function-based view"""

#     # Generate author list
#     author_list = Author.objects.all()
#     num_authors = author_list.count()

#     context = {'author_list': author_list,
#                'num_authors': num_authors,
#                }
#     return render(request, 'author_list.html', context=context)

class AuthorListView(LoginRequiredMixin, generic.ListView):
    """Class based view for authors"""
    model = Author
    context_object_name = "authors"
    paginate_by = 5

# def author_detail(request, pk):
#     """Author details using function based view"""

#     # Generate author details
#     author = Author.objects.get(pk=pk)
#     context = {"author": author}
#     return render(request, "catalog/author_detail.html", context=context)

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
