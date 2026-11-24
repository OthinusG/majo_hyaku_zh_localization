import unittest
from copy import deepcopy

from verify_alignment import verify_alignment


class VerifyAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.source = {
            "meta": {"total_entries": 2},
            "entries": [
                {"id": "a", "type": "text", "jp": "%02d\n%s %lld", "zh": "", "loc": {"row": 1}},
                {"id": "b", "type": "placeholder", "jp": "●▼", "zh": "", "loc": {"row": 2}},
            ],
        }
        self.translation = deepcopy(self.source)

    def test_draft_and_complete_translation(self):
        self.assertEqual(verify_alignment(self.source, self.translation), (2, 2))
        with self.assertRaisesRegex(ValueError, "empty zh"):
            verify_alignment(self.source, self.translation, require_complete=True)
        self.translation["entries"][0]["zh"] = "编号 %02d\n%s：%lld"
        self.translation["entries"][1]["zh"] = "●▼"
        self.assertEqual(verify_alignment(self.source, self.translation, require_complete=True), (2, 0))

    def test_rejects_format_changes(self):
        for text in ("%02d %s %lld", "%s\n%02d %lld", "%02d\n%s %ld"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "format tokens"):
                self.translation["entries"][0]["zh"] = text
                verify_alignment(self.source, self.translation)

    def test_rejects_coordinate_and_placeholder_changes(self):
        self.translation["entries"][1]["zh"] = "●"
        with self.assertRaisesRegex(ValueError, "placeholder"):
            verify_alignment(self.source, self.translation)
        self.translation["entries"][0]["loc"]["row"] = 2
        with self.assertRaisesRegex(ValueError, "loc differs"):
            verify_alignment(self.source, self.translation)

    def test_rejects_removed_or_reordered_entries(self):
        self.translation["entries"].reverse()
        with self.assertRaisesRegex(ValueError, "id differs"):
            verify_alignment(self.source, self.translation)
        self.translation["entries"].pop()
        with self.assertRaisesRegex(ValueError, "Entry count"):
            verify_alignment(self.source, self.translation)


if __name__ == "__main__":
    unittest.main()
