"""Personal wiki harness: local original-source retrieval + local MLX Gemma."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import subprocess
import sys
import time
import uuid
import unicodedata
from urllib.parse import quote
import source_io

ROOT = Path(__file__).resolve().parent
MODEL_ID = 'mlx-community/gemma-4-e2b-it-4bit'
REVISION = '238767527555cb75a05732a84dff5d6ba0dd6809'
STOP = set('a an the is are was were what how which when where who and or to of in on for did does do my me you your it its with from can have has had they them their'.split())
INSUFFICIENT = 'Insufficient evidence in the indexed sources.'
ALIASES = {'自然壟斷': 'natural monopoly', '自然垄断': 'natural monopoly',
           '邊際成本': 'marginal cost', '边际成本': 'marginal cost', '固定成本': 'fixed cost',
           '避險': 'hedging hedge futures', '避险': 'hedging hedge futures', '期貨': 'futures', '期货': 'futures',
           '購買': 'buying', '购买': 'buying', '限制': 'limitation ignores',
           '碳稅': 'carbon tax', '碳税': 'carbon tax', '外部性': 'externalities',
           '電力': 'electricity', '电力': 'electricity', '排放交易': 'cap trade permits',
           '稅負': 'tax incidence', '税负': 'tax incidence', '拍賣': 'auction', '拍卖': 'auction'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def terms(text):
    return [w for w in re.findall(r'[\w]+', unicodedata.normalize('NFKC', text).casefold()) if w not in STOP and len(w) > 1]


def passages(path, root=ROOT):
    return source_io.passages(path, root)


def build_index(root=ROOT):
    paths = source_io.originals(root)
    if not paths:
        raise ValueError('No DOCX, Markdown or text originals in vault/raw.')
    index = {'files': {p.relative_to(root).as_posix(): digest(p) for p in paths},
             'mapping_sha256': digest(root / 'sources.json') if (root / 'sources.json').exists() else None,
             'passages': [c for p in paths for c in passages(p, root)]}
    write_json(root / '.state/index.json', index)
    return index


def search(query, root=ROOT, limit=3):
    query = query + ' ' + ' '.join(english for chinese, english in ALIASES.items() if chinese in query)
    p = root / '.state/index.json'
    if not p.exists():
        raise ValueError('No retrieval index. Run wiki ingest vault/raw (or wiki index for retrieval only).')
    index = read_json(p)
    current = {p.relative_to(root).as_posix(): digest(p) for p in source_io.originals(root)}
    mapping = digest(root / 'sources.json') if (root / 'sources.json').exists() else None
    if current != index['files'] or mapping != index.get('mapping_sha256'):
        raise ValueError('Original sources changed. Re-run wiki ingest or wiki index before searching.')
    chunks = index['passages']
    docs = [Counter(terms(c['text'])) for c in chunks]
    avg = sum(sum(d.values()) for d in docs) / max(len(docs), 1)
    ranked = []
    for c, d in zip(chunks, docs):
        score = 0
        for word in set(terms(query)):
            if word not in d:
                continue
            df = sum(word in other for other in docs)
            idf = math.log(1 + (len(docs) - df + .5) / (df + .5))
            f = d[word]
            score += idf * f * 2.5 / (f + 1.5 * (.25 + .75 * sum(d.values()) / max(avg, 1)))
        if score > 0:
            ranked.append({**c, 'score': round(score, 5)})
    ranked.sort(key=lambda c: (-c['score'], c['path'], c['start']))
    return [{**c, 'label': f'S{i}'} for i, c in enumerate(ranked[:limit], 1)]


def evidence_text(hits):
    return '\n\n'.join(f"[{h['label']}] {h['path']} {h.get('location_unit', 'lines')} {h['start']}-{h['end']}\n{h['text']}" for h in hits)


def source_labels(hits):
    return '\n'.join(f"[{h['label']}] {h['path']} · {h.get('location_unit', 'lines')} {h['start']}-{h['end']}" for h in hits)


class LocalGemma:
    """Imports MLX lazily so search/help do not require a model or MLX."""
    def __init__(self):
        fallback = ROOT.parent / 'local-chatbot/model'
        self.path = Path(os.environ.get('WIKI_MODEL_PATH', str(ROOT / 'model' if (ROOT / 'model').exists() else fallback))).resolve()
        self.model = self.tokenizer = None
        self.load_seconds = 0

    def generate(self, messages, max_tokens=350, temperature=0):
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
        if not (self.path / 'config.json').is_file():
            raise ValueError('Local model missing. Follow README download steps or set WIKI_MODEL_PATH. No cloud fallback.')
        from mlx_lm import load, stream_generate
        from mlx_lm.sample_utils import make_sampler
        import mlx.core as mx
        if self.model is None:
            start = time.perf_counter()
            self.model, self.tokenizer = load(str(self.path))
            self.load_seconds = time.perf_counter() - start
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        count = len(self.tokenizer.encode(prompt))
        if count > 6000:
            raise ValueError(f'Prompt too long ({count} tokens; limit 6000). Shorten the source or conversation.')
        start = time.perf_counter()
        last, output = None, ''
        for response in stream_generate(self.model, self.tokenizer, prompt=prompt,
                                       max_tokens=max_tokens, sampler=make_sampler(temp=temperature)):
            output += response.text
            last = response
        stats = {'load_seconds': self.load_seconds, 'generation_seconds': time.perf_counter() - start,
                 'prompt_tokens': count, 'max_output_tokens': max_tokens, 'temperature': temperature,
                 'generated_tokens': getattr(last, 'generation_tokens', None),
                 'peak_mlx_gb': mx.get_peak_memory() / 1e9,
                 'process_peak_rss_gb': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9,
                 'model': MODEL_ID, 'snapshot_revision': REVISION,
                 'runtime': {p: importlib.metadata.version(p) for p in ['mlx', 'mlx-lm', 'transformers']}}
        return output.strip(), stats


def validate_citations(answer, hits, required=True):
    cited = {label for group in re.findall(r'\[([^\[\]]+)\]', answer)
             for label in re.findall(r'\bS\d+\b', group)}
    allowed = {h['label'] for h in hits}
    issues = []
    if cited - allowed:
        issues.append('Unknown citation labels: ' + ', '.join(sorted(cited - allowed)))
    if required and 'insufficient evidence' not in answer.lower() and not cited:
        issues.append('Answer has no source citation.')
    return {'cited': sorted(cited), 'valid_labels': not issues, 'issues': issues,
            'semantic_support': 'Requires human claim-by-claim review; valid labels do not prove support.'}


def ask(question, model, root=ROOT):
    hits = search(question, root)
    instructions = (root / 'prompts/wiki-instructions.md').read_text()
    messages = [{'role': 'system', 'content': instructions},
                {'role': 'user', 'content': 'ORIGINAL EVIDENCE:\n' + (evidence_text(hits) or '(none)') + '\n\nQUESTION: ' + question}]
    raw, stats = model.generate(messages)
    checks = validate_citations(raw, hits)
    answer = raw if checks['valid_labels'] else INSUFFICIENT + ' The generated answer failed citation validation.'
    return {'interaction_mode': 'ask', 'execution': 'local', 'question': question, 'retrieved': hits,
            'raw_model_answer': raw, 'answer': answer, 'citation_check': checks, 'metrics': stats,
            'chat_history_used': False}


def chat_needs_notes(text):
    # Conservative visible rule; /notes provides an explicit override.
    if text.startswith('/notes '):
        return True
    explicit = bool(re.search(r'\b(notes?|sources?|wiki|reflection)\b|according to', text, re.I))
    if not explicit and re.search(r'\b(imagine|hypothetical|pretend|brainstorm|draft|suggest)\b', text, re.I):
        return False
    return explicit or bool(re.search(r'\beem\b|\blcoe\b|\bmonopoly\b|\bhedg\w*\b|\bcarbon\b|筆記|壟斷|垄断|避險|避险|碳|電力|电力', text, re.I)) or bool(re.search(r'\b(my|our|the)\s+(experiments?|chatbot|project)\b|class\s*(4|four)', text, re.I))


def chat_turn(text, history, model, root=ROOT):
    retrieve = chat_needs_notes(text)
    query = text.removeprefix('/notes ')
    hits = search(query, root) if retrieve else []
    system = (root / 'prompts/persona.md').read_text()
    if retrieve:
        system += '\nORIGINAL EVIDENCE FOR THIS TURN:\n' + (evidence_text(hits) or '(none found)')
    messages = [{'role': 'system', 'content': system}, *history[-8:], {'role': 'user', 'content': query}]
    raw, stats = model.generate(messages, temperature=.3)
    check = validate_citations(raw, hits, required=bool(hits))
    answer = raw if check['valid_labels'] else 'I could not validate the source citations. Please try a narrower question with /notes.'
    history.extend([{'role': 'user', 'content': query}, {'role': 'assistant', 'content': answer}])
    del history[:-8]
    return {'interaction_mode': 'chat', 'execution': 'local', 'question': query, 'retrieval_used': retrieve,
            'retrieved': hits, 'answer': answer, 'raw_model_answer': raw, 'citation_check': check,
            'metrics': stats, 'history_messages_used': len(messages) - 2}


def save_record(record, root=ROOT, name=None):
    record = {'recorded_at': datetime.now(timezone.utc).isoformat(),
              'offline_proof': 'Local-only inference; physical internet disconnection not verified.', **record}
    name = name or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6]
    folder = root / 'evidence/runs'
    write_json(folder / (name + '.json'), record)
    md = f"# {record['interaction_mode'].title()} evidence\n\nExecution: local. {record['offline_proof']}\n\n"
    if 'question' in record:
        md += '## Input\n\n' + record['question'] + '\n\n'
    if 'answer' in record:
        md += '## Displayed answer\n\n' + record['answer'] + '\n\n'
    md += '## Original retrieved passages\n\n' + (evidence_text(record.get('retrieved', [])) or 'None.')
    md += '\n\n## Complete settings, checks and metrics\n\nSee [' + name + '.json](' + name + '.json).\n'
    (folder / (name + '.md')).write_text(md, encoding='utf-8')
    return folder / (name + '.md')


def inputs_for(row):
    return row.get('inputs', [{'raw': row.get('raw'), 'ranges': None}])


def catalog(root=ROOT):
    rows = read_json(root / 'sources.json')
    titles, mapped = set(), set()
    for row in rows:
        for field in ['title', 'topic']:
            if '/' in row[field] or '\\' in row[field] or row[field] in {'.', '..'}:
                raise ValueError('Invalid title or topic path.')
        if not 2 <= len(row['title'].split()) <= 6 or row['title'] in titles:
            raise ValueError('Note titles must be unique, descriptive names of 2–6 words.')
        titles.add(row['title'])
        for item in inputs_for(row):
            raw = item['raw']
            if not raw or Path(raw).name != raw:
                raise ValueError('Source mappings require a simple filename.')
            source = root / 'vault/raw' / raw
            if not source.is_file():
                raise ValueError('Missing original: ' + raw)
            mapped.add(raw)
            blocks = source_io.source_blocks(source)
            for lo, hi in item.get('ranges') or [(1, len(blocks))]:
                if not 1 <= lo <= hi <= len(blocks):
                    raise ValueError('Invalid original paragraph range: ' + raw)
    for row in rows:
        if set(row['related']) - titles:
            raise ValueError('Related-note target missing from sources.json.')
    if {p.name for p in source_io.originals(root)} != mapped:
        raise ValueError('Map every original in sources.json before ingestion.')
    return rows


def note_path(row, root=ROOT):
    return root / 'vault/wiki' / row['topic'] / (row['title'] + '.md')


def fingerprint(row, root):
    value = {'mapping': row, 'originals': {i['raw']: digest(root / 'vault/raw' / i['raw']) for i in inputs_for(row)},
             'prompt': (root / 'prompts/ingest.md').read_text()}
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def input_text(row, root):
    parts = []
    for item in inputs_for(row):
        blocks = source_io.source_blocks(root / 'vault/raw' / item['raw'])
        for lo, hi in item.get('ranges') or [(1, len(blocks))]:
            parts.append(item['raw'] + f' paragraphs {lo}-{hi}:\n' + '\n'.join(b['text'] for b in blocks[lo-1:hi]))
    return '\n\n'.join(parts)


def navigation(rows, root=ROOT):
    body = '# EEM Study Wiki\n\nCourse revision covering markets, regulation, energy and environmental policy, grounded in four EEM study notes.\n\n[[Source Catalog]] — Original documents, extracted text and figures.\n\n[[Reading Guide]] — How to use this wiki, source differences and figure limitations.\n'
    for topic in sorted({r['topic'] for r in rows}):
        body += '\n## ' + topic + '\n\n'
        for r in rows:
            if r['topic'] == topic:
                body += f"- [[{r['title']}]] — {r['description']}\n"
    (root / 'vault/index.md').write_text(body)
    state = read_json(root / '.state/ingestion.json')
    body = '# Source Catalog\n\nWord originals are unchanged. Reading copies preserve extracted text and embedded images. Images are available for human viewing but excluded from model retrieval. Paragraph locators refer to OOXML document order, not page numbers.\n\n'
    for source in source_io.originals(root):
        body += f'## {source.stem}\n\n[Original](raw/{quote(source.name)})'
        if source.suffix == '.docx':
            body += f' · [[sources/{source.stem}|Reading copy and figures]]'
        body += f'\n\nSHA-256: `{digest(source)}`\n\n'
        for r in rows:
            if source.name in {i['raw'] for i in inputs_for(r)}:
                status = state.get(r['title'], {}).get('review', 'pending')
                body += f"- [[{r['title']}]] — {status}\n"
        body += '\n'
    (root / 'vault/Source Catalog.md').write_text(body)


def ingest(model, root=ROOT, force=False):
    start = time.perf_counter()
    rows = catalog(root)
    extraction = source_io.export_reading_copies(root)
    state_path = root / '.state/ingestion.json'
    state = read_json(state_path) if state_path.exists() else {}
    results = []
    for row in rows:
        signature = fingerprint(row, root)
        target = note_path(row, root)
        old = state.get(row['title'], {})
        if not old and target.exists():
            # A fresh clone excludes .state, but reviewed Markdown carries its
            # input fingerprint. Preserve those edits when inputs still match.
            existing = target.read_text(encoding='utf-8')
            saved = re.search(r'^fingerprint: ([0-9a-f]{64})$', existing, re.M)
            status = re.search(r'^review: (pending|reviewed)$', existing, re.M)
            if saved:
                old = {'fingerprint': saved.group(1), 'review': status.group(1) if status else 'pending',
                       'page': target.relative_to(root).as_posix(),
                       'source_files': [i['raw'] for i in inputs_for(row)]}
                state[row['title']] = old
        if old.get('fingerprint') == signature and target.exists() and not force:
            results.append({'title': row['title'], 'status': 'unchanged; preserved existing page'})
            continue
        text = input_text(row, root)
        if len(text.split()) > 2500:
            raise ValueError(row['title'] + ' exceeds the 2500-word ingestion limit; narrow its source ranges.')
        messages = [{'role': 'system', 'content': (root / 'prompts/ingest.md').read_text()},
                    {'role': 'user', 'content': 'Summarize ONLY the subject ' + row['title'] + ':\n\n' + text}]
        raw_summary, metrics = model.generate(messages, max_tokens=480)
        summary = re.sub(r'\[\[([^\]]+)\]\]', r'\1', raw_summary)
        summary = re.sub(r'^#.*\n?', '', summary, flags=re.M).strip()
        if target.exists():
            backup = root / 'evidence/previous-pages' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6] + '-' + target.name)
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True, exist_ok=True)
        names = [i['raw'] for i in inputs_for(row)]
        body = f'---\nsource_files: {json.dumps(names)}\nfingerprint: {signature}\nreview: pending\n---\n\n# {row["title"]}\n\n{summary}\n\n## Sources\n\n'
        for item in inputs_for(row):
            raw = item['raw']
            body += f'- [Original {raw}](../../raw/{quote(raw)})'
            if raw.endswith('.docx'):
                body += f' · [[sources/{Path(raw).stem}|Text and figures]]'
            ranges = ', '.join(f'{lo}–{hi}' for lo, hi in item.get('ranges') or []) or 'all'
            body += ' · paragraphs ' + ranges + '\n'
        body += '\n## Related notes\n\n' + ''.join(f'- [[{t}]] — {reason}\n' for t, reason in row['related'].items())
        target.write_text(body, encoding='utf-8')
        state[row['title']] = {'fingerprint': signature, 'page': target.relative_to(root).as_posix(), 'review': 'pending', 'source_files': names}
        write_json(state_path, state)
        results.append({'title': row['title'], 'status': 'generated; review pending', 'metrics': metrics, 'raw_model_summary': raw_summary})
    write_json(state_path, state)
    index = build_index(root)
    navigation(rows, root)
    write_json(root / 'evidence/extraction-report.json', extraction)
    return {'interaction_mode': 'ingest', 'execution': 'local', 'sources': results,
            'source_hashes': index['files'], 'extraction_report': extraction, 'passages': len(index['passages']),
            'elapsed_seconds': time.perf_counter() - start}


def review(title, root=ROOT):
    rows = catalog(root)
    row = next((r for r in rows if r['title'] == title), None)
    if not row:
        raise ValueError('Unknown note title.')
    state = read_json(root / '.state/ingestion.json')
    if state[title]['fingerprint'] != fingerprint(row, root):
        raise ValueError('Source or mapping changed. Re-ingest before reviewing.')
    page = note_path(row, root)
    page.write_text(page.read_text().replace('review: pending', 'review: reviewed', 1))
    state[title]['review'] = 'reviewed'
    write_json(root / '.state/ingestion.json', state)
    navigation(rows, root)
    return {'interaction_mode': 'review', 'execution': 'local', 'answer': 'Marked reviewed: ' + title}


def doctor(root=ROOT):
    def run(args):
        r = subprocess.run(args, text=True, capture_output=True)
        return r.stdout.strip() or r.stderr.strip()
    vm = run(['vm_stat']) if sys.platform == 'darwin' else 'Not measured.'
    info = {'interaction_mode': 'doctor', 'execution': 'local', 'python': platform.python_version(),
            'os': platform.platform(), 'model': MODEL_ID, 'snapshot_revision': REVISION,
            'model_present': (LocalGemma().path / 'model.safetensors').exists(),
            'vm_stat': vm, 'disk': run(['df', '-h', str(root)]),
            'offline_proof': 'This command does not verify physical internet disconnection.'}
    if sys.platform == 'darwin':
        hardware = run(['system_profiler', 'SPHardwareDataType', 'SPDisplaysDataType'])
        info['hardware'] = '\n'.join(l for l in hardware.splitlines() if not any(s in l for s in ['Serial Number', 'UUID', 'UDID']))
    return info


def main(argv=None):
    parser = argparse.ArgumentParser(description='Fern personal wiki: local Gemma + original-source retrieval. No cloud fallback.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('ingest', help='Summarize mapped raw sources with Gemma; rebuild retrieval and navigation.')
    p.add_argument('source', nargs='?', default='vault/raw')
    p.add_argument('--regenerate', action='store_true', help='Run Gemma again; back up existing pages outside vault and reset review status.')
    sub.add_parser('index', help='Rebuild original-source retrieval only; no model required.')
    for name in ['ask', 'search']:
        p = sub.add_parser(name, help='Standalone cited factual answer.' if name == 'ask' else 'Original matching passages; no model call.')
        p.add_argument('question')
        p.add_argument('--mode', choices=['local'], default='local')
    sub.add_parser('chat', help='Conversational assistant. /notes QUERY forces retrieval; /reset clears history; /exit quits.')
    p = sub.add_parser('review', help='Mark a wiki page reviewed after comparing it with its original.')
    p.add_argument('title')
    sub.add_parser('doctor', help='Record local device/model availability.')
    sub.add_parser('help', help='Show command help.')
    args = parser.parse_args(argv)
    model = LocalGemma()
    try:
        if args.command == 'help':
            parser.print_help()
            return 0
        if args.command == 'chat':
            history = []
            print(f'Fern | chat | local | {MODEL_ID}\n/notes QUERY · /reset · /exit')
            while True:
                try:
                    text = input('\nYou: ').strip()
                except (EOFError, KeyboardInterrupt):
                    print('\nGoodbye.'); break
                if text == '/exit': break
                if text == '/reset': history.clear(); print('Conversation cleared.'); continue
                if not text: continue
                result = chat_turn(text, history, model)
                print('\nFern: ' + result['answer'])
                if result['retrieved']:
                    print(source_labels(result['retrieved']))
                print('Saved:', save_record(result).relative_to(ROOT))
            return 0
        if args.command == 'ingest':
            source = Path(args.source)
            if not source.is_absolute(): source = ROOT / source
            if source.resolve() != (ROOT / 'vault/raw').resolve():
                raise ValueError('Copy unchanged sources into this project’s vault/raw and map them in sources.json.')
            result = ingest(model, force=args.regenerate)
        elif args.command == 'index':
            idx = build_index()
            result = {'interaction_mode': 'index', 'execution': 'local', 'passages': len(idx['passages'])}
        elif args.command == 'ask': result = ask(args.question, model)
        elif args.command == 'search':
            result = {'interaction_mode': 'search', 'execution': 'local', 'question': args.question,
                      'retrieved': search(args.question), 'model_called': False}
        elif args.command == 'review': result = review(args.title)
        else: result = doctor()
        print(f'{args.command} | local | ' + (MODEL_ID if args.command in ['ask', 'ingest'] else 'no model call'))
        print(result.get('answer') or (evidence_text(result['retrieved']) if 'retrieved' in result else json.dumps(result, indent=2)))
        if args.command == 'ask' and result['retrieved']:
            print('\nSources:\n' + source_labels(result['retrieved']))
        print('Saved:', save_record(result).relative_to(ROOT))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        failure = {'interaction_mode': args.command, 'execution': 'local', 'error': str(exc) or 'Interrupted'}
        path = save_record(failure)
        print(f"Error: {failure['error']}\nSaved: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
