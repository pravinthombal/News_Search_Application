# News Search Application

This Django-based web application allows users to search for news articles based on keywords, view the results, and track their search history. It integrates with the [News API](https://newsapi.org/) to fetch the latest articles from various sources.

## Features

- **Search News**: Users can search for news articles by providing a keyword, stores result locally.
- **Search History**: Users can view their sorted search history based on "last searched keyword".
- **View Results**: Users can view detailed sorted results (Articles) for each search query (keyword) based uponthe “Date published”. 
- **Refresh Search**: Users can refresh the search results for a specific query (Keyword). While refreshing the search results, query only for new results, e.g., If we already
have results for “Tesla” till 31st December 2020. Fetched news articles published after
that and saved it in database
- **Admin Page**: Admin user can add, block and unblock user on Admin Page.
- **Login/Logout**: Users can log in and out to access their personalized search history.
authenticated user can see keywords that only they
searched.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- Django 3.x or later
- MySQL (or other database backend of your choice)
- A News API key (You can obtain it by signing up at [NewsAPI](https://newsapi.org/)).

## Installation

### 1. Clone the repository


git clone https://github.com/pravinthombal/News_Search_Application.git

### 2. Create a virtual environment

python3 -m venv myenv
source myenv/bin/activate   # On Windows: myenv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure the .env file

SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=3306
NEWS_API_KEY=your-news-api-key

### 5. Apply database migrations

python manage.py makemigartions
python manage.py migrate

### 6. Create a superuser

python manage.py createsuperuser

### 7. Run the development server

python manage.py runserver

## Usage
### Pages
- Search News Page (/search/): Enter a keyword and start searching for news articles.
- Search History (/history/): View a list of your past searches.
- View Results (/results/<search_query_id>/): View the detailed results of a specific search.
- Refresh Search (/refresh/<search_query_id>/): Refresh the search results for a specific search query.
- Admin (admin/): Admin Page to add, block and unblock user
- Login (login/): Login page to search keywords and see searched keyword history
- Logout (logout/): Logout page
- Register (/): Registration page

### Creating User, Logging in and Out
- Admin add user, blocks/unblock user
- To log in, use the login form available at /login/. The default authentication uses Django's AuthenticationForm.
- Once logged in, you can view your search history and search results.
- You can log out by visiting the /logout/ page.

## Time to complete Project

10 hours to complete project

## Experience of Working on the Project

- Enhanced skills in Django for building a robust web application.
- Search history and refresh Result, results filtering provided a personalized experience for each user
- Successfully integrated the News API, fetching and displaying real-time articles.
- Structured models for efficient data storage and retrieval.
- Separating functionality into clear methods and classes made development and debugging easier.
- Writing comprehensive docstrings and a README significantly improved project maintainability.
- Using .env files for managing sensitive data like API keys ensured better security.






