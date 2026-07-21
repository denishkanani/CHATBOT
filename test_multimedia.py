import os
import tempfile
import unittest
import zipfile

from multimedia import extract_text_from_file


class MultimediaParserTests(unittest.TestCase):
    def test_text_files_are_parsed(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write("Hello world from the uploaded file.")
            path = handle.name
        try:
            text, metadata = extract_text_from_file(path, "notes.txt")
            self.assertIn("Hello world", text)
            self.assertEqual(metadata["file_type"], "text")
        finally:
            os.remove(path)

    def test_json_files_are_parsed(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write('{"title": "Demo", "items": [1, 2, 3]}')
            path = handle.name
        try:
            text, metadata = extract_text_from_file(path, "data.json")
            self.assertIn("Demo", text)
            self.assertEqual(metadata["file_type"], "json")
        finally:
            os.remove(path)

    def test_zip_files_are_parsed(self):
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as handle:
            path = handle.name
        try:
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("notes.txt", "Zip contents are readable.")
            text, metadata = extract_text_from_file(path, "bundle.zip")
            self.assertIn("Zip contents", text)
            self.assertEqual(metadata["file_type"], "zip")
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
