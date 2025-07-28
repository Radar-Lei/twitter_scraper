from scweet import Scweet
from time import sleep
import os
import json
import sys
import argparse


def load_cities_config(config_file='cities_config.json'):
    """Load cities configuration file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file {config_file} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Configuration file {config_file} format is incorrect")
        sys.exit(1)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Twitter Metro Data Concurrent Scraper (by Cities)')
    parser.add_argument('--cities', type=str, nargs='*', 
                       help='Specify cities to scrape (e.g.: seoul hongkong), if not specified, scrape all cities')
    parser.add_argument('--limit', type=int, default=90000,
                       help='Tweet limit per city (default: 90000)')
    parser.add_argument('--resume', action='store_true',
                       help='Enable resume mode to continue from last interruption')
    parser.add_argument('--display_type', type=str, default="Recent",
                       choices=["Top", "Recent", "Latest", "image"],
                       help='Tweet display type (default: Recent)')
    return parser.parse_args()


def validate_cities(city_keys, cities_config):
    """Validate if specified cities exist in configuration"""
    valid_cities = {}
    invalid_cities = []
    
    for city_key in city_keys:
        if city_key in cities_config:
            valid_cities[city_key] = cities_config[city_key]
        else:
            invalid_cities.append(city_key)
    
    if invalid_cities:
        print(f"Error: The following city configurations do not exist: {', '.join(invalid_cities)}")
        print(f"Available city configurations: {', '.join(cities_config.keys())}")
        sys.exit(1)
    
    return valid_cities


# Parse command line arguments
args = parse_arguments()

# Basic configuration
proxy = None  # Add proxy settings if needed
cookies = None
cookies_directory = 'cookies'
user_agent = None
disable_images = True
env_path = '.env'
concurrency = 2  # Number of concurrent cities
headless = False
scroll_ratio = 100

# Load city configuration
print("Loading city configuration...")
cities_config = load_cities_config()

# Determine cities to scrape
if args.cities:
    # Use specified cities
    selected_cities = validate_cities(args.cities, cities_config)
    print(f"Specified cities to scrape: {', '.join(args.cities)}")
else:
    # Scrape all configured cities
    selected_cities = cities_config
    print(f"Scraping all cities: {', '.join(cities_config.keys())}")

print(f"Total cities to scrape: {len(selected_cities)}")

# Display scraping information
for city_key, city_config in selected_cities.items():
    city_name = city_config['city_name']
    metro_keywords = city_config['metro_keywords']
    geocode = city_config.get('geocode')
    
    print(f"\nCity: {city_name} ({city_key})")
    print(f"  Keywords: {metro_keywords}")
    if geocode:
        print(f"  Geographic range: {geocode}")
    else:
        print(f"  Geographic range: No restrictions")

# Output configuration
save_directory = "metro_data"  # Unified data save directory

# Ensure output directory exists
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

print(f"\nOutput directory: {save_directory}")
print(f"Limit per city: {args.limit} tweets")
print(f"Resume mode: {'Enabled' if args.resume else 'Disabled'}")
print(f"Display type: {args.display_type}")

# Initialize Scweet scraper
print("\nInitializing Twitter scraper...")
scweet = Scweet(proxy,
                cookies, 
                cookies_directory, 
                user_agent, 
                disable_images, 
                env_path,
                n_splits=1,  # No longer using time splitting
                concurrency=concurrency, 
                headless=headless, 
                scroll_ratio=scroll_ratio)

# Start data scraping
print(f"\nStarting concurrent scraping for {len(selected_cities)} cities metro-related tweets...")
print("=" * 60)

# Execute city concurrent scraping task
all_results = scweet.scrape_cities(
    cities_config=selected_cities,    # Selected city configurations
    words=None,                      # Use keywords from each city configuration
    to_account=None,                 # No specific target account restriction
    from_account=None,               # No specific source account restriction
    limit=args.limit,                # Tweet scraping limit
    display_type=args.display_type,  # Display type
    resume=args.resume,              # Resume mode
    filter_replies=False,            # Do not filter reply tweets
    proximity=False,                 # Do not use proximity search
    save_dir=save_directory          # Save directory
)

# Output result statistics
print("\n" + "=" * 60)
print("Scraping completed!")
print(f"Total cities scraped: {len(selected_cities)}")

total_tweets = 0
for city_key, city_results in all_results.items():
    tweet_count = len(city_results)
    total_tweets += tweet_count
    city_name = selected_cities[city_key]['city_name']
    csv_file = f"{save_directory}/{city_key}_metro_tweets.csv"
    print(f"  {city_name} ({city_key}): {tweet_count} tweets -> {csv_file}")

print(f"\nTotal: {total_tweets} tweets")
print(f"Data saved in: {save_directory}/ directory")

print("\nScript execution completed!")


"""
Usage examples:

# Scrape all cities (seoul and hongkong)
python test.py

# Only scrape Seoul
python test.py --cities seoul

# Scrape Seoul and Hong Kong with resume mode enabled
python test.py --cities seoul hongkong --resume

# Scrape all cities with limit of 5000 tweets per city
python test.py --limit 5000

# Scrape popular tweets
python test.py --display_type Top
"""