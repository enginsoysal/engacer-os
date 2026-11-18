"""A single complete fresh crawl may be reused only after the matching Save."""
import copy
from datetime import datetime, timezone
import unittest
from website_readback import validate_fresh_audit


class FreshAudit(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 18, 12, 10, tzinfo=timezone.utc)
        self.report = dict(source_commit='a'*40, started_at='2026-11-18T12:01:00Z',
                           checked_at='2026-11-18T12:08:00Z', pages_checked=1,
                           pages=[dict(url='https://engaceros.brixcanvas.com/')])
        self.payload = dict(source_commit='a'*40)
        self.saved = dict(source_commit='a'*40, home='Saved ✓', recovery='Saved ✓',
                          checked_at='2026-11-18T12:00:00Z')

    def test_same_source_fresh_post_save_crawl_passes(self):
        validate_fresh_audit(self.report, self.payload, self.saved, self.now)

    def test_wrong_source_pre_save_future_or_expired_crawl_is_refused(self):
        for field, value in [('source_commit', 'b'*40),
                             ('started_at', '2026-11-18T11:59:00Z'),
                             ('checked_at', '2026-11-18T12:11:00Z')]:
            report = copy.deepcopy(self.report)
            report[field] = value
            with self.assertRaises(AssertionError):
                validate_fresh_audit(report, self.payload, self.saved, self.now)
        with self.assertRaises(AssertionError):
            validate_fresh_audit(self.report, self.payload, self.saved,
                                 datetime(2026, 11, 18, 13, tzinfo=timezone.utc))

    def test_missing_save_or_duplicate_incomplete_inventory_is_refused(self):
        for field, value in [('home', 'Saving…'), ('recovery', 'Save'),
                             ('source_commit', 'b'*40)]:
            saved = dict(self.saved, **{field: value})
            with self.assertRaises(AssertionError):
                validate_fresh_audit(self.report, self.payload, saved, self.now)
        for count, rows in [(2, self.report['pages']),
                            (2, self.report['pages']*2)]:
            report = dict(self.report, pages_checked=count, pages=rows)
            with self.assertRaises(AssertionError):
                validate_fresh_audit(report, self.payload, self.saved, self.now)


if __name__ == '__main__':
    unittest.main()
