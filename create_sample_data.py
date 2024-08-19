import os
import django
from faker import Faker
import random

# Configure settings for project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')

# Load the Django project's settings
django.setup()

# Import models
from catalog.models import Genre, Book, BookInstance, Author, Language

# Initialize Faker Instance
fake = Faker()
Faker.seed(1) # Generate consistent sample data

# Create genres
def create_genre(n):
    for _ in range(n):
        name = fake.word()
        genre, created = Genre.objects.get_or_create(name=name)
        print(f"{'Created' if created else 'Exists'}: Genre - {genre.name}")

# Create authors
def create_author(n):
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        author, created = Author.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth = fake.date_of_birth(),
            date_of_death = fake.date_of_birth() if fake.boolean(chance_of_getting_true=25) else None
        )
        print(f"{'Created' if created else 'Exists'}: Author - {author}")

# Create books
def create_book(n):
    # Add languages
    languages = ["English", "Spanish", "German", "French"]
    for language in languages:
        Language.objects.get_or_create(name=language)

    for _ in range(n):
        title = fake.sentence(nb_words=4).rstrip('.')
        author = random.choice(Author.objects.all())
        summary = fake.text(max_nb_chars=500)
        isbn = fake.isbn13()
        book, created = Book.objects.get_or_create(
            title=title,
            author=author,
            summary=summary,
            isbn=isbn,
            )
        
        # Add genres to book
        genres = random.sample(list(Genre.objects.all()), k=random.randint(1, 3))
        book.genre.set(genres)

        # Add language to book
        book.language = random.choice(Language.objects.all())
        book.save()

        print(f"{'Created' if created else 'Exists'}: Book - {book.title}")

# Create book instances
def create_book_instance(n):
    for _ in range(n):
        book = random.choice(Book.objects.all())
        imprint = fake.company()
        status = random.choice(['m', 'o', 'a', 'r'])
        due_back = fake.future_date() if status == 'o' else None
    book_instance = BookInstance.objects.create(
        book=book,
        imprint=imprint,
        status=status,
        due_back=due_back,
    )
    print(f"Created: BookInstance - {book_instance}")

# Reset database
Language.objects.all().delete()
BookInstance.objects.all().delete()
Genre.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()

# Create sample data
create_genre(5)
create_author(10)
create_book(30)
create_book_instance(60)

print("\nSample data generated\n")