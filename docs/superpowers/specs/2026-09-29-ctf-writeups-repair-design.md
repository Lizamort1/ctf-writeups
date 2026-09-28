# CTF write-ups blog repair design

## Purpose

Repair the shared presentation defects in the CTF write-ups blog while preserving
the technical content of all 40 posts. The public site must switch English and
Vietnamese reliably, show a table of contents for only the selected language,
render Vietnamese and code text consistently, and use a lighter Van Gogh artwork
in light mode.

## Evidence

- The public home page and a post log `SyntaxError: Unexpected end of input`.
- Selecting Vietnamese in the post language switch leaves English active.
- The post table of contents contains Vietnamese and English headings at once.
- The current light artwork is Almond Blossom; the requested replacement is a
  Van Gogh painting suited to a light background.
- The repository contains 40 posts, each with `.lang-vn` and `.lang-en` blocks.

## Scope

### Shared language behavior

- Keep `data-lang` on the root element as the single source of truth.
- Replace imperative per-element display styles with a small controller that
  synchronizes controls, persists the preference, and recalculates the table of
  contents visibility after the DOM is ready and on `pageshow`.
- Each table-of-contents link will be hidden unless its heading is inside the
  selected language block. Links to non-language structural headings remain
  visible.
- Keep the existing EN default and all existing EN/VN post content unchanged.

### Typography and capitalization

- Apply a readable Vietnamese-capable sans-serif stack to prose and preserve
  the theme's monospaced font for `pre`, `code`, and syntax-highlighted blocks.
- Prevent automatic uppercasing in sidebar navigation.
- Replace hard-coded all-caps Vietnamese/English sidebar labels with normal
  title case. Do not alter challenge titles, flags, acronyms, commands, or code.

### Artwork

- Replace `assets/img/vangogh-light.jpg` with a locally stored public-domain
  rendering of Vincent van Gogh's *Irises* (1889).
- Retain the existing light overlay, adjusted only if needed to keep text and
  controls at accessible contrast on the new artwork.
- Keep the dark-mode *The Starry Night* artwork unchanged.

## Files and responsibilities

| File | Change |
| --- | --- |
| `_includes/head.html` | Light artwork reference, language controller, typography, TOC filtering, and shared visual styles. |
| `_includes/sidebar.html` | Human-readable navigation labels without all-caps text. |
| `assets/img/vangogh-light.jpg` | Replacement *Irises* image. |
| `_posts/*.md` | No content rewrite; validation only confirms all 40 keep the shared bilingual structure. |

## Error handling and accessibility

- Browser storage failures must fall back to English without breaking controls.
- Controls must update `aria-selected` and preserve keyboard-operable buttons.
- A missing TOC or an unresolved link must be ignored safely.
- No external image dependency is introduced at runtime.

## Verification

1. Parse the rendered custom JavaScript before publishing.
2. Build the Jekyll site and run the existing HTML checker when the local Ruby
   toolchain is available; record an environment limitation otherwise.
3. Statistically verify all 40 posts retain exactly one Vietnamese and one
   English content block.
4. In Chrome, verify both languages on the home page and a representative post,
   confirm the selected TOC contains only the matching language's headings,
   inspect light and dark artwork, and confirm zero console errors caused by
   the custom script.
