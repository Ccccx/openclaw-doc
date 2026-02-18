#!/usr/bin/env python3
"""
获取GitHub Trending信息的脚本
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def get_github_trending(since='daily'):
    """获取GitHub trending页面"""
    url = f"https://github.com/trending?since={since}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return None

def parse_trending_html(html_content):
    """解析HTML获取trending项目"""
    soup = BeautifulSoup(html_content, 'html.parser')
    repos = []
    
    # 查找所有repo条目
    for article in soup.find_all('article', class_='Box-row'):
        try:
            # 跳过sponsors项目
            if article.find('span', class_='Label-sponsor'):
                continue
            
            # 获取repo链接
            link_elem = article.find('a', href=True)
            if not link_elem:
                continue
            
            href = link_elem['href']
            if not href.startswith('/'):
                continue
            
            # 解析作者/项目名
            parts = href.strip('/').split('/')
            if len(parts) < 2:
                continue
            
            author = parts[0]
            repo_name = parts[1]
            
            # 获取star数
            star_elem = article.find('a', href=re.compile(r'/stargazers'))
            stars = star_elem.get_text(strip=True) if star_elem else "0"
            
            # 获取今日增长
            today_elem = article.find('span', class_=re.compile(r'd-\S+'))
            today_stars = today_elem.get_text(strip=True) if today_elem else ""
            
            # 获取描述
            desc_elem = article.find('p', class_='color-fg-muted')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # 获取语言
            lang_elem = article.find('span', itemprop='programmingLanguage')
            language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
            
            repos.append({
                'author': author,
                'repo': repo_name,
                'full_name': f"{author}/{repo_name}",
                'url': f"https://github.com{href}",
                'stars': stars,
                'today_stars': today_stars,
                'description': description,
                'language': language
            })
        except Exception as e:
            print(f"Error parsing repo: {e}")
            continue
    
    return repos

def main():
    print("正在获取GitHub Trending信息...")
    html = get_github_trending('daily')
    
    if not html:
        print("获取失败")
        return
    
    repos = parse_trending_html(html)
    
    print(f"\n获取到 {len(repos)} 个项目:\n")
    for i, repo in enumerate(repos[:10], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐️ {repo['stars']} (今日+{repo['today_stars']})")
        print(f"   💻 {repo['language']}")
        print(f"   📝 {repo['description'][:100]}...")
        print()

if __name__ == "__main__":
    main()
