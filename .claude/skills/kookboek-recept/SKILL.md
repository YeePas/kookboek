---
name: kookboek-recept
description: >
  Comprehensive skill for managing the "Mijn Kookboek" personal cookbook website.
  Triggers when the user wants to add or edit recipes, add photos, create category
  chapters, or make any changes to the kookboek cookbook website. Trigger keywords:
  recepten, kookboek, recept toevoegen, foto toevoegen, ingredienten, bereiding,
  hoofdstuk, categorie, inhoud bijwerken, register bijwerken. Also triggers for
  Dutch food/cooking-related requests in the context of this project (e.g. adding
  a dish, listing ingredients, updating navigation).
---

# Mijn Kookboek - Recipe Management Skill

## Project Overview

"Mijn Kookboek" is a personal cookbook website styled as an editorial magazine, inspired by **The Gourmand**. It uses a clean black-and-white aesthetic with serif typography for headings and sans-serif for body text.

### Design System

- **Typography**: `Instrument Serif` (Google Fonts) for headings; system sans-serif (`-apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif`) for body text
- **Colors**: Black (`#111111`) on white (`#FFFFFF`) with muted grey (`#777777`), subtle background (`#F2F1EE`), and light borders (`#D0D0D0`)
- **Navigation**: Dark top bar (`background: #111`) with serif brand name "Mijn Kookboek" in white, and uppercase links (Omslag, Inhoud, Register) in muted white
- **Cover page** (`index.html`): Full-viewport dark background, large serif title, recipe count
- **Table of contents** (`inhoud.html`): Magazine grid of recipe cards + classic list below
- **Recipe pages**: Full-width hero image, centered content in 720px container
- **Index** (`index-trefwoorden.html`): Two-column layout with large serif letter headings
- **Chapter pages**: Dark background, centered serif title, list of recipes in that category

### Project Structure

```
kookboek/
+-- index.html                  -- Omslag / cover page (recipe count here)
+-- inhoud.html                 -- Inhoudsopgave (toc-grid cards + toc-list)
+-- index-trefwoorden.html      -- Trefwoordenregister (alphabetical index)
+-- style.css                   -- Shared styling (do not duplicate)
+-- fotos/                      -- Recipe photos (.webp or .jpg)
+-- recepten/
    +-- fermenteren/
    |   +-- index.html           -- Chapter page
    |   +-- kimchi.html
    +-- groentes/
    |   +-- spitskool-sichuan.html
    +-- vlees/
        +-- ossobuco-alla-milanese.html
```

### Category Directories

| Directory | Category |
|-----------|----------|
| `recepten/vlees/` | Vlees |
| `recepten/vis/` | Vis & zeevruchten |
| `recepten/vegetarisch/` | Vegetarisch |
| `recepten/soepen/` | Soepen |
| `recepten/bijgerechten/` | Bijgerechten |
| `recepten/desserts/` | Desserts |
| `recepten/bakken/` | Bakken |
| `recepten/fermenteren/` | Fermenteren |
| `recepten/groentes/` | Groentes |

New categories can be added by creating a new directory under `recepten/`.

### Naming Conventions

- Filenames: **lowercase**, words separated by **hyphens**: `ossobuco-alla-milanese.html`
- No spaces, accents, or special characters in filenames
- Directory names also lowercase: `recepten/vlees/`
- Photos: `fotos/receptnaam.webp` (or `.jpg`)

---

## Workflow: Adding a New Recipe

Follow ALL of these steps when adding a new recipe. Do not skip any step.

### Step 1: Determine the recipe number and page number

Look at the existing recipes to determine:
- The next recipe number (for the badge, e.g., "006")
- The page number for the footer and register entries
- The current recipe count in `index.html`

The recipe number is a zero-padded 3-digit number shown in the badge (e.g., `Vlees / 003`). Determine the next number by checking existing recipes.

### Step 2: Create the recipe HTML file

Create a new file in the appropriate category directory: `recepten/{categorie}/{receptnaam}.html`

Use this complete template:

```html
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RECEPTNAAM — Mijn Kookboek</title>
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<nav class="site-nav"><div class="site-nav-inner">
<p class="brand">Mijn Kookboek</p>
<div>
  <a href="../../index.html">Omslag</a>
  <a href="../../inhoud.html">Inhoud</a>
  <a href="../../index-trefwoorden.html">Register</a>
</div>
</div></nav>
<div class="page recipe">
  <div class="recipe-hero-placeholder">Foto volgt</div>
  <div class="recipe-nav">
    <a href="../categorie/vorig-recept.html"><span class="arrow">&lsaquo;</span><span>Vorig</span></a>
    <a href="../categorie/volgend-recept.html"><span>Volgend</span><span class="arrow">&rsaquo;</span></a>
  </div>
  <div class="recipe-content">
    <div class="recipe-badge">CATEGORIE / NR</div>
    <h1>RECEPTNAAM</h1>
    <p class="subtitle">Korte beschrijving van het recept.</p>
    <div class="recipe-meta">
      <div class="cell"><div class="label">PERSONEN</div><div class="value">4</div></div>
      <div class="cell"><div class="label">VOORBER.</div><div class="value">15 min</div></div>
      <div class="cell"><div class="label">BEREIDING</div><div class="value">30 min</div></div>
      <div class="cell"><div class="label">NIVEAU</div><div class="value">makkelijk</div></div>
    </div>
    <div class="recipe-body">
      <div>
        <div class="section-label">Ingredienten</div>
        <ul class="ingredients">
          <li>Ingredient 1</li>
          <li>Ingredient 2</li>
        </ul>
      </div>
      <div>
        <div class="section-label">Bereiding</div>
        <div class="steps">
          <div class="step"><span class="num">01</span><span>Stap 1.</span></div>
          <div class="step"><span class="num">02</span><span>Stap 2.</span></div>
        </div>
      </div>
    </div>
    <div class="extras">
      <div class="block">
        <div class="section-label">Tips</div>
        <ul><li>Tip 1.</li></ul>
      </div>
    </div>
    <div class="recipe-footer">
      <div><span class="tag">tag1</span><span class="tag">tag2</span></div>
      <div>pagina X</div>
    </div>
  </div>
</div>
</body>
</html>
```

**Important template notes:**

- The `recipe-nav` goes BETWEEN the hero image and `recipe-content`. It overlays the bottom of the hero.
- If the recipe is the FIRST recipe (no previous), replace the prev link with `<span class="spacer"></span>`.
- If the recipe is the LAST recipe (no next), replace the next link with nothing (just omit it), but keep the spacer: `<span class="spacer"></span>` in place of the prev link if there IS a prev.
- Navigation links use relative paths from the recipe file (e.g., `../vlees/ossobuco-alla-milanese.html`).
- Step numbers are zero-padded: `01`, `02`, `03`, etc.
- The badge format is: `CATEGORIE / NR` where NR is zero-padded 3 digits (e.g., `Vlees / 003`).
- The meta grid labels are uppercase: PERSONEN, VOORBER., BEREIDING, NIVEAU (or custom like OPBRENGST, FERMENT.).
- Ingredient sub-headers use inline styles: `<li style="font-weight:500; color:#999; font-size:11px; letter-spacing:1px; text-transform:uppercase; border-bottom:none; padding-bottom:2px;">Subheader</li>` (add `margin-top:8px;` for non-first sub-headers).
- Bold labels in steps use `<strong>Label:</strong>` inside the step span.
- The footer shows `pagina X` (single page) or `pagina X / Y` (if multi-page, where Y is the total in the category or the next page).
- Tags in the footer are lowercase keywords relevant to the recipe.
- Extras can contain multiple blocks (Tips, Variaties, Bron, etc.).

### Step 3: Add card to inhoud.html toc-grid

Insert a new card inside the `<div class="toc-grid">` in `inhoud.html`. Place it in a logical order (group by category or chronologically).

```html
<a class="toc-card" href="recepten/categorie/bestandsnaam.html">
  <div class="card-placeholder">Foto volgt</div>
  <div class="card-body">
    <div class="card-category">Categorie</div>
    <div class="card-title">Receptnaam</div>
    <div class="card-desc">Korte beschrijving van het recept.</div>
  </div>
</a>
```

If a photo exists, replace the placeholder with:
```html
<img src="fotos/receptnaam.webp" alt="Receptnaam">
```

### Step 4: Add entry to inhoud.html toc-list

Add an entry in the `<div class="toc-list">` section of `inhoud.html`. Find the correct category block or create a new one.

**Add to existing category:**
```html
<a class="toc-list-entry" href="recepten/categorie/bestandsnaam.html"><span>Receptnaam</span><span class="pagenum">X</span></a>
```

**Create new category block:**
```html
<div class="toc-list-category">
  <h3>Categorienaam</h3>
  <a class="toc-list-entry" href="recepten/categorie/bestandsnaam.html"><span>Receptnaam</span><span class="pagenum">X</span></a>
</div>
```

### Step 5: Add entries to index-trefwoorden.html

Add index entries for the recipe name and each tag. Entries must be placed in **alphabetical order** within the `<div class="index-columns">`.

```html
<div class="index-entry">trefwoord<a href="recepten/categorie/bestandsnaam.html">X</a></div>
```

- `X` is the page number of the recipe.
- Add a new letter header if the letter doesn't exist yet:
  ```html
  <div class="index-letter">L</div>
  ```
- The recipe name itself should also appear as an index entry (capitalized as the recipe title).
- Tags are lowercase in the index.
- If a keyword already exists with a different recipe, add a NEW `index-entry` div for the same keyword with the new recipe link (do not merge into one entry).

### Step 6: Update recipe count in index.html

In `index.html`, update the count in:
```html
<p class="sub">X recepten</p>
```

Increment the number by 1.

### Step 7: Update prev/next navigation in adjacent recipes

The recipes are linked in a chain via `recipe-nav`. When adding a new recipe:

1. Determine where the new recipe falls in the chain (usually at the end).
2. Update the PREVIOUS last recipe to add a "Volgend" (next) link pointing to the new recipe.
3. The new recipe should have a "Vorig" (prev) link pointing to the previous recipe.

**Prev link format:**
```html
<a href="../categorie/vorig-recept.html"><span class="arrow">&lsaquo;</span><span>Vorig</span></a>
```

**Next link format:**
```html
<a href="../categorie/volgend-recept.html"><span>Volgend</span><span class="arrow">&rsaquo;</span></a>
```

**If no prev (first recipe):** use `<span class="spacer"></span>` instead.
**If no next (last recipe):** omit the next link entirely; if there IS a prev link, the spacer is not needed since `justify-content: space-between` handles layout.

### Step 8: Update or create chapter page

Check if `recepten/{categorie}/index.html` exists.

**If it exists:** Add the new recipe to the `<ul class="chapter-recipes">` list:
```html
<li><a href="bestandsnaam.html">Receptnaam</a></li>
```

**If it does not exist:** Create a new chapter page using the template below (see Chapter Page Template section).

---

## Workflow: Adding a Photo to a Recipe

Photos are stored in the `fotos/` directory at the project root.

### In the recipe page:

Replace:
```html
<div class="recipe-hero-placeholder">Foto volgt</div>
```

With:
```html
<img class="recipe-hero" src="../../fotos/receptnaam.webp" alt="Receptnaam">
```

### In inhoud.html (toc-card):

Replace:
```html
<div class="card-placeholder">Foto volgt</div>
```

With:
```html
<img src="fotos/receptnaam.webp" alt="Receptnaam">
```

Note the different relative paths: recipe pages use `../../fotos/` while inhoud.html uses `fotos/`.

---

## Workflow: Creating a Chapter/Category Page

Create `recepten/{categorie}/index.html` using this template:

### Chapter Page Template

```html
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CATEGORIENAAM — Mijn Kookboek</title>
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<nav class="site-nav"><div class="site-nav-inner">
<p class="brand">Mijn Kookboek</p>
<div>
  <a href="../../index.html">Omslag</a>
  <a href="../../inhoud.html">Inhoud</a>
  <a href="../../index-trefwoorden.html">Register</a>
</div>
</div></nav>
<div class="page chapter">
  <div class="chapter-number">Hoofdstuk ROMAN_NUMERAL</div>
  <h1>Categorienaam</h1>
  <p class="chapter-desc">Beschrijving van deze categorie.</p>
  <ul class="chapter-recipes">
    <li><a href="receptnaam.html">Receptnaam</a></li>
  </ul>
</div>
</body>
</html>
```

**Notes:**
- Chapter numbers use Roman numerals (I, II, III, IV, V, etc.).
- The chapter description should be a short, evocative sentence about the category.
- Recipe links in the chapter list are relative (just the filename, no directory prefix).

---

## CSS Class Reference

### Layout & Navigation
| Class | Description |
|-------|-------------|
| `.site-nav` | Dark sticky top navigation bar |
| `.site-nav-inner` | Flex container inside nav (max-width 1200px) |
| `.brand` | Serif brand name "Mijn Kookboek" in the nav |
| `.page` | Main page container (max-width 800px, white bg, padded) |

### Cover Page (index.html)
| Class | Description |
|-------|-------------|
| `.cover` | Full-viewport dark cover page |
| `.kicker` | Small uppercase text above the title ("persoonlijk kookboek") |
| `.divider` | Thin horizontal line between title and subtitle |
| `.sub` | Recipe count text below divider |

### Table of Contents (inhoud.html)
| Class | Description |
|-------|-------------|
| `.toc` | Table of contents page container (no max-width, soft bg) |
| `.toc-header` | Centered header with title and subtitle |
| `.toc-subtitle` | Small uppercase subtitle under "Inhoud" |
| `.toc-grid` | CSS grid for recipe cards (auto-fill, min 300px) |
| `.toc-card` | Clickable card with image and body |
| `.card-placeholder` | Grey placeholder when no photo exists |
| `.card-body` | Text area of the card |
| `.card-category` | Small uppercase category label on card |
| `.card-title` | Serif recipe title on card |
| `.card-desc` | Muted description text (2-line clamp) |
| `.toc-list` | Classic list-style table of contents (720px, bordered top) |
| `.toc-list-category` | Category group in the list |
| `.toc-list-entry` | Single recipe entry (flex, dotted border bottom) |
| `.pagenum` | Right-aligned page number in list entries |

### Recipe Pages
| Class | Description |
|-------|-------------|
| `.recipe` | Recipe page container (no padding, no max-width) |
| `.recipe-hero` | Full-width hero image (max-height 70vh) |
| `.recipe-hero-placeholder` | Grey placeholder when no hero photo (height 40vh) |
| `.recipe-nav` | Prev/next navigation overlaying bottom of hero |
| `.arrow` | Serif arrow character in nav links |
| `.spacer` | Flex spacer for alignment when prev or next is missing |
| `.recipe-content` | Centered content area (max-width 720px) |
| `.recipe-badge` | Black uppercase badge with category and number |
| `.subtitle` | Italic serif description below h1 |
| `.recipe-meta` | 4-column grid with recipe metadata |
| `.cell` | Single cell in the meta grid |
| `.label` | Tiny uppercase label in meta cell |
| `.value` | Large serif value in meta cell |
| `.recipe-body` | 2-column grid: ingredients (1fr) + steps (1.6fr) |
| `.section-label` | Uppercase label with bottom border (e.g., "Ingredienten", "Bereiding") |
| `.ingredients` | Unstyled list of ingredients |
| `.steps` | Container for numbered steps |
| `.step` | Single step (flex with number and text) |
| `.num` | Large serif step number (28px, light grey) |
| `.extras` | Section below recipe body (bordered top) |
| `.block` | Block within extras (Tips, Variaties, Bron) |
| `.recipe-footer` | Footer with tags and page number |
| `.tag` | Uppercase muted tag label |

### Chapter Pages
| Class | Description |
|-------|-------------|
| `.chapter` | Dark full-width chapter intro page |
| `.chapter-number` | Small uppercase chapter number (e.g., "Hoofdstuk III") |
| `.chapter-desc` | Muted description text |
| `.chapter-recipes` | Centered list of recipe links |

### Index/Register (index-trefwoorden.html)
| Class | Description |
|-------|-------------|
| `.index` | Register page container |
| `.index-columns` | Two-column layout for index entries |
| `.index-letter` | Large serif letter heading (bordered bottom) |
| `.index-entry` | Single keyword entry with linked page number |

---

## Important Reminders

- **Work directly on the main branch** for recipes -- no branches or PRs needed.
- All pages share `style.css` via relative paths. Never duplicate CSS into recipe files.
- The `<link rel="stylesheet">` href depends on depth: root pages use `style.css`, recipe pages use `../../style.css`.
- Similarly, nav links in recipe pages use `../../index.html` etc., while root pages use `index.html`.
- Always keep the register (`index-trefwoorden.html`) in strict alphabetical order.
- The recipe chain (prev/next nav) must be consistent -- every "Volgend" link must have a matching "Vorig" link on the target page.
