"""Run fixed questions and mode checks, preserving every actual result."""
from datetime import datetime, timezone
import json
import sys
from pathlib import Path
from wiki import ROOT, LocalGemma, ask, chat_turn, search, save_record, read_json, write_json, ingest


def main():
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    model = LocalGemma()
    records = []
    for case in read_json(ROOT / 'evals/questions.json'):
        print('\nASK:', case['question'], flush=True)
        record = ask(case['question'], model)
        record['expectation'] = case
        record['retrieval_expected_source_found'] = case['expected_source'] is None or any(h['path'] == case['expected_source'] for h in record['retrieved'])
        record['expected_excerpt_retrieved'] = case['expected_source'] is None or any(case['expected_excerpt'] in h['text'] for h in record['retrieved'] if h['path'] == case['expected_source'])
        record['expected_terms_present'] = all(t.lower() in record['answer'].lower() for t in case['expected_terms'])
        record['assessment'] = 'Automated source/term checks only; read the answer and cited original before accepting.'
        path = save_record(record, name=run_id + '-' + case['id'])
        records.append(str(path.relative_to(ROOT)))
        print(record['answer'], flush=True)
    history = []
    prompts = ['what can we do?', 'what can you help me with?',
               'Suggest a short three-step plan for revising a difficult topic.', 'make that shorter',
               'For this conversation only, imagine that my project budget is 999 dollars.']
    for i, prompt in enumerate(prompts, 1):
        print('\nCHAT:', prompt, flush=True)
        record = chat_turn(prompt, history, model)
        records.append(str(save_record(record, name=f'{run_id}-chat-{i}').relative_to(ROOT)))
        print(record['answer'], flush=True)
    record = ask('What is my project budget in dollars?', model)
    record['assessment'] = 'Must not treat the imaginary 999 dollars in chat as source evidence.'
    records.append(str(save_record(record, name=run_id + '-ask-isolation').relative_to(ROOT)))
    print('\nASK ISOLATION:', record['answer'], flush=True)
    record = ask('根據筆記，LCOE 有哪些限制？', model)
    records.append(str(save_record(record, name=run_id + '-ask-chinese').relative_to(ROOT)))
    print('\nCHINESE ASK:', record['answer'], flush=True)
    record = chat_turn('/notes What are the limitations of LCOE in my notes?', history, model)
    records.append(str(save_record(record, name=run_id + '-chat-notes').relative_to(ROOT)))
    print('\nCHAT WITH NOTES:', record['answer'], flush=True)
    hits = search('natural monopoly marginal cost fixed cost')
    record = {'interaction_mode': 'search', 'execution': 'local', 'question': 'natural monopoly marginal cost fixed cost',
              'retrieved': hits, 'model_called': False}
    records.append(str(save_record(record, name=run_id + '-search').relative_to(ROOT)))
    before = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'vault/wiki').rglob('*.md'))
    result = ingest(model)
    after = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'vault/wiki').rglob('*.md'))
    result['same_page_paths'] = before == after
    records.append(str(save_record(result, name=run_id + '-reingestion').relative_to(ROOT)))
    write_json(ROOT / 'evidence/latest-evaluation.json', {'run_id': run_id, 'records': records,
               'physical_offline_demonstration': 'pending', 'human_review': 'pending'})
    print('\nSaved', len(records), 'records. Physical offline demonstration remains pending.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        save_record({'interaction_mode': 'evaluation', 'execution': 'local', 'error': str(exc)})
        raise
