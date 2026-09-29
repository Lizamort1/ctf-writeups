# Archive list

Source: `_layouts/archives.html`; styles: `_includes/head.html`.

- Data: group `site.posts` by the first category; derive competition and post counts from the same collection.
- Structure: one competition card with a heading, count, and list of links. Each row displays the second category, full post title, and publication date.
- Desktop: three grid columns (category, flexible title, date). Titles wrap without clipping.
- Mobile: category occupies the first line; title and date occupy the second line.
- Behavior: links navigate to posts; row hover provides a subtle background. EN/VN labels follow the shared language controller.
- Constraint: do not use the theme's `#archives` ID because it activates Chirpy's timeline layout.
