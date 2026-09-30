import shutil
import tempfile
import unittest
from pathlib import Path
import wiki


class RecordingModel:
    def __init__(self, reply='Supported fact. [S1]'):
        self.calls = []
        self.reply = reply

    def generate(self, messages, **kwargs):
        self.calls.append(messages)
        return self.reply, {'test_double': True}


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(wiki.ROOT / 'prompts', self.root / 'prompts')
        (self.root / 'vault/raw').mkdir(parents=True)
        (self.root / 'vault/raw/Note.md').write_text('# Workshop\n\nThe workshop starts at 10 a.m. in Room 204.\n')
        wiki.build_index(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_search_exact_original_and_location(self):
        hit = wiki.search('workshop location', self.root)[0]
        original = (self.root / hit['path']).read_text().splitlines(keepends=True)
        self.assertEqual(hit['text'], ''.join(original[hit['start']-1:hit['end']]))

    def test_sources_changed_refuses_stale_index(self):
        (self.root / 'vault/raw/Note.md').write_text('Workshop cancelled.')
        with self.assertRaisesRegex(ValueError, 'changed'):
            wiki.search('workshop', self.root)

    def test_ask_has_no_persona_or_chat_history(self):
        model = RecordingModel()
        wiki.ask('Where is the workshop?', model, self.root)
        self.assertEqual(len(model.calls[0]), 2)
        self.assertNotIn('Fern', model.calls[0][0]['content'])

    def test_casual_chat_skips_lookup_without_index(self):
        (self.root / '.state/index.json').unlink()
        model = RecordingModel('I can help draft a study plan.')
        history = []
        result = wiki.chat_turn('what can we do?', history, model, self.root)
        self.assertFalse(result['retrieval_used'])
        wiki.chat_turn('make that shorter', history, model, self.root)
        self.assertEqual(model.calls[1][2]['content'], 'I can help draft a study plan.')

    def test_unknown_citations_and_uncited_claims_fail_closed(self):
        for text in ['Room 204. [S99]', 'Room 204. [S1, S99]', 'Room 204.']:
            result = wiki.ask('Where is the workshop?', RecordingModel(text), self.root)
            self.assertFalse(result['citation_check']['valid_labels'])
            self.assertEqual(result['raw_model_answer'], text)
            self.assertIn('Insufficient evidence', result['answer'])

    def test_unsupported_question_still_calls_local_model(self):
        model = RecordingModel(wiki.INSUFFICIENT)
        result = wiki.ask('zebra catering', model, self.root)
        self.assertEqual(result['retrieved'], [])
        self.assertEqual(len(model.calls), 1)

    def test_generated_answers_never_enter_index(self):
        (self.root / 'vault/wiki').mkdir()
        (self.root / 'vault/wiki/Draft.md').write_text('Zebras cater everything.')
        wiki.build_index(self.root)
        self.assertEqual(wiki.search('zebras', self.root), [])

    def test_hypothetical_budget_is_conversation_not_evidence(self):
        self.assertFalse(wiki.chat_needs_notes('For this conversation only, imagine that my project budget is 999 dollars.'))
        self.assertTrue(wiki.chat_needs_notes('/notes What is my project budget?'))

    def test_reingestion_preserves_reviewed_page_and_original(self):
        wiki.write_json(self.root / 'sources.json', [{'raw':'Note.md', 'title':'Workshop Details',
                        'topic':'Projects', 'origin':'test fixture', 'description':'Workshop details.', 'related':{}}])
        model = RecordingModel('The workshop starts at 10 a.m. in Room 204.')
        original = (self.root / 'vault/raw/Note.md').read_bytes()
        wiki.ingest(model, self.root)
        wiki.review('Workshop Details', self.root)
        page = self.root / 'vault/wiki/Projects/Workshop Details.md'
        reviewed = page.read_bytes()
        wiki.ingest(model, self.root)
        self.assertEqual(len(model.calls), 1)
        self.assertEqual(page.read_bytes(), reviewed)
        (self.root / '.state/ingestion.json').unlink()
        wiki.ingest(model, self.root)
        self.assertEqual(len(model.calls), 1)
        self.assertEqual(page.read_bytes(), reviewed)
        self.assertEqual((self.root / 'vault/raw/Note.md').read_bytes(), original)
        self.assertEqual(len(list((self.root / 'vault/wiki').rglob('*.md'))), 1)
        wiki.ingest(model, self.root, force=True)
        self.assertEqual(len(model.calls), 2)
        self.assertEqual(len(list((self.root / 'evidence/previous-pages').glob('*.md'))), 1)

class DocxTests(unittest.TestCase):
    def test_docx_table_cells_and_original_provenance(self):
        from zipfile import ZipFile
        import source_io
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'vault/raw').mkdir(parents=True)
            path = root / 'vault/raw/Source.docx'
            xml = '''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Natural Monopoly</w:t></w:r></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>Fixed cost</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Cannot be recovered at P=MC.</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>'''
            with ZipFile(path, 'w') as z:
                z.writestr('word/document.xml', xml)
                z.writestr('word/_rels/document.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')
            before = path.read_bytes()
            wiki.build_index(root)
            hit = wiki.search('自然壟斷 固定成本', root)[0]
            self.assertEqual(hit['location_unit'], 'paragraphs')
            self.assertIn('Cannot be recovered', hit['text'])
            self.assertEqual(hit['path'], 'vault/raw/Source.docx')
            report = source_io.export_reading_copies(root)
            self.assertEqual(report[0]['table_paragraphs'], 2)
            self.assertEqual(path.read_bytes(), before)

    def test_mapping_change_requires_reindex(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'vault/raw').mkdir(parents=True)
            (root / 'vault/raw/Text.md').write_text('original')
            wiki.write_json(root / 'sources.json', [])
            wiki.build_index(root)
            wiki.write_json(root / 'sources.json', [{'title': 'New topic'}])
            with self.assertRaisesRegex(ValueError, 'changed'):
                wiki.search('original', root)


if __name__ == '__main__':
    unittest.main()
