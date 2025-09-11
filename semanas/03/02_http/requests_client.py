# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

# pip install requests
import requests

# GET com parâmetros
response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'language:python stars:>10000', 'sort': 'stars'},
    headers={'Accept': 'application/vnd.github.v3+json'}
)

data = response.json()
print(f"Total de repositórios: {data['total_count']}\n")

# Top 3 repos Python
for repo in data['items'][:3]:
    print(f"⭐ {repo['stargazers_count']:,} - {repo['full_name']}")
    print(f"   {repo['description'][:60]}...")