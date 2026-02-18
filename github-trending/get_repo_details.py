#!/usr/bin/env python3
"""
获取GitHub项目详细信息
"""
import requests
import json
from datetime import datetime

def get_repo_info(owner, repo):
    """获取仓库详细信息"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Mozilla/5.0'
    }
    
    # 获取仓库信息
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'full_name': data.get('full_name'),
                'description': data.get('description'),
                'stars': data.get('stargazers_count'),
                'forks': data.get('forks_count'),
                'language': data.get('language'),
                'license': data.get('license', {}).get('name') if data.get('license') else None,
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'url': data.get('html_url'),
                'readme_url': f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
            }
    except Exception as e:
        print(f"Error fetching {owner}/{repo}: {e}")
        return None

def get_readme(owner, repo):
    """获取README内容"""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        'Accept': 'application/vnd.github.v3.raw',
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.text[:3000]  # 限制长度
    except:
        pass
    return None

def main():
    repos = [
        ("p-e-w", "heretic"),
        ("seerr-team", "seerr"),
        ("alibaba", "zvec"),
        ("SynkraAI", "aios-core"),
        ("ashishps1", "awesome-system-design-resources"),
        ("anthropics", "claude-quickstarts"),
        ("davila7", "claude-code-templates"),
        ("OpenCTI-Platform", "opencti"),
    ]
    
    results = []
    for owner, repo in repos:
        print(f"获取 {owner}/{repo} 信息...")
        info = get_repo_info(owner, repo)
        if info:
            readme = get_readme(owner, repo)
            info['readme_preview'] = readme
            results.append(info)
            print(f"  ⭐️ {info['stars']:,} stars")
    
    # 保存结果
    with open('/tmp/repo_details.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n获取了 {len(results)} 个项目详情")

if __name__ == "__main__":
    main()
