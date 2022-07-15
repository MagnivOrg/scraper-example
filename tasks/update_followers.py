from magniv.core import task
from datetime import datetime
from utils.github_utils import _get_follower_count
import utils.redis_utils as store
import os

@task(schedule="0 */2 * * *", description="Update follower count for each stargazer")
def update_followers():
	# Get stargazers from store
	r = store.Client()
	stargazers = r.get('stargazers')

	# Sort based on last_updated, oldest
	stargazers = sorted(stargazers, key=lambda x: datetime.strptime(x["last_updated"], '%Y-%m-%d %H:%M:%S'))

	updated_count = 0
	for idx, user in enumerate(stargazers):
		print(f'Updating user ID {idx}')
		follower_count = _get_follower_count(
			user["login"], 
			os.environ.get("GITHUB_CLIENT_ID"), 
			os.environ.get("GITHUB_CLIENT_SECRET"))

		if follower_count:
			print(f'  User {idx} has {follower_count} followers')
			stargazers[idx]["follower_count"] = int(follower_count)
			stargazers[idx]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			updated_count += 1
		else:
			# Probably hit rate limit
			print(f'Hit rate limit on user {idx}!')
			break

	# Save stargazers in store
	r.set('stargazers', stargazers)
	print(f'Updated {updated_count} users in store')

if __name__ == '__main__':
	update_followers()