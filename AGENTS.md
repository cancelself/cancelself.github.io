# AGENTS.md

## Keep README.md in sync with index.md

`README.md` mirrors the body of `index.md` (the site's homepage). Any edit to `index.md` must be applied to `README.md` as well, and vice versa. The README omits the Jekyll frontmatter at the top of `index.md`, but everything from `# The Great Matter` onward should match (with blank lines or trailing two spaces where needed for GitHub Markdown line breaks).

## `## Heading <!---->` / `<!--+-->` are disclosure-triangle markers, not typos

Headings written with a trailing `<!---->` or `<!--+-->` HTML comment (e.g. `## Inspiration <!---->`, `## Expression <!--+-->`) are **intentional**. They render as ordinary `<h2>` headings on github.com (clean text, auto-anchored, bookmarkable) because GitHub strips HTML comments. On the rendered Jekyll site, the custom renderer in `_layouts/default.html` matches `^(#{1,6}) (.+?) <!--(\+?)-->\s*$` and wraps the heading and everything beneath it in a collapsible `<details>` element with a disclosure triangle (▶ / ▼):

- `<!---->` — **closed** by default; the reader clicks the triangle to reveal the content.
- `<!--+-->` — **open** by default; the content shows and the reader can still collapse it.

A `<details>` block continues until the next heading at the same or a higher level, or end of file. Lower-level headings remain inside it. Lower-level headings with their own markers create nested disclosures, allowing documents such as `inspiration.md` to render as an outline.

Use closed disclosures for sections that are part of the document but should not demand the reader's attention on first read (e.g. appendices). Use plain `## Heading` for sections that should always render expanded with no triangle.

Do **not** strip these markers. The earlier `##+ Heading` form was replaced by this convention so that the same source renders correctly in both Jekyll and GitHub's native markdown view (see commit `849e8de`).

The `<!-- inspiration-outline -->` marker in `index.md` and `README.md` embeds the body of `inspiration.md` inside the homepage's Inspiration disclosure. The renderer shifts its heading levels down one so its disclosure hierarchy nests beneath the homepage section.
