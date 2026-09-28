# CTF Write-ups Presentation Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the blog switch languages reliably, show a language-correct table of contents, use readable typography and title-case navigation, and use Van Gogh's *Irises* in light mode.

**Architecture:** The root `data-lang` attribute is the only language state. The shared head include supplies declarative visibility CSS plus a small controller that synchronizes controls and filters TOC links by the language class of their target heading. The artwork stays local, so light mode has no runtime external-image dependency.

**Tech Stack:** Jekyll 4 / Chirpy 7.6, Liquid, HTML, CSS, vanilla JavaScript, Python standard-library tests, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-29-ctf-writeups-repair-design.md`

## Global Constraints

- Preserve every post's existing technical prose and flags.
- Use English if browser storage is unavailable.
- Do not change dark-mode *The Starry Night*.
- Keep `pre`, `code`, and syntax-highlighted blocks monospaced.
- Introduce no runtime external image request.
- Do not uppercase sidebar navigation through markup or CSS.

## Review Focus

- Storage unavailable: English remains visible and every control works.
- A TOC link with a missing target does not throw.
- A TOC heading outside a language block remains visible in both languages.
- Every post retains exactly one `.lang-vn` and one `.lang-en` content block.
- Code samples and flags retain existing capitalization and monospaced rendering.

---

## File Structure

| Path | Responsibility |
| --- | --- |
| `tests/test_blog_presentation.py` | Dependency-free regression checks for bilingual structure and shared templates. |
| `_includes/head.html` | Language CSS/controller, TOC filtering, type styles, and light artwork declaration. |
| `_includes/sidebar.html` | Title-case bilingual navigation copy. |
| `assets/img/vangogh-light.jpg` | Local public-domain *Irises* image. |

### Task 1: Add regression coverage for shared presentation rules

**Files:**
- Create: `tests/test_blog_presentation.py`
- Test: `tests/test_blog_presentation.py`

**Interfaces:**
- Consumes: repository-root `_posts`, `_includes/head.html`, and `_includes/sidebar.html`.
- Produces: `python -m unittest tests.test_blog_presentation` as the pre-publish regression command.

- [ ] **Step 1: Write the failing test**

Create `BlogPresentationTests` to assert all 40 Markdown files have one `.lang-vn` and one `.lang-en` block, and to assert that the shared template contains the new controller and title-case navigation.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest tests.test_blog_presentation -v`

Expected: FAIL because the new controller and labels do not exist.

- [ ] **Step 3: Keep the tests standalone**

Use only `pathlib` and `unittest`; do not require Jekyll, Bundler, or a network connection.

### Task 2: Repair language state, TOC filtering, typography, and capitalization

**Files:**
- Modify: `_includes/head.html:137-495`
- Modify: `_includes/sidebar.html:29-59`
- Test: `tests/test_blog_presentation.py`

**Interfaces:**
- Consumes: every `.lang-btn` and the root `data-lang` attribute.
- Produces: `window.setLanguage(lang)` and `filterTocForLanguage(lang)`.

- [ ] **Step 1: Extend the failing test**

Require `syncLanguageUi`, `filterTocForLanguage`, safe `localStorage` handling, Source Sans Pro prose styling, and a monospace code selector.

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `python -m unittest tests.test_blog_presentation.BlogPresentationTests.test_shared_template_has_language_controller -v`

Expected: FAIL with missing named behavior.

- [ ] **Step 3: Replace the imperative display controller**

Implement `setLanguage(lang)` to normalize `vn`/`en`, update the root attribute, persist safely, synchronize `aria-selected`/`.active`, and call the TOC filter. Do not set inline display styles on language content nodes.

- [ ] **Step 4: Add language-aware TOC filtering**

Resolve each TOC anchor target. Hide its link only if the target heading's closest `.lang-vn` or `.lang-en` container does not match the selected language; keep missing-target and structural links visible. Invoke after DOM readiness and `pageshow`.

- [ ] **Step 5: Apply typography and title-case navigation**

Set prose to Source Sans Pro/system fallback, preserve the theme monospace stack for code, override sidebar text transformation, and convert only hard-coded sidebar labels to normal title case.

- [ ] **Step 6: Run regression coverage**

Run: `python -m unittest tests.test_blog_presentation -v`

Expected: PASS.

- [ ] **Step 7: Commit the implementation and tests**

Run: `git add tests/test_blog_presentation.py _includes/head.html _includes/sidebar.html`

Run: `git commit -m "fix: stabilize bilingual write-up presentation"`

### Task 3: Replace the light-mode artwork and validate the rendered site

**Files:**
- Modify: `assets/img/vangogh-light.jpg`
- Modify: `_includes/head.html:201-238` only if overlay contrast requires it.
- Test: `tests/test_blog_presentation.py`

**Interfaces:**
- Consumes: the existing light-mode image URL and CSS selectors.
- Produces: a local *Irises* backdrop for the light sidebar and topbar.

- [ ] **Step 1: Download the public-domain image**

Download a public-domain rendering of Vincent van Gogh's *Irises* (1889) into `assets/img/vangogh-light.jpg`, retaining the current path.

- [ ] **Step 2: Inspect contrast and adjust only the light overlay if needed**

Keep the pale overlay unless navigation text is not comfortably legible. Do not modify dark mode.

- [ ] **Step 3: Run static and JavaScript checks**

Run: `python -m unittest tests.test_blog_presentation -v`

Run: parse the extracted language-controller script with Node through a temporary file on Windows.

Expected: all tests pass and JavaScript emits no parser errors.

- [ ] **Step 4: Attempt the Jekyll build and HTML checker**

Run: `bundle exec jekyll build --trace`

Run: `bundle exec htmlproofer _site --disable-external`

Expected: both pass; if Bundler is unavailable, record it and use the deployed GitHub Actions build as the authoritative check.

- [ ] **Step 5: Verify the public site in Chrome**

Test EN then VN on the home page and FleetLink, inspect visible content and TOC labels, switch light/dark mode, and check console errors. Capture the successful light-mode post view for handoff.

- [ ] **Step 6: Commit artwork and final changes**

Run: `git add assets/img/vangogh-light.jpg _includes/head.html tests/test_blog_presentation.py`

Run: `git commit -m "style: refresh light theme with Van Gogh irises"`
