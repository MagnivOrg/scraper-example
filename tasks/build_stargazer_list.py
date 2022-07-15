from magniv.core import task
from utils.github_utils import _get_github_stargazers
import utils.redis_utils as store
from datetime import datetime
import os

@task(schedule="@weekly", description="Build/Update list of stargazers from repo")
def update_stargazers_for_repo():
	repo = None
	with open('tasks/repo.txt', 'r') as repos_file:
		repo = repos_file.read().strip()
	print("Repo to process:", repo)

	feteched_stars = _get_github_stargazers(
			repo, 
			os.environ.get("GITHUB_CLIENT_ID"), 
			os.environ.get("GITHUB_CLIENT_SECRET"))
	print(f'Found {len(feteched_stars)} stargazers')

	# Get stargazers from store
	r = store.Client()
	stargazers = r.get('stargazers') or []
	users_processed = {u.login for u in stargazers}

	for user in feteched_stars:
		if user["login"] in users_processed:
			continue

		user_data = {
			"login": user["login"],
			"html_url": user["html_url"],
			"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		}
		stargazers.append(user_data)
		users_processed.add(user["login"])	
	
	# Update stargazers in store
	r.set('stargazers', stargazers)

if __name__ == '__main__':
	update_stargazers_for_repo()