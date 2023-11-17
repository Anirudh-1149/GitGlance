import requests

def lambda_handler(event, context):
    github_token = 'TOKEN'

    url = "https://api.github.com/search/issues"
    params = {
        'q': 'is:open',  # Filter for open issues
        'per_page': 100   # Number of results per page
    }
    
    # Add the authentication token to the headers
    headers = {
        'Authorization': f'Bearer {github_token}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        issues_data = response.json()
        issues_list = []
    
        for issue in issues_data['items'][:10]:
            repo_url = issue['repository_url']
            title = issue['title']

            # Send a GET request for languages
            languages_response = requests.get(repo_url + "/languages", headers=headers)
            if languages_response.status_code == 200:
                languages_data = languages_response.json()
                languages = list(languages_data.keys())
            else:
                languages = []
    
            # Send a GET request for labels
            labels_response = requests.get(repo_url + "/labels", headers=headers)
            if labels_response.status_code == 200:
                labels_data = labels_response.json()
                labels = [label['name'] for label in labels_data]
            else:
                labels = []
    
            # Send a GET request for forks
            forks_response = requests.get(repo_url + "/forks", headers=headers)
            if forks_response.status_code == 200:
                forks_data = forks_response.json()
                forks_count = len(forks_data)
            else:
                forks_count = 0
    
            # Send a GET request for topics
            topics_response = requests.get(repo_url + "/topics", headers=headers)
            if topics_response.status_code == 200:
                topics_data = topics_response.json()
                topics = topics_data.get('names', [])
            else:
                topics = []

            # Send a GET request for stargazers
            stargazers_response = requests.get(repo_url + "/stargazers", headers=headers)
            if stargazers_response.status_code == 200:
                stargazers_data = stargazers_response.json()
                stargazers_count = len(stargazers_data)
            else:
                stargazers_count = 0
    
            issue_info = {
                'repo_url': repo_url,
                'languages': languages,
                'labels': labels,
                'forks_count': forks_count,
                'topics': topics,
                'stargazers_count': stargazers_count
            }
    
            # Add the dictionary to the array
            issues_list.append(issue_info)
        print(issues_list)
    
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    print(event)
