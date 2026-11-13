"""Export Pelican's published articles for Sequoia without editing source files."""

from html.parser import HTMLParser
from datetime import datetime
import json
import os
from pathlib import Path
import re

from pelican import signals
from pelican.generators import ArticlesGenerator


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.hidden += 1
        elif tag == 'img' and not self.hidden:
            self.parts.append(dict(attrs).get('alt', ''))
        elif tag in {'br', 'p', 'div', 'li', 'pre', 'h1', 'h2', 'h3', 'h4', 'tr'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.hidden = max(0, self.hidden - 1)
        elif tag in {'p', 'div', 'li', 'pre', 'h1', 'h2', 'h3', 'h4', 'tr'}:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_text(value):
    parser = PlainText()
    parser.feed(str(value))
    return '\n'.join(line.rstrip() for line in ''.join(parser.parts).splitlines()).strip()


def export_articles(generators):
    for generator in generators:
        if not isinstance(generator, ArticlesGenerator):
            continue
        export_dir = Path(generator.settings['STANDARD_SITE_EXPORT_PATH'])
        cover_image = generator.settings['OPENGRAPH_IMAGE']
        cover_path = Path(generator.settings['PATH']) / cover_image
        if not cover_path.is_file():
            raise ValueError(f'Standard.site cover image does not exist: {cover_path}')
        cover_relative = os.path.relpath(cover_path, export_dir.parent.parent)
        export_dir.mkdir(parents=True, exist_ok=True)
        # This directory contains only generated Sequoia input, never source posts.
        for previous in export_dir.glob('*.md'):
            previous.unlink()
        paths = set()
        manifest = []
        for article in generator.articles:
            if article.status != 'published' or article.date > datetime.now(article.date.tzinfo):
                continue
            path = '/' + article.url.lstrip('/')
            if path in paths:
                raise ValueError(f'Duplicate Standard.site article URL: {path}')
            paths.add(path)
            metadata = {
                'title': plain_text(article.title),
                'description': ' '.join(plain_text(article.summary).split()),
                'publishDate': article.date.isoformat(),
                'path': path,
                'textContent': plain_text(article.content),
                'ogImage': cover_image,
            }
            # Pelican otherwise falls back to the checkout's filesystem mtime.
            source_header = Path(article.source_path).read_text(encoding='utf-8').split('\n\n', 1)[0]
            if re.search(r'^modified\s*:', source_header, re.IGNORECASE | re.MULTILINE):
                metadata['updatedAt'] = article.modified.isoformat()
            if getattr(article, 'tags', None):
                metadata['tags'] = [plain_text(tag) for tag in article.tags]
            # JSON is valid YAML and safely quotes multiline text, colons, and dates.
            frontmatter = json.dumps(metadata, ensure_ascii=False, indent=2)
            filename = Path(article.source_path).stem + '.md'
            (export_dir / filename).write_text(f'---\n{frontmatter}\n---\n', encoding='utf-8')
            manifest.append({'file': str((export_dir / filename).relative_to(export_dir.parent.parent)), 'path': path,
                             'saveAs': article.save_as, 'title': metadata['title'],
                             'coverImage': cover_relative})
        (export_dir.parent / 'manifest.json').write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def register():
    signals.all_generators_finalized.connect(export_articles)
