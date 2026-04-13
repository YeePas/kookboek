---
name: kookboek-recept
description: >
  Skill for managing the "Foodnotes" personal cookbook website built with Eleventy (11ty)
  and Decap CMS. Triggers when the user wants to add or edit recipes, add photos, manage
  categories, or make changes to the cookbook. Trigger keywords: recepten, kookboek, recept
  toevoegen, foto toevoegen, ingredienten, bereiding, hoofdstuk, categorie, foodnotes.
  Also triggers for Dutch food/cooking-related requests in the context of this project.
---

# Foodnotes - Recipe Management Skill

## Project Overview

"Foodnotes" is a personal cookbook website styled as an editorial magazine, inspired by **The Gourmand**. Built with **Eleventy (11ty)** static site generator and **Decap CMS** for visual editing. Hosted on GitHub Pages.

### Tech Stack
- **Eleventy 3.x** — static site generator
- **Nunjucks** — template engine
- **Decap CMS** — visual content editor at `/admin`
- **GitHub Pages** — hosting via GitHub Actions
- **YAML frontmatter in Markdown** — recipe data format

### Design System

- **Typography**: `Instrument Serif` (Google Fonts) for headings; system sans-serif for body
- **Colors**: Black (`#111`) on white (`#FFF`) with muted grey (`#777`), soft bg (`#F2F1EE`), borders (`#D0D0D0`)
- **Navigation**: Dark top bar with serif "Foodnotes" brand link, Inhoud/Register links
- **Cover** (`/`): Full-viewport dark background, large serif title, auto recipe count
- **TOC** (`/inhoud/`): Magazine grid of recipe cards + classic list grouped by category
- **Recipes** (`/recepten/{category}/{slug}/`): Full-width hero image, 720px centered content
- **Register** (`/register/`): Auto-generated alphabetical keyword index from tags
- **Chapters** (`/recepten/{category}/`): Auto-generated from `categories.json`

### Project Structure

```
kookboek/
├── eleventy.config.js          — 11ty config (filters, collections, passthrough)
├── package.json                — npm project with 11ty dependency
├── fotos/                      — Recipe photos (.webp), served at /fotos/
├── src/                        — 11ty input directory
│   ├── index.njk               — Cover page (auto recipe count)
│   ├── inhoud.njk              — TOC (auto grid + list from collection)
│   ├── register.njk            — Keyword index (auto from tags)
│   ├── chapters.njk            — Paginated chapter pages from categories.json
│   ├── style.css               — Shared stylesheet
│   ├── admin/
│   │   ├── index.html          — Decap CMS entry point
│   │   └── config.yml          — CMS collection/field definitions
│   ├── _data/
│   │   └── categories.json     — Category metadata (title, order, roman, description)
│   ├── _includes/
│   │   ├── base.njk            — HTML shell (head, nav, content)
│   │   ├── recipe.njk          — Recipe page template
│   │   ├── chapter.njk         — Chapter page template
│   │   └── partials/
│   │       └── nav.njk         — Navigation bar partial
│   └── recepten/
│       ├── recepten.json        — Directory data (layout: recipe.njk, permalink pattern)
│       ├── kimchi.md
│       ├── ossobuco-alla-milanese.md
│       └── spitskool-sichuan.md
└── _site/                      — Generated output (gitignored)
```

---

## Recipe Markdown Format

Each recipe is a `.md` file in `src/recepten/` with YAML frontmatter. The body is empty (all data in frontmatter).

```yaml
---
title: "Recipe Name"
subtitle: "Short evocative description of the dish."
category: "vlees"              # Must match a slug in categories.json
foto: "recipe-name.webp"       # Filename in fotos/ dir, or "" if no photo
pageNumber: 6                  # Unique, determines sort order

meta:                          # Flexible metadata cells (usually 4)
  - label: "Personen"
    value: "4"
  - label: "Voorber."
    value: "15 min"
  - label: "Bereiding"
    value: "30 min"
  - label: "Niveau"
    value: "makkelijk"

ingredienten:                  # Groups with items
  - groep: "Group Name"       # Optional, use "" for ungrouped
    items:
      - "200 g ingredient"
      - "1 el olijfolie"

stappen:                       # Use **bold** for step labels
  - "**Stap label:** Description of the step."
  - "Another step without a bold label."

tips:                          # Optional
  - "A helpful tip."

variaties:                     # Optional
  - "A variation suggestion."

bron: "Source attribution."    # Optional

tags:                          # Used for register/keyword index
  - "categorie-tag"
  - "keuken"
  - "seizoen"
---
```

### Important Notes
- **`meta`** uses flexible label/value pairs. Common labels: Personen, Voorber., Bereiding, Niveau, Opbrengst, Ferment.
- **`ingredienten`** groups display as small uppercase headers. Use `groep: ""` for recipes without sub-groups.
- **`stappen`** support inline markdown (`**bold**` → `<strong>`).
- **`pageNumber`** must be unique across all recipes — it determines global sort order and prev/next navigation.
- **`tags`** feed the auto-generated register. The recipe title is also auto-added as a keyword.

---

## Workflow: Adding a New Recipe

With 11ty, adding a recipe is simple — just create one Markdown file.

### Step 1: Create the Markdown file

Create `src/recepten/{recipe-slug}.md` with the YAML frontmatter schema above.

**Naming conventions:**
- Lowercase, hyphen-separated: `ossobuco-alla-milanese.md`
- No spaces, accents, or special characters

### Step 2: Determine pageNumber

Check existing recipes for the highest `pageNumber` and use the next integer. This number must be unique — it controls sort order and prev/next navigation.

### Step 3: Add photo (optional)

If a photo is available:
1. Copy/move the photo to `fotos/{recipe-slug}.webp`
2. Set `foto: "{recipe-slug}.webp"` in the frontmatter

If no photo: set `foto: ""` and a placeholder will be shown.

### That's it!

Everything else is **automatic**:
- Recipe page generated at `/recepten/{category}/{slug}/`
- Prev/next navigation based on `pageNumber` sort order
- Recipe badge (`Category / 003`) auto-generated
- Cover page recipe count updates automatically
- TOC grid card + list entry added automatically
- Register/keyword index entries from tags generated automatically
- Chapter page updated with new recipe automatically

---

## Workflow: Adding a New Category

### Step 1: Add to categories.json

Edit `src/_data/categories.json` and add a new entry to the array:

```json
{
  "slug": "vis",
  "title": "Vis & Zeevruchten",
  "order": 4,
  "roman": "IV",
  "description": "Verse vis en schaaldieren — van eenvoudig gebakken tot verfijnd bereid."
}
```

### Step 2: Add to Decap CMS config

Add the new category option to `src/admin/config.yml` in the category select widget.

### That's it!

A chapter page is automatically generated at `/recepten/{slug}/`.

---

## Workflow: Adding a Photo to a Recipe

1. Copy the photo to `fotos/{recipe-slug}.webp`
2. Update the recipe's `foto` field in frontmatter: `foto: "{recipe-slug}.webp"`

Both the hero image and the TOC card image update automatically.

---

## Auto-Generated Features (via 11ty)

| Feature | How It Works |
|---------|--------------|
| **Recipe count** | `collections.recepten.length` on cover |
| **TOC grid** | Loops over `collections.recepten` |
| **TOC list** | `groupByCategory` filter groups + sorts by category order |
| **Register** | `buildKeywordIndex` filter builds from title + tags |
| **Prev/Next nav** | `prevRecipe`/`nextRecipe` filters based on pageNumber sort |
| **Chapter pages** | Pagination over `categories.json` array |
| **Recipe badge** | `categoryTitle` + `pad(3)` filters |

---

## Development

```bash
# Install dependencies
npm install

# Dev server with hot reload
npm run dev     # → npx @11ty/eleventy --serve

# Production build
npm run build   # → npx @11ty/eleventy

# CMS: visit /admin/ in browser (requires GitHub OAuth app)
```

---

## Important Reminders

- **Work directly on main branch** for recipes — no branches or PRs needed.
- All styling is in `src/style.css` — never duplicate CSS.
- Recipe files need NO body content — everything is in YAML frontmatter.
- The `pageNumber` field is the single source of truth for ordering.
- Photos go in the root `fotos/` directory (not `src/fotos/`), served via passthrough copy.
- Build output goes to `_site/` (gitignored).
