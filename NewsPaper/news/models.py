from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_profiles = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f'{self.user_profiles}'


class Category(models.Model):
    name_category = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    article = 'ART'
    news = 'NWS'

    CONTENT = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_content = models.CharField(max_length=3,
                                    choices=CONTENT,
                                    default=news)
    data_time_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_content = models.IntegerField(default=0)

    def like(self):
        self.rating_content += 1
        self.save()

    def dislike(self):
        self.rating_content -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    data_time_creation = models.DateTimeField(auto_now_add=True)
    rating_content = models.IntegerField(default=0)

    def like(self):
        self.rating_content += 1
        self.save()

    def dislike(self):
        self.rating_content -= 1
        self.save()
