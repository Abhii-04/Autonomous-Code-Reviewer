import unittest

from src.tools.treesitter import tree_sitter_segmenter


class TreeSitterSegmenterTests(unittest.TestCase):
    def test_segments_supported_languages(self):
        newline = "\n"
        samples = {
            "py": "def hello(name):\n    return name\n\nclass A:\n    pass",
            "js": "function hello(name){ return name; }\nclass A {}",
            "ts": "function hello(name: string): string { return name; }\nclass A {}",
            "c": "int hello(int x){ return x; }",
            "cpp": "class A {};\nint hello(int x){ return x; }",
        }

        for language, code in samples.items():
            with self.subTest(language=language):
                result = tree_sitter_segmenter.invoke(
                    {"code": code, "language": language}
                )

                self.assertIn("Chunks found:", result)
                self.assertIn("--- Simplified code ---", result)
                self.assertNotIn("segmentation failed", result.lower())
                self.assertNotIn("syntax errors", result.lower())
                self.assertGreater(len(result.split(newline)), 3)

    def test_reports_invalid_input(self):
        result = tree_sitter_segmenter.invoke({"code": "", "language": "py"})

        self.assertEqual(result, "No code provided for Tree-sitter segmentation.")


if __name__ == "__main__":
    unittest.main()
