#!/usr/bin/env python3
"""
Generate comprehensive GitHub trending report
"""
import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

# Read the cached HTML
with open('/tmp/github_trending.html', 'r') as f:
    html_content = f.read()

# Parse repos from the cached HTML
soup = BeautifulSoup(html_content, 'html.parser')
repos = []

# Find all repo entries - more flexible parsing
for article in soup.find_all('article', class_='Box-row'):
    try:
        # Skip sponsored
        if article.find('span', class_='Label-sponsor'):
            continue
        
        # Find repo link
        links = article.find_all('a', href=True)
        repo_link = None
        for link in links:
            href = link['href']
            if href.startswith('/') and '/' in href[1:] and 'sponsors' not in href:
                parts = href.strip('/').split('/')
                if len(parts) >= 2 and not any(x in href.lower() for x in ['wiki', 'issues', 'pulls', 'actions', 'settings']):
                    repo_link = href
                    break
        
        if not repo_link:
            continue
            
        parts = repo_link.strip('/').split('/')
        author, repo_name = parts[0], parts[1]
        
        # Get description
        desc_elem = article.find('p', class_='color-fg-muted')
        description = desc_elem.get_text(strip=True) if desc_elem else ""
        
        # Get language
        lang_elem = article.find('span', itemprop='programmingLanguage')
        language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
        
        # Get stars
        star_links = article.find_all('a', href=True)
        stars_text = ""
        for sl in star_links:
            if '/stargazers' in sl.get('href', ''):
                stars_text = sl.get_text(strip=True)
                break
        
        repos.append({
            'author': author,
            'repo': repo_name,
            'full_name': f"{author}/{repo_name}",
            'url': f"https://github.com{repo_link}",
            'stars': stars_text,
            'language': language,
            'description': description
        })
    except Exception as e:
        print(f"Error: {e}")
        continue

print(f"Found {len(repos)} trending repos")

# Now get API details for each
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Mozilla/5.0'
}

detailed_repos = []
for repo in repos[:10]:
    try:
        url = f"https://api.github.com/repos/{repo['author']}/{repo['repo']}"
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            repo['stars_count'] = data.get('stargazers_count', 0)
            repo['forks_count'] = data.get('forks_count', 0)
            repo['description'] = data.get('description') or repo['description']
            repo['language'] = data.get('language') or repo['language']
            repo['license'] = data.get('license', {}).get('name') if data.get('license') else None
            repo['topics'] = data.get('topics', [])[:5]
            repo['created_at'] = data.get('created_at', '')[:10]
            repo['updated_at'] = data.get('updated_at', '')[:10]
            
            # Try to get README
            readme_url = f"https://api.github.com/repos/{repo['author']}/{repo['repo']}/readme"
            rm_resp = requests.get(readme_url, headers=headers, timeout=30)
            if rm_resp.status_code == 200:
                readme_data = rm_resp.json()
                content = readme_data.get('content', '')
                import base64
                try:
                    readme_content = base64.b64decode(content).decode('utf-8')[:2000]
                    repo['readme'] = readme_content
                except:
                    repo['readme'] = ""
            else:
                repo['readme'] = ""
        else:
            repo['stars_count'] = 0
            repo['readme'] = ""
    except Exception as e:
        print(f"Error getting details for {repo['full_name']}: {e}")
        repo['stars_count'] = 0
        repo['readme'] = ""
    
    detailed_repos.append(repo)
    print(f"Processed: {repo['full_name']} - {repo.get('stars_count', 0)} stars")

# Save detailed data
with open('/tmp/detailed_repos.json', 'w') as f:
    json.dump(detailed_repos, f, indent=2, ensure_ascii=False)

print(f"\nTotal repos processed: {len(detailed_repos)}")
