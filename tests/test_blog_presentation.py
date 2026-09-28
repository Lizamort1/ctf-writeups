from pathlib import Path
import subprocess
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

    def test_language_controller_survives_html_whitespace_compression(self):
        """Catches line comments swallowing the controller after Jekyll compression."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
        script = head.split("<script>", 1)[1].split("</script>", 1)[0]
        compressed_script = " ".join(script.splitlines())

        result = subprocess.run(
            ["node", "-e", "new Function(process.argv[1]);", compressed_script],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_toc_filter_reapplies_after_toc_regeneration(self):
        """Catches responsive TOC refreshes restoring headings from both languages."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
        script = head.split("<script>", 1)[1].split("</script>", 1)[0]
        harness = r'''
let rootLanguage = 'en';
let tocMutationCallback;
const target = {
  closest: () => ({ classList: { contains: (name) => name === 'lang-vn' } })
};
const link = {
  hidden: false,
  getAttribute: () => '#vn-heading',
  setAttribute: () => {}
};
const tocRoot = {};
const document = {
  readyState: 'complete',
  documentElement: {
    getAttribute: () => rootLanguage,
    setAttribute: (_name, value) => { rootLanguage = value; }
  },
  querySelectorAll: (selector) => {
    if (selector.includes('a[href')) return [link];
    if (selector === '#toc-wrapper, #toc-popup-content') return [tocRoot];
    return [];
  },
  getElementById: () => target,
  addEventListener: () => {}
};
const MutationObserver = class {
  constructor(callback) { tocMutationCallback = callback; }
  observe() {}
};
const window = { addEventListener: () => {}, MutationObserver };
global.document = document;
global.window = window;
new Function(process.argv[1])();
if (!tocMutationCallback) throw new Error('Expected a TOC MutationObserver');
link.hidden = false;
tocMutationCallback();
if (!link.hidden) throw new Error('Expected regenerated Vietnamese TOC link to stay hidden in English');
'''

        result = subprocess.run(
            ["node", "-e", harness, script],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
