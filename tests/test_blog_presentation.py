from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BlogPresentationTests(unittest.TestCase):
    def test_every_post_keeps_one_bilingual_content_pair(self):

        posts = sorted((ROOT / "_posts").glob("*.md"))

        self.assertEqual(47, len(posts))
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

        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertIn("rgba(248, 250, 252, 0.56)", head)
        self.assertIn("rgba(241, 245, 249, 0.68)", head)

    def test_writeup_typography_avoids_accidental_heavy_text(self):

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

        archives = (ROOT / "_layouts" / "archives.html").read_text(encoding="utf-8")

        self.assertIn('group_by_exp: "post", "post.categories[0]"', archives)
        self.assertIn("assign t_size = t_posts | size", archives)
        self.assertIn("competition-timeline-entry", archives)
        self.assertIn("/competitions/{{ info.slug }}/", archives)
        self.assertNotIn("{% for post in t_posts %}", archives)
        self.assertNotIn("3 Competitions", archives)
        self.assertNotIn("40 Writeups", archives)
        self.assertNotIn('assign tournament_list = "', archives)

    def test_light_competition_details_and_clean_section_headings(self):
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
        home = (ROOT / "_layouts" / "home.html").read_text(encoding="utf-8")
        categories = (ROOT / "_layouts" / "categories.html").read_text(encoding="utf-8")
        archives = (ROOT / "_layouts" / "archives.html").read_text(encoding="utf-8")

        self.assertIn('html:not([data-bs-theme="dark"]) .competition-detail-hero {', head)
        self.assertIn("background: #fff", head)
        self.assertNotIn("competition-eyebrow", home)
        self.assertNotIn("Khám phá bài giải", home)
        self.assertNotIn("Chọn cuộc thi", categories)
        self.assertNotIn("competition-see-all", categories)
        self.assertNotIn("competition-section-lead", archives)

    def test_competition_navigation_keeps_subjects_scoped(self):

        categories = (ROOT / "_layouts" / "categories.html").read_text(encoding="utf-8")
        post = (ROOT / "_layouts" / "post.html").read_text(encoding="utf-8")
        detail = (ROOT / "_layouts" / "competition.html").read_text(encoding="utf-8")

        self.assertIn('post.categories[0] == competition.name', categories)
        self.assertIn('group_by_exp: "post", "post.categories[1]"', categories)
        self.assertIn('<details class="competition-category">', categories)
        self.assertNotIn('<details class="competition-category" open>', categories)
        self.assertNotIn('/categories/{{ sub_category', categories)
        self.assertIn('/competitions/', post)
        self.assertIn('site.data.competitions | where: "name", competition_name | first', post)
        self.assertIn('#{{ subject_slug }}', post)
        self.assertIn('post.categories[0] == page.competition', detail)

    def test_sunshine_posts_use_the_requested_subjects(self):
        expected = {
            "2026-09-26-vecnet.md": "Misc",
            "2026-09-26-this-code-s-got-bars.md": "OSINT",
        }
        for filename, subject in expected.items():
            content = (ROOT / "_posts" / filename).read_text(encoding="utf-8")
            self.assertIn(f'categories: ["SunshineCTF 2026", "{subject}"]', content)
        self.assertFalse((ROOT / "_posts" / "2026-09-26-helpdesk-freebie.md").exists())

    def test_pointer_overflow_writeup_has_its_own_osint_competition(self):
        post = (ROOT / "_posts" / "2026-09-30-where-the-light-fails-to-fall.md").read_text(encoding="utf-8")
        competition = (ROOT / "competitions" / "poctf-2026.md").read_text(encoding="utf-8")
        catalog = (ROOT / "_data" / "competitions.yml").read_text(encoding="utf-8")
        poctf_posts = [
            item for item in (ROOT / "_posts").glob("*.md")
            if 'categories: ["Pointer Overflow CTF 2026", ' in item.read_text(encoding="utf-8")
        ]

        self.assertIn('categories: ["Pointer Overflow CTF 2026", "OSINT"]', post)
        self.assertEqual(8, len(poctf_posts))
        self.assertIn("permalink: /competitions/poctf-2026/", competition)
        self.assertIn("https://pointeroverflowctf.com/img/logo-mini.png", catalog)
        self.assertEqual(6, post.count("POCTF{99.623.3YOADRV22RFD27OD.DSGJUSWQHG734ELY3KPFEDNF4F}"))

    def test_home_has_one_authentic_image_card_per_competition(self):

        home = (ROOT / "_layouts" / "home.html").read_text(encoding="utf-8")
        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
        self.assertIn("site.data.competitions", home)
        self.assertIn('post.categories[0] == competition.name', home)
        self.assertIn('class="competition-card ', home)
        self.assertIn('.competition-card-image .preview-img::before {', head)

        for slug, extension in (
            ("poctf-2026", "png"),
            ("h7ctf-2026", "png"),
            ("sunshinectf-2026", "png"),
            ("ptitctf-2026", "jpg"),
        ):
            self.assertTrue((ROOT / "competitions" / f"{slug}.md").is_file())
            self.assertTrue((ROOT / "assets" / "img" / "competitions" / f"{slug}.{extension}").is_file())

    def test_shared_template_has_language_controller(self):

        head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")

        self.assertIn("function syncLanguageUi", head)
        self.assertIn("function filterTocForLanguage", head)
        self.assertIn("localStorage.setItem('blog_lang_pref', targetLang)", head)

    def test_language_controller_survives_html_whitespace_compression(self):

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


if __name__ == "__main__":
    unittest.main()
