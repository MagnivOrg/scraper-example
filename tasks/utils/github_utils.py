import requests
import time
import random

def _get_github_stargazers(repo, client_id, client_secret, page=1):
    url = "https://api.github.com/repos/{}/stargazers?per_page=100&page={}".format(
        repo, page
    )
    resp = requests.get(url, auth=(client_id, client_secret))
    if resp.status_code != 200:
        print("! Failed on page {} for repo {}".format(page, repo))
        return []

    to_return = []
    response = resp.json()
    if len(response) < 100:
        return response
    
    print("Fetch the next page", page)
    time.sleep(1)
    next_page = _get_github_stargazers(
                repo,
                client_id,
                client_secret,
                page=page + 1,
            )
    return response + next_page

def _get_follower_count(login, client_id, client_secret):
    time.sleep(random.randrange(35,55) / 100.0)
    url = f'https://api.github.com/users/{login}'
    resp = requests.get(
        url,
        auth=(
            client_id,
            client_secret,
        ),
    )
    if resp.status_code != 200:
        print(f'Failed with error code {resp.status_code}... probably rate limit')
        print("----")
        print(resp.text)
        print("----")
        return None

    response = resp.json()
    return response.get("followers", None)