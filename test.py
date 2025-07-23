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
    parser = argparse.ArgumentParser(description='Twitter Metro Data Scraper')
    parser.add_argument('--since', type=str, default="", 
                       help='Start date (YYYY-MM-DD format, default: 2024-01-01)')
    parser.add_argument('--until', type=str, default="", 
                       help='End date (YYYY-MM-DD format, default: 2024-12-31)')
    parser.add_argument('--city', type=str, required=True,
                       help='City configuration key (e.g., seoul, hongkong)')
    return parser.parse_args()


def validate_city_config(city_key, cities_config):
    """Validate if the specified city exists in configuration"""
    if city_key not in cities_config:
        print(f"错误：城市配置 '{city_key}' 不存在")
        print(f"可用的城市配置：{', '.join(cities_config.keys())}")
        sys.exit(1)
    return cities_config[city_key]


# ==================== Parse Command Line Arguments ====================
args = parse_arguments()

# Proxy settings (uncomment and fill in proxy information if needed)
proxy = {
    "host": "127.0.0.1",    # Proxy server IP address
    "port": "8235",         # Proxy server port
}

# ==================== Basic Configuration ====================
proxy = None # add proxy settings. IF the proxy is public, you can provide empty username and password
cookies = None # current library implementation depends on Nodriver cookies handling.
cookies_directory = 'cookies' # directory where you want to save/load the cookies 'username_cookies.dat'
user_agent = None
disable_images = True # disable loading images while fetching
env_path = '.env' # .env path where twitter account credentials are
n_splits = 42 # set the number of splits that you want to perform on the date interval (the bigger the interval and the splits, the bigger the scraped tweets)
concurrency = 10 # tweets and profiles fetching run in parallel (on multiple browser tabs at the same time). Adjust depending on resources.
headless = False
scroll_ratio = 100 # scrolling ratio while fetching tweets. adjust between 30 to 200 to optimize tweets fetching.

# ==================== Load City Configuration ====================
print("Loading city configuration...")
cities_config = load_cities_config()

# Select city
selected_city_key = args.city
selected_city_config = validate_city_config(selected_city_key, cities_config)

# Get relevant parameters from configuration
metro_keywords = selected_city_config['metro_keywords']
geocode = selected_city_config.get('geocode')  # Use .get() to handle null values
city_name = selected_city_config['city_name']
language = selected_city_config.get('language', None)

print(f"\nSelected city: {city_name}")
if geocode:
    print(f"Geocode: {geocode}")
else:
    print("Geocode: None (no geographic restrictions)")
print(f"Number of keywords: {len(metro_keywords)}")

# ==================== Search Configuration ====================
# Search time range (use command line arguments or defaults)
since_date = args.since if args.since else None        # Start date from command line argument
until_date = args.until if args.until else None        # End date from command line argument

# Display date range information
if since_date and until_date:
    print(f"Date range: {since_date} to {until_date}")
elif since_date:
    print(f"Date range: from {since_date} onwards")
elif until_date:
    print(f"Date range: up to {until_date}")
else:
    print("Date range: all time (no time restrictions)")

# Tweet filtering conditions
# min_likes = 5                  # Minimum number of likes
# min_retweets = 2               # Minimum number of retweets
# min_replies = 1                # Minimum number of replies

# ==================== Output Configuration ====================
save_directory = f'{selected_city_key}_metro_data'      # Data save directory

# Generate filename with date suffix, handling empty dates
if since_date and until_date:
    custom_filename = f'{selected_city_key}_metro_tweets_{since_date}_to_{until_date}.csv'
elif since_date:
    custom_filename = f'{selected_city_key}_metro_tweets_{since_date}_onwards.csv'
elif until_date:
    custom_filename = f'{selected_city_key}_metro_tweets_until_{until_date}.csv'
else:
    custom_filename = f'{selected_city_key}_metro_tweets_all_time.csv'

# Ensure output directory exists
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

print(f"Output file: {custom_filename}")

# ==================== Initialize Scweet Scraper ====================
print("Initializing Twitter scraper...")
scweet = Scweet(proxy,
                cookies, 
                cookies_directory, 
                user_agent, 
                disable_images, 
                env_path,
                n_splits=n_splits, 
                concurrency=concurrency, 
                headless=headless, 
                scroll_ratio=scroll_ratio)

# ==================== Start Data Scraping ====================
print(f"\nStarting to scrape {city_name} metro-related tweets...")
print(f"Search keywords: {metro_keywords}")

# Display geographic and time information
if geocode:
    print(f"Geographic range: {city_name} ({geocode})")
else:
    print("Geographic range: worldwide (no geographic restrictions)")

if since_date and until_date:
    print(f"Time range: {since_date} to {until_date}")
elif since_date:
    print(f"Time range: from {since_date} onwards")
elif until_date:
    print(f"Time range: up to {until_date}")
else:
    print("Time range: all time (no time restrictions)")

# Execute scraping task
all_results = scweet.scrape(
    since=since_date,              # Start date (can be None)
    until=until_date,              # End date (can be None)
    words=metro_keywords,          # Search keywords list
    to_account=None,               # Tweets to specific account (None means no restriction)
    from_account=None,             # Tweets from specific account (None means no restriction)
    limit=90000,                   # Tweet scraping limit
    display_type="Recent",         # Display type: "Top"(popular), "Latest"(latest), "Recent"(recent)
    resume=True,                   # Whether to resume from last interruption (avoid duplicate scraping)
    filter_replies=False,          # Whether to filter reply tweets
    proximity=False,               # Whether to use proximity search
    geocode=geocode,               # Geocode restriction
    save_dir=save_directory,       # Save directory
    custom_csv_name=custom_filename # Custom filename
)

# ==================== Output Result Statistics ====================
print(f"\nScraping completed!")
print(f"Total tweets retrieved: {len(all_results)}")
print(f"Data saved to: {save_directory}/{custom_filename}")


print("\nScript execution completed!")


"""
python test.py --since "2024-01-01" --until "2024-12-31" --city seoul


chmod +x auto.sh

# 使用默认日期范围（2021-01-01 到 2021-05-31）和首尔配置
./auto.sh

# 指定日期范围，使用首尔配置
./auto.sh 2024-01-01 2024-12-31

# 如果想爬取香港数据，修改脚本中的 CITY="hongkong"
"""