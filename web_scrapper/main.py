import requests
from bs4 import BeautifulSoup as bs


github_user_name = input("Enter github user name: ")
print(github_user_name)
url = "https://github.com/" + github_user_name
try:
    req = requests.get(url)
    req.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    soup = bs(req.content, "html.parser")
    avatar_tag = soup.find('img', {'class': 'avatar'})
    if avatar_tag is None:
        print("Error: Unable to find the profile image. The user may not exist or the page structure has changed.")
    else:
        profile_image = avatar_tag['src']
        print(profile_image)
except requests.exceptions.RequestException as e:
    print(f"Error: Unable to fetch the profile page. Details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
