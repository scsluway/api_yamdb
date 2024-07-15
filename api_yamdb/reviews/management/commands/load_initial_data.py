import csv
import os

from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


def fill_model_fields(filename, row):
    if filename == 'category':
        id, name, slug = row
        Category.objects.get_or_create(
            pk=id,
            name=name,
            slug=slug
        )
    elif filename == 'comments':
        id, review_id, text, author, pub_date = row
        Comment.objects.create(
            pk=id,
            review=Review.objects.get(pk=review_id),
            text=text,
            author=author,
            pub_date=pub_date
        )
    elif filename == 'genre_title':
        id, name, slug = row
        GenreTitle.objects.create(
            pk=id,
            name=name,
            slug=slug
        )
    elif filename == 'genre':
        id, name, year, category = row
        Genre.objects.create(
            pk=id,
            name=name,
            year=year,
            category=Category.objects.get(pk=category),
        )
    elif filename == 'title':
        id, name, year, category = row
        Title.objects.create(
            pk=id,
            name=name,
            year=year,
            category=Category.objects.get(pk=category),
        )
    elif filename == 'review':
        id, title_id, text, author, score, pub_date = row
        Review.objects.create(
            pk=id,
            title=Title.objects.get(pk=title_id),
            text=text,
            author=author,
            score=score,
            pub_date=pub_date
        )
    elif filename == 'users':
        id, username, email, role, bio, first_name, last_name = row
        User.objects.create(
            pk=id,
            username=username,
            email=email,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )


class Command(BaseCommand):
    help = 'Loads initial data into the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading initial data...'))
        directory = r'C:\Dev\api_yamdb\api_yamdb\static\data'
        for filename in os.listdir(directory):
            if (
                os.path.isfile(os.path.join(directory, filename))
                and filename.endswith('.csv')
            ):
                file_path = directory + '\\' + filename
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        fill_model_fields(filename[:-4], row)

        self.stdout.write(self.style.SUCCESS(
            'Начальные данные успешно загружены!'
        ))
