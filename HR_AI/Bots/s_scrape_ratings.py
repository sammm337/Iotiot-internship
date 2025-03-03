import requests
from playwright.sync_api import sync_playwright
import Bots.s_extract_profiles as extract_profiles
def get_codeforces_rating(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url).json()
    if "result" in response:
        return response["result"][0]["rating"]
    return None

def get_leetcode_rating(username):
    url = f"https://leetcode-api-faisalshohag.vercel.app/{username}"
    try:
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
          # Debugging: print raw response
        
        if response.status_code == 200:
            data = response.json()
            rating = data.get("ranking", "Rating not found")
            return rating
        else:
            return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"
def get_codechef_rating(username):
    """Fetch CodeChef rating using the CodeChef API."""
    url = f"https://codechef-api.vercel.app/handle/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("currentRating", "Rating not found")
        return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"
       
def scrape_ratings(profiles):
    ratings = {}
    
    if "Codeforces" in profiles:
        cf_username = profiles["Codeforces"].split("/")[-1]
        ratings["Codeforces"] = get_codeforces_rating(cf_username)
        print(cf_username)

    if "LeetCode" in profiles:
        leet_username = profiles["LeetCode"].split("/")[-1]
        print(leet_username)
        ratings["LeetCode"] = get_leetcode_rating(leet_username)

    if "CodeChef" in profiles:  # Add this block
        codechef_username = profiles["CodeChef"].split("/")[-1]
        print(codechef_username)
        ratings["CodeChef"] = get_codechef_rating(codechef_username)

    return ratings

if __name__ == "__main__":
    profiles = extract_profiles.profiles
    print(profiles)
    ratings = scrape_ratings(profiles)
    print("Coding Ratings:", ratings)