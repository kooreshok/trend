import requests
import json
import os
from datetime import datetime, timezone

# --- CONFIGURATION ---
# IMPORTANT: Never commit API keys to your repository. Use environment variables.
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '04b0c1441d4042cf9f5cc754da6ffb0d')
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '6532d7cbac8891884e5ccc4a2013138d')

# Output path for the JSON file
OUTPUT_PATH = os.path.join(os.path.dirname(__name__), '..', 'public', 'data', 'trends.json')
NUM_ITEMS = 10

# --- DATA FETCHING FUNCTIONS ---

def get_tech_news():
    """Fetches top 10 tech headlines from NewsAPI."""
    print("Fetching tech news...")
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize={NUM_ITEMS}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        articles = response.json().get('articles', [])
        
        processed_data = []
        for i, article in enumerate(articles):
            processed_data.append({
                "rank": i + 1,
                "image": article.get('urlToImage', 'https://via.placeholder.com/150'), # Placeholder if no image
                "title": article.get('title'),
                "description": article.get('description', 'No description available.'),
                "source_link": article.get('url')
            })
        print(f"Successfully fetched {len(processed_data)} tech news items.")
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tech news: {e}")
        return []

def get_trending_movies():
    """Fetches top 10 trending movies from TMDB."""
    print("Fetching trending movies...")
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movies = response.json().get('results', [])[:NUM_ITEMS]
        
        processed_data = []
        for i, movie in enumerate(movies):
            processed_data.append({
                "rank": i + 1,
                "image": f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}" if movie.get('poster_path') else 'https://via.placeholder.com/150',
                "title": movie.get('title'),
                "description": movie.get('overview', 'No description available.')[:150] + '...', # Truncate long descriptions
                "source_link": f"https://www.themoviedb.org/movie/{movie.get('id')}"
            })
        print(f"Successfully fetched {len(processed_data)} trending movies.")
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending movies: {e}")
        return []

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("Starting data ingestion process...")
    
    # Get current UTC time for the timestamp
    last_updated_utc = datetime.now(timezone.utc).strftime("%B %d, %Y, %H:%M %Z")

    # The final data structure to be saved as JSON
    final_data = {
        "last_updated": last_updated_utc,
        "categories": {
            "tech_news": get_tech_news(),
            "trending_movies": get_trending_movies()
        }
    }
    
    # Write the data to the JSON file
    try:
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(final_data, f, indent=2)
        print(f"Successfully wrote data to {OUTPUT_PATH}")
    except IOError as e:
        print(f"Error writing to file: {e}")