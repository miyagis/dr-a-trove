from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_beers_by_user(user_name):
    url = f"https://untappd.com/user/{user_name}/beers?sort=highest_rated_you"

def get_beers(search_query, search_type="beer", search_sort="all"):
    # Set up ChromeDriver
    # service = Service('path/to/chromedriver')  # Update with your ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window

    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    url = f"https://untappd.com/search?q={search_query}&type={search_type}&sort={search_sort}"
    driver.get(url)

    # Wait for the content to load
    time.sleep(5)  # Adjust based on your internet speed

    # Get the page source
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the results container
    results_container = soup.find('div', class_='results-container')

    # Extract beer items
    beer_items = results_container.find_all('div', class_='beer-item')

    # Extract details for each beer
    beers = []
    for beer in beer_items:
        name = beer.find('p', class_='name').text.strip()
        brewery = beer.find('p', class_='brewery').text.strip()
        style = beer.find('p', class_='style').text.strip()
        abv = beer.find('p', class_='abv').text.strip()
        rating = beer.find('div', class_='caps').get('data-rating')
        url = beer.find('a', class_='label').get('href')
        
        beers.append({
            'name': name,
            'brewery': brewery,
            'style': style,
            'abv': abv,
            'rating': rating,
            'url': f"https://untappd.com{url}"
        })

    return beers

def get_breweries(search_query, search_type="brewery", search_sort="all"):
    # Set up ChromeDriver
    # service = Service('path/to/chromedriver')  # Update with your ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window

    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    url = f"https://untappd.com/search?q={search_query}&type={search_type}&sort={search_sort}"
    driver.get(url)

    # Wait for the content to load
    time.sleep(5)  # Adjust based on your internet speed

    # Get the page source
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the results container
    results_container = soup.find('div', class_='results-container')

    # Extract beer items
    beer_items = results_container.find_all('div', class_='beer-item')

    # Extract details for each beer
    breweries = []
    for item in beer_items:
        url = item.find('p', class_='name').find('a')['href']
        name = item.find('p', class_='name').get_text(strip=True)
        country = item.find_all('p', class_='style')[0].get_text(strip=True)
        style = item.find_all('p', class_='style')[1].get_text(strip=True)
        rating = item.find('div', class_='caps')['data-rating']
        
        breweries.append({
            'name': name,
            'style': style,
            'country': country,
            'rating': rating,
            'url': f"https://untappd.com{url}"
        })

    return breweries

def get_venues(search_query, search_type="venues", search_sort="all"):
    # Set up ChromeDriver
    # service = Service('path/to/chromedriver')  # Update with your ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode to avoid opening a browser window

    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    url = f"https://untappd.com/search?q={search_query}&type={search_type}&sort={search_sort}"
    driver.get(url)

    # Wait for the content to load
    time.sleep(5)  # Adjust based on your internet speed

    html = driver.page_source

    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    results_container = soup.find('div', class_='results-container')
    venues_items = results_container.find_all('div', class_='beer-item')

    venues = []
    for venue in venues_items:
        name = venue.find('p', class_='name').text.strip()
        style = venue.find_all('p', class_='style')[0].get_text(strip=True)
        location = venue.find_all('p', class_='style')[1].get_text(strip=True)
        url = venue.find('a', class_='label').get('href')

        venues.append({
            'name': name,
            'style': style,
            'location': location,
            'url': f"https://untappd.com{url}"
        })
    
    return venues

if __name__ == '__main__':
    get_breweries('Aalst')
    get_beers('Aalst')
    get_venues('Aalst')