import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone
from .models import SearchQuery, Article
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Q  
from django.utils.timezone import now
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SearchForm, CustomUserCreationForm
from datetime import timedelta
from django.utils.timezone import make_aware, is_naive



def register(request):
    """
    Handles user registration.
    If the form is valid, saves the user and redirects to the login page.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})










def login_view(request):
    """Handles the user login functionality.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search_news')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})








def fetch_news_articles(keyword, last_published_at=None):
    
    """Fetch articles from the News API based on the provided keyword and date filter.
    Args:
        keyword (str): The search keyword.
        last_published_at (datetime, optional): The date after which to fetch articles. Defaults to None.
    Returns:
        list: A list of articles fetched from the News API.
    """
    if last_published_at:
        last_published_at += timedelta(seconds=1)
        published_after = last_published_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={settings.NEWS_API_KEY}&from={published_after}"
    else:
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={settings.NEWS_API_KEY}"

    response = requests.get(url)   
    if response.status_code == 200:     
        return response.json().get('articles', [])
    return []

def fetch_Source_objs():
    
    """Fetches the list of available news sources from the News API and returns them as a dictionary.

    Returns:
        dict: A dictionary where the keys are the names of news sources and the values are the source details 
        (e.g., language, category, etc.). If the request fails, returns an empty dictionary.
    """
    
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={settings.NEWS_API_KEY}"
    response = requests.get(url) 
    if response.status_code == 200:  
        sources = response.json().get('sources', []) 
        return {source['name']: source for source in sources}  
    return {}



@login_required
def search_news(request):
    
    """View function to perform a search for news articles based on user input, fetches new articles from an external API,
    and stores the results in the database for future access.

    This function handles the user's search from database by accepting various filtering criteria, such as keyword, date range,
    source name, language, and category. If the search is valid, it fetches articles from the external news API and 
    stores them in the database, displaying the results to the user. The search history is also saved for the user.

    Args:
        request (HttpRequest): The HTTP request object, which contains metadata about the request, including the 
        currently authenticated user.
    Returns:
        HttpResponse: Renders the 'search.html' template with search results, or the search page if no results are found 
        or the query is invalid.
    """
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            sources = fetch_Source_objs()  
            keyword = form.cleaned_data['keyword']
            print('keyword', keyword)
            start_date = form.cleaned_data['start_date']  
            end_date = form.cleaned_data['end_date']
            user_source_name = form.cleaned_data['source_name']
            language_name = form.cleaned_data['language_name']
            category_name = form.cleaned_data['category_name']
            
            if keyword:  
                search_query, created = SearchQuery.objects.get_or_create(user=request.user, keyword=keyword) #
                
                if created or search_query.last_searched_at < timezone.now() - timezone.timedelta(minutes=15):
                    search_query.last_searched_at = timezone.now()
                    search_query.save()

                    articles_data = fetch_news_articles(keyword)
                    if articles_data != []:
                        for article_data in articles_data:
                            source_name = article_data['source'].get('name', 'unknown') 
                            source_details = sources.get(source_name, {})  
                            
                            Article.objects.get_or_create(
                                search_query=search_query,
                                url=article_data['url'],
                                defaults={
                                    'source': source_name,
                                    'language': source_details.get('language', 'unknown'),  
                                    'category': source_details.get('category', 'unknown'), 
                                    'author': article_data.get('author'),
                                    'title': article_data['title'],
                                    'description': article_data['description'],
                                    'url_to_image': article_data.get('urlToImage'),
                                    'published_at': article_data['publishedAt'],
                                    'content': article_data['content']
                                }
                            )
                    else:
                        return render(request, 'news_app/search.html', {'keyword_not_found': "Articles not found related with keyword", 'keyword': keyword})
                
                else:
                    return render(request, 'news_app/search.html', {'search_time_limit': f"Please wait at least 15 minutes before searching '{keyword}' again.", 'keyword': keyword})

                articles = Article.objects.filter(search_query=search_query)
                if start_date:
                    start_date = datetime.combine(start_date, datetime.min.time())
                    start_date= make_aware(start_date)
                    articles = articles.filter(published_at__gte=start_date)

                if end_date:
                    end_date = datetime.combine(end_date, datetime.max.time())
                    end_date= make_aware(end_date)
                    articles = articles.filter(published_at__lte=end_date)

     
                if user_source_name:
                    articles = articles.filter(source__icontains=user_source_name)
                if language_name:
                    articles = articles.filter(language__iexact=language_name)
                if category_name:
                    articles = articles.filter(category__iexact=category_name)
                
                articles = articles.order_by('-published_at')

                return render(request, 'news_app/search.html', {'articles': articles, 'keyword': keyword})

    return render(request, 'news_app/search.html')



@login_required
def search_history(request):
    
    """View function to display the search history of the logged-in user sorted by "last_searched_at".

    Args:
        request (HttpRequest):  It contains metadata about the request, including the current logged-in user.

    Returns:
         HttpResponse: Renders the 'search_history.html' template with the user's search queries.
    """
    search_queries = SearchQuery.objects.filter(user=request.user).order_by('-last_searched_at')
    return render(request, 'news_app/search_history.html', {'search_queries': search_queries})




@login_required
def view_results(request, search_query_id):
    
    """View function to display the search results for a specific search query based on "date published".

    Args:
        request (HttpRequest): The HTTP request object. It contains metadata about the request,
        including the current logged-in user.
        search_query_id (int): The unique identifier for the search query, used to retrieve
        the relevant `SearchQuery` object.

    Returns:
        HttpResponse: Renders the 'view_results.html' template with the articles associated
        with the search query.
    """
    
    search_query = get_object_or_404(SearchQuery, id=search_query_id, user=request.user)
    articles = Article.objects.filter(search_query=search_query).order_by('-published_at')
    print('*******************: ',type(search_query.id))
    return render(request, 'news_app/view_results.html', {'articles': articles, 'keyword': search_query.keyword})

@login_required
def refresh_search(request, search_query_id):
    
    """View function to refresh the search results for a specific search query.
    This function retrieves a given search query, checks the most recent article associated with
    that query, and fetches new articles from the News API starting from the last published article's
    timestamp. It then adds the new articles to the database and renders the updated search results.
    for e.g., If we already have results for “Tesla” till 31st December 2020. Fetch news articles published after that.

    Args:
        request (HttpRequest): The HTTP request object. Contains metadata about the request, 
        including the currently authenticated user.
        search_query_id (int): The unique identifier for the search query, used to retrieve the 
        relevant `SearchQuery` object.

    Returns:
        HttpResponse: Renders the 'view_results.html' template with the newly fetched and 
        stored articles associated with the search query.
    """
    search_query = get_object_or_404(SearchQuery, id=search_query_id, user=request.user)
    keyword = search_query.keyword
    most_recent_article = Article.objects.filter(search_query=search_query).order_by('-published_at').first()
    if most_recent_article:
        last_published_at = most_recent_article.published_at
    # else:
    #     last_published_at = timezone.now() - timedelta(days=365)  # 1 year ago
    articles_data = fetch_news_articles(keyword, last_published_at)
    for article_data in articles_data:
        Article.objects.create(
            search_query=search_query,
            url=article_data['url'],
            source=article_data['source']['name'],
            author=article_data.get('author'),
            title=article_data['title'],
            description=article_data['description'],
            url_to_image=article_data.get('urlToImage'),
            published_at=article_data['publishedAt'],
            content=article_data['content']
        )
    articles = Article.objects.filter(search_query=search_query).order_by('-published_at')
    return render(request, 'news_app/view_results.html', {'articles': articles, 'keyword': search_query.keyword})