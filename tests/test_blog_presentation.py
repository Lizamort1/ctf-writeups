from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BlogPresentationTests(unittest.TestCase):
    def test_every_post_keeps_one_bilingual_content_pair(self):
        """Catches a post losing one language block during presentation repairs."""
        posts = sorted((ROOT / "_posts").glob("*.md"))

        self.assertEqual(40, len(posts))
        for post in posts:
            content = post.read_text(encoding="utf-8")
            self.assertEqual(
                1,
                content.count('<div class="lang-vn" markdown="1">'),
                post.name,
            )
            self.assertEqual(
                1,
                content.count('<div class="lang-en" markdown="1">'),
                post.name,
            )

    def test_sidebar_navigation_uses_title_case_labels(self):
        """Catches navigation returning to visually noisy all-caps labels."""
        sidebar = (ROOT / "_includes" / "sidebar.html").read_text(encoding="utf-8")

        for label in (
            "Trang chủ",
            "Chuyên mục",
            "Thẻ",
            "Lưu trữ",
            "Giới thiệu",
            "Home",
            "Categories",
            "Tags",
            "Archives",
            "About",
        ):
            self.assertIn(label, sidebar)

    def test_shared_template_has_language_controller(self):
        """Catches loss of the shared language switch and TOC synchronization."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertIn("function syncLanguageUi", head)
        self.assertIn("function filterTocForLanguage", head)
        self.assertIn("localStorage.setItem('blog_lang_pref', targetLang)", head)


if __name__ == "__main__":
    unittest.main()
