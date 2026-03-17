import json
import os
import urllib.request
from datetime import datetime

REPOS = [
    {'slug': 'moviesxmovies/MoviesXMovies', 'label': 'Main', 'icon': '🎬'},
    {'slug': 'moviesxmovies/MoviesXMoviesBackend', 'label': 'Backend', 'icon': '⚙️'},
    {'slug': 'moviesxmovies/MoviesXMoviesFrontend', 'label': 'Frontend', 'icon': '🖥️'},
]

CATEGORIES = [
    {'title': '🚀 Features', 'prefixes': ['feat', 'feature']},
    {'title': '🐛 Fixes', 'prefixes': ['fix', 'bug']},
    {'title': '🧪 Tests', 'prefixes': ['test', 'tests']},
    {'title': '🧰 Maintenance', 'prefixes': ['chore', 'ci', 'build']},
]
IGNORE_PREFIXES = ['ignore']

OUT = 'docs/changelog.md'

ADMONTIONS_TYPES = {
    '🚀 Features': ('tip', '🚀 Features'),
    '🐛 Fixes': ('bug', '🐛 Fixes'),
    '🧪 Tests': ('example', '🧪 Tests'),
    '🧰 Maintenance': ('note', '🧰 Maintenance'),
}


def gh_get(url: str):
    req = urllib.request.Request(
        url,
        headers={
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
    if not body:
        return {}

    result = {}
    current = None
    new_contributors = []
    full_changelog = None

    for raw_line in body.replace('\r\n', '\n').split('\n'):
        line = raw_line.strip()

        if line.startswith('## ') or line.startswith('### '):  # ← fix: also match ###
            section = line.lstrip('#').strip()
            # Skip the generic "What's Changed" wrapper
            if section == "What's Changed":
                continue
            current = section
            if current not in result:
                result[current] = []

        elif line.lower().startswith('**full changelog**'):
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
    text = entry_line.lstrip('* ').lower()
    return any(text.startswith(p) for p in IGNORE_PREFIXES)


def format_release(rel_entry: dict) -> str:
    rel = rel_entry['release']
    date = parse_date(rel['published_at']).strftime('%B %d, %Y')
    tag = rel['tag_name']
    name = rel.get('name') or tag
    url = rel['html_url']
    pre = ' _(pre-release)_' if rel.get('prerelease') else ''

    lines = []

    # Release title as admonition instead of ### header — no ToC entry generated
    lines.append(f'??? info "{name}{pre} &nbsp;·&nbsp; `{tag}` &nbsp;·&nbsp; {date}"')
    lines.append(f'    [View on GitHub]({url})\n')

    parsed = parse_release_body(rel.get('body', ''))

    if parsed:
        rendered_any = False

        for cat in CATEGORIES:
            section_lines = parsed.get(cat['title'], [])
            visible = [l for l in section_lines if not should_ignore(l)]
            if visible:
                admonition_types = {
                    '🚀 Features':    ('tip',     '🚀 Features'),
                    '🐛 Fixes':       ('bug',     '🐛 Fixes'),
                    '🧪 Tests':       ('example', '🧪 Tests'),
                    '🧰 Maintenance': ('note',    '🧰 Maintenance'),
                }
                adm_type, adm_title = admonition_types.get(cat['title'], ('note', cat['title']))
                lines.append(f'    !!! {adm_type} "{adm_title}"')
                for item in visible:
                    lines.append(f'        {item}')
                lines.append('')
                rendered_any = True

        known_titles = {c['title'] for c in CATEGORIES} | {'New Contributors', "What's Changed"}
        for section_title, section_lines in parsed.items():
            if section_title.startswith('_'):
                continue
            if section_title not in known_titles:
                visible = [l for l in section_lines if not should_ignore(l)]
                if visible:
                    lines.append(f'    !!! note "{section_title}"')
                    for item in visible:
                        lines.append(f'        {item}')
                    lines.append('')
                    rendered_any = True

        if not rendered_any:
            lines.append('    !!! abstract "No Changes"\n        _No categorized changes found._\n')

        if parsed.get('_new_contributors'):
            lines.append('    !!! success "👋 New Contributors"')
            for c in parsed['_new_contributors']:
                lines.append(f'        {c}')
            lines.append('')

        if parsed.get('_full_changelog'):
            lines.append(f'    !!! quote "↔️ Full Changelog"\n        {parsed["_full_changelog"]}\n')

    else:
        lines.append('    !!! abstract "No Changes"\n        _No release notes provided._\n')

    lines.append('')
    return '\n'.join(lines)



def build_repo_tab(repo: dict, releases: list) -> str:
    """Renders all releases for one repo as a MkDocs tab block."""
    lines = []
    lines.append(f'=== "{repo["icon"]} {repo["label"]}"')

    if not releases:
        lines.append('\n    _No releases yet._\n')
        return '\n'.join(lines)

    for entry in releases:
        block = format_release(entry)
        # Indent every line 4 spaces — required by MkDocs content.tabs
        for line in block.split('\n'):
            lines.append(f'    {line}' if line.strip() else '')

    return '\n'.join(lines)


def build_markdown(releases_by_repo: dict) -> str:
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    lines = [
        '---',
        'title: Changelog',
        'icon: lucide/history',
        'hide:',
        '  - toc',
        '  - navigation',
        '---',
        '',
        '# Changelog\n',
        'All releases across **Main**, **Backend** and **Frontend** repositories.\n',
        f'> Last updated: {now}\n',
        '',
    ]

    for repo in REPOS:
        slug = repo['slug']
        releases = releases_by_repo.get(slug, [])
        lines.append(build_repo_tab(repo, releases))
        lines.append('')

    return '\n'.join(lines)


def main():
    releases_by_repo: dict[str, list] = {}

    for repo in REPOS:
        print(f'Fetching {repo["slug"]} …')
        try:
            releases = fetch_releases(repo['slug'])
        except Exception as exc:
            print(f'  ⚠️  Failed: {exc}')
            releases_by_repo[repo['slug']] = []
            continue

        entries = []
        for rel in releases:
            if rel.get('draft'):
                continue
            entries.append(
                {
                    'release': rel,
                    'label': repo['label'],
                    'icon': repo['icon'],
                    'slug': repo['slug'],
                    'date': parse_date(rel['published_at']),
                }
            )

        # Newest first dentro de cada repo
        entries.sort(key=lambda x: x['date'], reverse=True)
        releases_by_repo[repo['slug']] = entries

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(build_markdown(releases_by_repo))

    total = sum(len(v) for v in releases_by_repo.values())
    print(f'✅  {total} releases written to {OUT}')


if __name__ == '__main__':
    main()
