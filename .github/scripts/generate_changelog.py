import json
import os
import urllib.request
from datetime import datetime

REPOS = [
    {'slug': 'moviesxmovies/MoviesXMovies', 'label': 'Main', 'icon': '🎬'},
    {'slug': 'moviesxmovies/MoviesXMoviesBackend', 'label': 'Backend', 'icon': '⚙️'},
    {'slug': 'moviesxmovies/MoviesXMoviesFrontend', 'label': 'Frontend', 'icon': '🖥️'},
]

# Mirrors your .github/release.yml categories
CATEGORIES = [
    {'title': '🚀 Features', 'prefixes': ['feat', 'feature']},
    {'title': '🐛 Fixes', 'prefixes': ['fix', 'bug']},
    {'title': '🧪 Tests', 'prefixes': ['test', 'tests']},
    {'title': '🧰 Maintenance', 'prefixes': ['chore', 'ci', 'build']},
]
IGNORE_PREFIXES = ['ignore']

TOKEN = os.environ['GH_TOKEN']
OUT = 'docs/changelog.md'


def gh_get(url: str):
    req = urllib.request.Request(
        url,
        headers={
            'Authorization': f'Bearer {TOKEN}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def fetch_releases(slug: str) -> list:
    return gh_get(f'https://api.github.com/repos/{slug}/releases?per_page=100')


def parse_date(iso: str) -> datetime:
    return datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S')


def parse_release_body(body: str) -> dict:
    """
    Parse a GitHub auto-generated release body into categorized sections.
    GitHub renders them as:
        ## 🚀 Features
        * feat: something by @user in #123
        ## 🐛 Fixes
        * fix: something by @user in #456
        ## New Contributors
        ...
        **Full Changelog**: ...
    Returns a dict like:
        {
            "🚀 Features":    ["* feat: something by @user in #123", ...],
            "🐛 Fixes":       [...],
            "full_changelog": "https://...",
            "new_contributors": ["* @user made their first contribution in #7", ...],
        }
    """
    if not body:
        return {}

    result = {}
    current = None
    full_changelog = None
    new_contributors = []

    for raw_line in body.replace('\r\n', '\n').split('\n'):
        line = raw_line.strip()

        if line.startswith('## '):
            current = line[3:].strip()
            if current not in result:
                result[current] = []

        elif line.lower().startswith('**full changelog**'):
            # e.g. **Full Changelog**: https://github.com/.../compare/v1.0.0...v1.1.0
            parts = line.split(':', 1)
            if len(parts) == 2:
                full_changelog = parts[1].strip()

        elif current == 'New Contributors' and line.startswith('*'):
            new_contributors.append(line)

        elif current and line.startswith('*'):
            result[current].append(line)

    result['_full_changelog'] = full_changelog
    result['_new_contributors'] = new_contributors
    return result


def should_ignore(entry_line: str) -> bool:
    """Skip lines whose PR title starts with an ignored prefix."""
    text = entry_line.lstrip('* ').lower()
    return any(text.startswith(p) for p in IGNORE_PREFIXES)


def format_release(entry: dict) -> str:
    rel = entry['release']
    label = entry['label']
    icon = entry['icon']
    slug = entry['slug']
    date = parse_date(rel['published_at']).strftime('%B %d, %Y')
    tag = rel['tag_name']
    name = rel.get('name') or tag
    url = rel['html_url']
    pre = ' _(pre-release)_' if rel.get('prerelease') else ''

    lines = []
    lines.append(f'## {icon} [{label}] {name}{pre}\n')
    lines.append(
        f'**Repo:** `{slug}` &nbsp;·&nbsp; '
        f'**Tag:** `{tag}` &nbsp;·&nbsp; '
        f'**Released:** {date} &nbsp;·&nbsp; '
        f'[View on GitHub]({url})\n'
    )

    parsed = parse_release_body(rel.get('body', ''))

    if parsed:
        # Render known categories in order, using titles from CATEGORIES
        # but matching against what GitHub actually put in the release body
        rendered_any = False
        for cat in CATEGORIES:
            # Find the matching section in the parsed body by title
            section_lines = parsed.get(cat['title'], [])
            visible = [l for l in section_lines if not should_ignore(l)]
            if visible:
                lines.append(f'\n### {cat["title"]}\n')
                for item in visible:
                    lines.append(f'{item}\n')
                rendered_any = True

        # Render any sections from the release body NOT in our known categories
        # (future-proofing — e.g. if GitHub adds a new group)
        known_titles = {c['title'] for c in CATEGORIES} | {'New Contributors'}
        for section_title, section_lines in parsed.items():
            if section_title.startswith('_'):
                continue
            if section_title not in known_titles:
                visible = [l for l in section_lines if not should_ignore(l)]
                if visible:
                    lines.append(f'\n### {section_title}\n')
                    for item in visible:
                        lines.append(f'{item}\n')
                    rendered_any = True

        if not rendered_any:
            lines.append('\n_No categorized changes found._\n')

        # New contributors
        if parsed.get('_new_contributors'):
            lines.append('\n### 👋 New Contributors\n')
            for c in parsed['_new_contributors']:
                lines.append(f'{c}\n')

        # Full changelog compare link
        if parsed.get('_full_changelog'):
            lines.append(f'\n**Full Changelog:** {parsed["_full_changelog"]}\n')

    else:
        lines.append('\n_No release notes provided._\n')

    lines.append('\n---\n')
    return '\n'.join(lines)


def build_markdown(all_releases: list) -> str:
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    header = [
        '# Changelog\n',
        'All releases across **Main**, **Backend** and **Frontend** repositories, newest first.\n',
        f'> Last updated: {now}\n',
        '---\n',
    ]
    return '\n'.join(header) + '\n' + '\n'.join(format_release(e) for e in all_releases)


def main():
    all_releases = []

    for repo in REPOS:
        print(f'Fetching {repo["slug"]} …')
        try:
            releases = fetch_releases(repo['slug'])
        except Exception as exc:
            print(f'  ⚠️  Failed: {exc}')
            continue

        for rel in releases:
            if rel.get('draft'):
                continue
            all_releases.append(
                {
                    'release': rel,
                    'label': repo['label'],
                    'icon': repo['icon'],
                    'slug': repo['slug'],
                    'date': parse_date(rel['published_at']),
                }
            )

    all_releases.sort(key=lambda x: x['date'], reverse=True)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(build_markdown(all_releases))

    print(f'✅  {len(all_releases)} releases written to {OUT}')


if __name__ == '__main__':
    main()
