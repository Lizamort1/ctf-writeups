from pathlib import Path
import re
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

    def test_site_identity_and_avatar_are_presented_completely(self):
        """Keeps the public brand name and fills the round avatar without a white ring."""
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertRegex(config, r"(?m)^title:\s*Lizamort1\s*(?:#.*)?$")
        self.assertRegex(config, r"(?m)^  name:\s*Lizamort1\s*$")
        avatar_rule = re.search(r"#sidebar #avatar img\s*\{(?P<body>.*?)\}", head, re.S)
        self.assertIsNotNone(avatar_rule)
        self.assertIn("object-fit: cover", avatar_rule.group("body"))
        frame_rule = re.search(r"#sidebar #avatar\s*\{(?P<body>.*?)\}", head, re.S)
        self.assertIsNotNone(frame_rule)
        self.assertIn("border-radius: 50%", frame_rule.group("body"))
        self.assertIn("border: 0", frame_rule.group("body"))
        self.assertIn("background: transparent", frame_rule.group("body"))
        sidebar = (ROOT / "_includes" / "sidebar.html").read_text(encoding="utf-8")
        self.assertIn('loading="eager"', sidebar)
        self.assertNotIn("sidebar-lang-switch", sidebar)
        title_rule = re.search(
            r"(?m)^    #sidebar \.site-title\s*\{(?P<body>.*?)\}", head, re.S
        )
        self.assertIsNotNone(title_rule)
        self.assertIn("font-weight: 600", title_rule.group("body"))

    def test_light_sidebar_keeps_van_gogh_art_visible(self):
        """Catches the light overlay returning to the washed-out screenshot state."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertIn("rgba(248, 250, 252, 0.56)", head)
        self.assertIn("rgba(241, 245, 249, 0.68)", head)

    def test_writeup_typography_avoids_accidental_heavy_text(self):
        """Quoted challenge descriptions should not use monospace code formatting."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertIn(".content strong", head)
        self.assertIn("font-weight: 600", head)
        self.assertNotIn(".content p > code:only-child", head)
        for post in (ROOT / "_posts").glob("*.md"):
            content = post.read_text(encoding="utf-8")
            lines = content.splitlines()
            for index, line in enumerate(lines):
                if "Mô tả thử thách:" in line:
                    next_content = next((item for item in lines[index + 1:] if item.strip()), "")
                    self.assertTrue(
                        next_content.startswith("> "),
                        f"Challenge description should be a quotation in {post.name}",
                    )

    def test_archives_are_derived_from_posts_instead_of_hard_coded(self):
        """The timeline contains one linked row per competition, never one per writeup."""
        archives = (ROOT / "_layouts" / "archives.html").read_text(encoding="utf-8")

        self.assertIn('group_by_exp: "post", "post.categories[0]"', archives)
        self.assertIn("site.posts | size", archives)
        self.assertIn("assign t_size = t_posts | size", archives)
        self.assertIn("competition-timeline-entry", archives)
        self.assertIn("/competitions/{{ info.slug }}/", archives)
        self.assertNotIn("{% for post in t_posts %}", archives)
        self.assertNotIn("3 Competitions", archives)
        self.assertNotIn("40 Writeups", archives)
        self.assertNotIn('assign tournament_list = "', archives)

    def test_competition_navigation_keeps_subjects_scoped(self):
        """Shared subject names must not link back to global category archives."""
        categories = (ROOT / "_layouts" / "categories.html").read_text(encoding="utf-8")
        post = (ROOT / "_layouts" / "post.html").read_text(encoding="utf-8")
        detail = (ROOT / "_layouts" / "competition.html").read_text(encoding="utf-8")

        self.assertIn('post.categories[0] == competition.name', categories)
        self.assertIn('group_by_exp: "post", "post.categories[1]"', categories)
        self.assertNotIn('/categories/{{ sub_category', categories)
        self.assertIn('/competitions/', post)
        self.assertIn('#{{ subject_slug }}', post)
        self.assertIn('post.categories[0] == page.competition', detail)

    def test_home_has_one_authentic_image_card_per_competition(self):
        """Checks each competition landing page and its local event image are present."""
        home = (ROOT / "_layouts" / "home.html").read_text(encoding="utf-8")
        self.assertIn("site.data.competitions", home)
        self.assertIn('post.categories[0] == competition.name', home)
        self.assertIn('class="competition-card ', home)

        for slug, extension in (
            ("h7ctf-2026", "png"),
            ("sunshinectf-2026", "png"),
            ("ptitctf-2026", "jpg"),
        ):
            self.assertTrue((ROOT / "competitions" / f"{slug}.md").is_file())
            self.assertTrue((ROOT / "assets" / "img" / "competitions" / f"{slug}.{extension}").is_file())

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

    def test_switching_language_redraws_visible_mermaid_diagram(self):
        """Chirpy must recalculate an SVG that was measured while hidden."""
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
        script = head.split("<script>", 1)[1].split("</script>", 1)[0]
        harness = r'''
let language = 'en';
const messages = [];
const document = {
  readyState: 'complete',
  documentElement: {
    getAttribute: () => language,
    setAttribute: (_name, value) => { language = value; }
  },
  querySelectorAll: () => [],
  querySelector: (selector) => selector === '.mermaid' ? {} : null,
  addEventListener: () => {}
};
const window = {
  addEventListener: () => {},
  postMessage: (message) => messages.push(message)
};
global.document = document;
global.window = window;
new Function(process.argv[1])();
window.setLanguage('vn');
window.setLanguage('vn');
window.setLanguage('en');
if (messages.length !== 2 || messages.some(m => m.id !== 'theme-updated')) {
  throw new Error('Expected one Mermaid redraw per actual language change');
}
'''
        result = subprocess.run(
            ["node", "-e", harness, script],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_post_translations_share_flags_and_technical_blocks(self):
        """Prevents English write-ups from inventing another exploit or flag."""
        for post in (ROOT / "_posts").glob("*.md"):
            content = post.read_text(encoding="utf-8")
            vn = content.split('<div class="lang-vn" markdown="1">', 1)[1].split("</div>", 1)[0]
            en = content.split('<div class="lang-en" markdown="1">', 1)[1].split("</div>", 1)[0]
            flags = lambda body: set(re.findall(r"\b[A-Z][A-Z0-9_]*\{[A-Za-z0-9_:-]+\}", body))
            def blocks(body):
                found = re.findall(r"(?ms)^```([^\n]*)\n(.*?)^```\s*$", body)
                return [
                    (kind, re.sub(r'"(?:\\.|[^"\\])*"', '""', code) if kind == "mermaid" else code)
                    for kind, code in found
                ]
            self.assertEqual(flags(vn), flags(en), post.name)
            self.assertEqual(blocks(vn), blocks(en), post.name)
            strip_fences = lambda body: re.sub(r"(?ms)^```.*?^```\s*$", "", body)
            inline_code = lambda body: set(re.findall(r"(?<!`)`([^`\n]+)`(?!`)", strip_fences(body)))
            headings = lambda body: [len(mark) for mark in re.findall(r"(?m)^(#{1,6}) ", body)]
            self.assertEqual(inline_code(vn), inline_code(en), post.name)
            self.assertEqual(headings(vn), headings(en), post.name)
            self.assertEqual(vn.count("**"), en.count("**"), post.name)


if __name__ == "__main__":
    unittest.main()
