"""Offline OOXML extraction. Raw DOCX bytes are never rewritten.

Paragraph numbers refer to every w:p in document.xml body order, including
paragraphs in table cells. They are stable locators, NOT Word page numbers.
Images are preserved for human inspection; no OCR or visual inference is claimed.
"""
from pathlib import Path
import hashlib
import json
import posixpath
from urllib.parse import quote
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W, 'm': M, 'a': A, 'r': R}
SUPPORTED = {'.md', '.txt', '.docx'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def originals(root):
    raw = root / 'vault/raw'
    paths = sorted(p for p in raw.rglob('*') if p.is_file() and p.suffix.lower() in SUPPORTED)
    for p in paths:
        if p.is_symlink() or not p.resolve().is_relative_to(raw.resolve()):
            raise ValueError('Sources must be real files inside vault/raw, not links.')
    return paths


def extract_docx(path):
    with ZipFile(path) as z:
        document = ET.fromstring(z.read('word/document.xml'))
        body = document.find('w:body', NS)
        rels = ET.fromstring(z.read('word/_rels/document.xml.rels'))
        targets = {r.attrib['Id']: posixpath.normpath(posixpath.join('word', r.attrib['Target']))
                   for r in rels if r.attrib.get('TargetMode') != 'External'}
        parents = {child: parent for parent in body.iter() for child in parent}
        blocks = []
        for i, p in enumerate(body.findall('.//w:p', NS), 1):
            pieces = []
            for el in p.iter():
                if el.tag in {f'{{{W}}}t', f'{{{M}}}t'}:
                    pieces.append(el.text or '')
                elif el.tag in {f'{{{W}}}tab', f'{{{W}}}br'}:
                    pieces.append('\t' if el.tag.endswith('tab') else '\n')
            images = []
            for blip in p.findall('.//a:blip', NS):
                target = targets.get(blip.get(f'{{{R}}}embed'))
                if target and target.startswith('word/media/'):
                    images.append(target)
            ancestors = []
            current = p
            while current in parents:
                current = parents[current]
                ancestors.append(current.tag)
            blocks.append({'number': i, 'text': ''.join(pieces), 'images': images,
                           'in_table': f'{{{W}}}tc' in ancestors})
        media = {n: z.read(n) for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')}
        return blocks, media


def source_blocks(path):
    if path.suffix.lower() == '.docx':
        return extract_docx(path)[0]
    return [{'number': i, 'text': text, 'images': [], 'in_table': False}
            for i, text in enumerate(path.read_text(encoding='utf-8').splitlines(keepends=True), 1)]


def sections(root, filename, blocks):
    """Human-selected topic ranges are structural metadata, never answer keys."""
    map_path = root / 'sources.json'
    if not map_path.exists():
        return [(1, len(blocks), '')]
    ranges = set()
    for note in json.loads(map_path.read_text()):
        for source in note.get('inputs', []):
            if source['raw'] == filename:
                for lo, hi in source['ranges']:
                    ranges.add((lo, hi, note['title']))
    if not ranges:
        return [(1, len(blocks), '')]
    # Unmapped original paragraphs remain searchable; no silent source omission.
    covered = {i for lo, hi, _ in ranges for i in range(lo, hi + 1)}
    extra = [b['number'] for b in blocks if b['number'] not in covered and b['text'].strip()]
    return sorted(ranges) + [(i, i, '') for i in extra]


def passages(path, root):
    if path.suffix.lower() != '.docx':
        # Keep byte-for-byte line slices for legacy Markdown tests.
        blocks = source_blocks(path)
        ranges = [(1, len(blocks), '')]
        unit = 'lines'
    else:
        blocks = source_blocks(path)
        ranges = sections(root, path.name, blocks)
        unit = 'paragraphs'
    hits = []
    for lo, hi, title in ranges:
        start = lo - 1
        while start < min(hi, len(blocks)):
            end, count = start, 0
            while end < min(hi, len(blocks)) and (count < 160 or end == start):
                count += len(blocks[end]['text'].split())
                end += 1
            selected = blocks[start:end]
            text = ('' if unit == 'lines' else '\n').join(b['text'] for b in selected)
            if text.strip():
                hits.append({'path': path.relative_to(root).as_posix(), 'start': start + 1,
                             'end': end, 'text': text, 'sha256': sha256(path), 'location_unit': unit,
                             'section': title, 'extraction': 'OOXML text; table-cell paragraph order; images excluded' if unit == 'paragraphs' else 'original text'})
            if end >= min(hi, len(blocks)):
                break
            start = max(start + 1, end - 1)
    return hits


def export_reading_copies(root):
    """Human-readable source views with exact text and unchanged embedded images."""
    report = []
    for path in originals(root):
        if path.suffix.lower() != '.docx':
            continue
        blocks, media = extract_docx(path)
        out = root / 'vault/sources' / (path.stem + '.md')
        out.parent.mkdir(parents=True, exist_ok=True)
        target_dir = root / 'vault/attachments' / path.stem
        target_dir.mkdir(parents=True, exist_ok=True)
        for name, data in media.items():
            (target_dir / Path(name).name).write_bytes(data)
        body = f'# {path.stem}\n\nVerbatim OOXML text extraction, not a generated summary. Paragraph numbers include table cells and empty paragraphs. No page numbers are inferred.\n\n[Open unchanged Word original](../raw/{quote(path.name)})\n\nImages below are preserved for visual checking. Their contents are not indexed or supplied to the text model.\n\n'
        for b in blocks:
            if b['text'].strip() or b['images']:
                body += f"### Paragraph {b['number']}" + (' · table cell' if b['in_table'] else '') + '\n\n'
                if b['text'].strip():
                    # Use a plain fenced block so Markdown does not reinterpret original symbols.
                    fence = '~~~~' if '```' in b['text'] else '```text'
                    endf = '~~~~' if fence == '~~~~' else '```'
                    body += fence + '\n' + b['text'] + '\n' + endf + '\n\n'
                for name in b['images']:
                    body += f'![](../attachments/{quote(path.stem)}/{quote(Path(name).name)})\n\n'
        out.write_text(body, encoding='utf-8')
        report.append({'path': path.relative_to(root).as_posix(), 'sha256': sha256(path),
                       'paragraphs': len(blocks), 'table_paragraphs': sum(b['in_table'] for b in blocks),
                       'images_preserved': len(media), 'images_indexed': 0,
                       'word_count': sum(len(b['text'].split()) for b in blocks)})
    return report
