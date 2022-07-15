from magniv.core import task
from datetime import datetime
import utils.redis_utils as store
import requests
import os

@task(schedule="@daily", description="Calculate top 10 influencers")
def calculate_influencers():
	# Get stargazers from store
	r = store.Client()
	stargazers = r.get('stargazers')

	# Sort based on follower_count
	stargazers = sorted(stargazers, key=lambda x: x.get("follower_count", -1))[::-1]
	top_ten = stargazers[:10]

	# Get previous top 10 influencers
	yesterday_top_ten = r.get('top_ten') or []

	top_ten_formatted = "\n".join([f'#{idx+1}: {u["login"]} ({u.get("follower_count", -1)}) - {u["html_url"]}' for idx,u in enumerate(top_ten)])

	if not yesterday_top_ten or any(y["login"] != top_ten[idx]["login"] for idx, y in enumerate(yesterday_top_ten)):
		print("New top 10!")
		# Update store with new top 10
		r.set('top_ten', top_ten)

		req = requests.post(os.environ.get("SLACK_WEBHOOK_URL"), json={"text": "New top 10 influencers!\n\n" + top_ten_formatted})
		# Send slack notification
	else:
		print("No change in top 10")
	print("===")
	print(top_ten_formatted)

if __name__ == '__main__':
	calculate_influencers()