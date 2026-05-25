from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    # AbstractUser already gives you: username, email, password, first_name, last_name
    # Nothing extra needed unless you want to add fields later
    
    def __str__(self):
        return self.username


class Collection(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField()  # link to full Wikipedia page
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='article_tags')
    tagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'tag')  # prevent duplicate tags on same article

    def __str__(self):
        return f"{self.tag.name} on {self.article.title}"


class UserNote(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    article = models.ForeignKey(Article, on_delete=models.OneToOneField, related_name='note')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.article.title}"


class SearchHistory(models.Model):
    query = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    searched_at = models.DateTimeField(auto_now_add=True)
    result_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: '{self.query}'"


class CollectionShare(models.Model):
    collection = models.OneToOneField(Collection, on_delete=models.CASCADE, related_name='share')
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Share for {self.collection.name}"
