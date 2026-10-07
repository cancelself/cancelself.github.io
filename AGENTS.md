# AGENTS.md

## Keep README.md in sync with index.md

`README.md` mirrors the body of `index.md` (the site's homepage). Any edit to `index.md` must be applied to `README.md` as well, and vice versa. The README has no Jekyll frontmatter or `# The Great Matter` H1 line, but everything from the `**Godō...**` byline onward should match.

## `## Heading <!--+-->` is a disclosure-triangle marker, not a typo

Headings written with a trailing `<!--+-->` HTML comment (e.g. `## Expression <!--+-->`) are **intentional**. They render as ordinary `<h2>` headings on github.com (clean text, auto-anchored, bookmarkable) because GitHub strips HTML comments. On the rendered Jekyll site, the custom renderer in `_layouts/default.html` matches `^(#{1,4}) (.+?) <!--\+-->\s*$` and wraps the heading and everything beneath it in a collapsible `<details>` element — closed by default, opened by clicking the disclosure triangle (▶ / ▼).

A `<details>` block stays open until the next heading at the same or a higher level, or end of file. Lower-level headings remain inside it. Lower-level headings with their own `<!--+-->` markers create nested disclosures, allowing documents such as `inspiration.md` to render as an outline.

Use this for sections that are part of the document but should not demand the reader's attention on first read (e.g. personal expression pieces, appendices). Use plain `## Heading` for sections that should always render expanded.

Do **not** strip the `<!--+-->` marker. The earlier `##+ Heading` form was replaced by this convention so that the same source renders correctly in both Jekyll and GitHub's native markdown view (see commit `849e8de`).
