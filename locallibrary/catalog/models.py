from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction)
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre ("
                                                      "e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book)
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief descriptiom of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href='
                                                             '"https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a sstring for Genre. This is required to display genre in Admin
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this paticular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object"""
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)


    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object"""
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    """
    Model representing a language
    """
    name = models.CharField(max_length=100, help_text="Input a languauge (e.g. English, Russian, French etc.")

    def __str__(self):
        return self.name


class Benefactor(models.Model):
    """
    Model representing a local benefactor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

