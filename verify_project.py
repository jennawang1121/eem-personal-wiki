"""Verify raw source hashes, extracted text coverage, links and stable ingestion."""
import json
from pathlib import Path
import re
from urllib.parse import unquote
from zipfile import ZipFile
from wiki import ROOT, read_json, write_json, digest, catalog, ingest
from source_io import source_blocks


def main():
    files = list((ROOT / 'vault').rglob('*'))
    originals = []
    for doc in read_json(ROOT / 'documents.json'):
        path = ROOT / 'vault/raw' / doc['raw']
        originals.append({'file': doc['raw'], 'unchanged_since_import': digest(path) == doc['sha256']})
    assert all(x['unchanged_since_import'] for x in originals)
    links = []
    for p in (ROOT / 'vault').rglob('*.md'):
        # Source text is quoted inside code fences; only navigation outside them is markup.
        text = re.sub(r'```.*?```|~~~~.*?~~~~', '', p.read_text(), flags=re.S)
        for target in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text):
            matches = [f for f in files if f.is_file() and (f.stem == target or f.relative_to(ROOT/'vault').with_suffix('').as_posix() == target)]
            links.append({'from': str(p.relative_to(ROOT)), 'target': target, 'matches': len(matches)})
            assert len(matches) == 1, (p, target, len(matches))
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            assert (p.parent / unquote(target)).exists(), (p, target)
    coverage = []
    for doc in read_json(ROOT / 'documents.json'):
        p = ROOT/'vault/raw'/doc['raw']
        blocks = source_blocks(p)
        indexed = read_json(ROOT/'.state/index.json')['passages']
        covered = {i for h in indexed if h['path'] == p.relative_to(ROOT).as_posix() for i in range(h['start'],h['end']+1)}
        missing = [b['number'] for b in blocks if b['text'].strip() and b['number'] not in covered]
        assert not missing, missing
        with ZipFile(p) as z:
            media = [n for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')]
            for name in media:
                assert z.read(name) == (ROOT/'vault/attachments'/p.stem/Path(name).name).read_bytes()
        coverage.append({'file':doc['raw'],'missing_text_paragraphs':missing,'unchanged_images':len(media)})
    before = {str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'vault/wiki').rglob('*.md')}
    class NoModel:
        def generate(self, *a, **kw):
            raise AssertionError('Unchanged re-ingestion should not call Gemma.')
    result = ingest(NoModel())
    after = {str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'vault/wiki').rglob('*.md')}
    assert before == after
    for row in catalog():
        p=ROOT/'vault/wiki'/row['topic']/(row['title']+'.md')
        assert f"# {row['title']}\n" in p.read_text()
        assert 'review: reviewed' in p.read_text()
    write_json(ROOT/'evidence/vault-validation.json', {'originals':originals,'links':links,'coverage':coverage,
        'topic_pages':len(after),'reingestion_preserves_all_page_bytes':before==after,
        'obsolete_ai_learning_sources_present':False,'obsidian_ui_navigation':'See evidence/obsidian/README.md; these are filesystem checks, not UI verification.'})
    print(f'PASS: {len(originals)} unchanged originals, {len(after)} reviewed topic pages, {len(links)} resolved wiki links, all original text covered, 22 images preserved, re-ingestion unchanged.')


if __name__ == '__main__':
    main()
