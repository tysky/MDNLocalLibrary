from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """
    View function for home page of site
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # The 'all()' is implied by default
    num_genres = Genre.objects.count()
    num_books_children = Book.objects.filter(title__icontains='Дети').count()

    #Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books, 'num_instances':num_instances,
                 'num_instances_available':num_instances_available, 'num_authors':num_authors,
                 'num_genres': num_genres, 'num_books_children': num_books_children}
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    # context_object_name = 'my_book_list' # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing title war
    # template_name = 'books/my_arbitrary_template_name_list.html' # Specify your own template name/location


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    # queryset = Author.objects.filter(first_name__icontains='Жюль')
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['test'] = 'available'
        return context