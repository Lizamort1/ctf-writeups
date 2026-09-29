# Design reference: anhcd05.github.io

Inspected in the browser on 2026-09-29. The reference uses Chirpy with a fixed 260px profile sidebar, a compact top bar, a readable main column, small metadata, and a separate recent-posts/tag panel. Body copy uses Source Sans Pro; headings use Lato. The dark background is near `#1b1b1e`, with restrained cards and clear hierarchy between title, summary, and metadata.

## Adaptation for Lizamort1

- Keep the existing Jekyll/Chirpy structure and all 40 technical posts.
- Show the complete local avatar image inside a rounded frame and keep the site name `Lizamort1`.
- Remove text shadows that soften lettering, increase dark-mode text contrast, and use regular weight for prose and archive post titles. Reserve semibold for headings and intentional emphasis.
- Organize archives by competition and category. Use a responsive three-column row with category, title, and date. Avoid Chirpy's built-in `#archives` timeline selector, which was applying unrelated vertical lines and spacing.
- Keep language controls in the shared sidebar/top bar; remove redundant controls from the archive and category bodies.

## Verification targets

- Home, post, archive, and category pages in dark and light modes.
- Archive rows aligned on desktop and stacked without clipping on mobile.
- EN/VN controls and local avatar remain available across pages.
