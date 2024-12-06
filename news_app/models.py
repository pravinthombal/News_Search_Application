from django.db import models
from django.contrib.auth.models import User

class SearchQuery(models.Model):
    
    """Represents a search query made by a user.
    This model is used to store the search queries made by a user, including the search keyword and the
    timestamp of the last time the keyword was searched.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #  
    keyword = models.CharField(max_length=255)
    last_searched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword

class Article(models.Model):
    
    """    Represents an article fetched based on a user's search query.

    This model stores information about a news article related to a specific search query, including the 
    article's metadata (e.g., title, author, source) and its content.


    """
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='articles')
    source = models.CharField(max_length=500)
    author = models.CharField(max_length=500, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=900)
    url_to_image = models.URLField(max_length=900, null=True, blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    language= models.CharField(max_length=255, null=True, blank=True)
    category= models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
