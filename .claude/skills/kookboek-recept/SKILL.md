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

"Foodnotes" is a personal cookbook website styled as an editorial magazine, inspired by **The Gourmand**. Built with **Eleventy (11ty)** static site generator and **Decap CMS** for visual editing.

- **Site:** GitHub Pages via GitHub Actions
- **CMS:** Decap CMS op Netlify (alleen auth, geen build)
- **Domein:** foodnotes.nl

### Project Structure

```
kookboek/
├── eleventy.config.js          — 11ty config (filters, collections, passthrough)
├── package.json                — npm project with 11ty dependency
├── netlify.toml                — Netlify config (alleen admin kopiëren, geen build)
├── fotos/                      — Recipe photos (.webp), served at /fotos/
├── src/
│   ├── index.njk               — Cover page (auto recipe count, klikbaar)
│   ├── inhoud.njk              — TOC (magazine grid + klassieke lijst)
│   ├── register.njk            — Auto keyword index vanuit tags
│   ├── chapters.njk            — Auto chapter pages vanuit categories.json
│   ├── style.css               — Shared stylesheet
│   ├── admin/                  — Decap CMS (passthrough, niet verwerkt door 11ty)
│   ├── _data/categories.json   — Categorieën (slug, title, order, roman, description)
│   ├── _includes/
│   │   ├── base.njk            — HTML shell + carousel JS + Netlify Identity
│   │   ├── recipe.njk          — Recept template
│   │   └── partials/nav.njk    — Navigatiebalk
│   └── recepten/
│       ├── recepten.json       — Directory data (layout + permalink)
│       └── *.md                — Recepten als Markdown met YAML frontmatter
└── _site/                      — Build output (gitignored)
```

---

## Recept toevoegen — Instructie

> Dit is de enige stap die nodig is. Al het andere (inhoud, register, navigatie, recepttelling, hoofdstukken) wordt automatisch gegenereerd.

### 1. Bepaal het volgnummer

Kijk welk hoogste `pageNumber` bestaat in `src/recepten/*.md` en gebruik het volgende getal.

### 2. Maak het bestand aan

Maak `src/recepten/{slug}.md` aan. Slug = lowercase, woorden gescheiden door `-`, geen accenten of spaties.

### 3. Vul het YAML frontmatter in

```yaml
---
title: "Naam van het gerecht"
subtitle: "Korte, sfeervolle beschrijving van het gerecht."
category: "vlees"
foto: ""
pageNumber: 7
order: 1

meta:
  - label: "Personen"
    value: "4"
  - label: "Voorber."
    value: "20 min"
  - label: "Bereiding"
    value: "45 min"
  - label: "Niveau"
    value: "gemiddeld"

ingredienten:
  - groep: "Hoofdgerecht"
    items:
      - "400 g ingredient"
      - "2 el olijfolie"
  - groep: "Saus"
    items:
      - "200 ml room"

stappen:
  - "**Voorbereiding:** Snijd de groenten in blokjes."
  - "Verhit olie in een pan op middelhoog vuur."
  - "**Afwerking:** Garneer met verse kruiden."

tips:
  - "Kan een dag van tevoren bereid worden."

variaties:
  - "Vervang de room door kokosmelk voor een vegan variant."

bron: "Ottolenghi, Simple"

extrafotos:
  - foto: "gerecht-stap1.webp"
    bijschrift: "De groenten na het snijden"
  - foto: "gerecht-resultaat.webp"
    bijschrift: "Het eindresultaat"

tags:
  - "stoofpot"
  - "winter"
  - "italiaans"
---
```

### 4. Foto toevoegen (optioneel)

- **Hero foto:** Kopieer naar `fotos/{slug}.jpg` en zet `foto: "{slug}.jpg"`
- **Extra foto's:** Kopieer naar `fotos/` en voeg toe aan `extrafotos` array
- **Pexels API** (gratis foto's): Gebruik de API key `aMq3g2BlsaWaTYEPsK9UKpBaH89dJkAzZE3OQHWATS5QQgWU8QRs6vqF` om foto's te zoeken en downloaden:
  ```bash
  # Zoeken
  curl -s -H "Authorization: API_KEY" "https://api.pexels.com/v1/search?query=ZOEKTERM&per_page=3&orientation=landscape"
  # Downloaden (gebruik w=800 voor goede kwaliteit)
  curl -sL "https://images.pexels.com/photos/ID/pexels-photo-ID.jpeg?auto=compress&cs=tinysrgb&w=800" -o fotos/slug.jpg
  ```

### Klaar!

Commit naar main → GitHub Actions bouwt automatisch → site is live.

> **Register:** Het register (trefwoordenindex op ingrediënt) wordt automatisch gegenereerd uit de `ingredienten` van elk recept. Er hoeft niets handmatig bijgewerkt te worden — elk nieuw recept verschijnt automatisch in het register.

---

## Veldverklaring

| Veld | Verplicht | Beschrijving |
|------|-----------|--------------|
| `title` | ✅ | Naam van het gerecht |
| `subtitle` | ✅ | Korte beschrijving (cursief onder titel) |
| `category` | ✅ | Slug uit categories.json: `vlees`, `groentes`, `fermenteren` |
| `foto` | ❌ | Bestandsnaam in `fotos/` voor hero image, `""` voor placeholder |
| `pageNumber` | ✅ | Uniek volgnummer, bepaalt globale sortering en prev/next |
| `order` | ✅ | Volgnummer binnen categorie, getoond in badge (Categorie / 001) |
| `meta` | ✅ | Array van `{label, value}` paren (meestal 4) |
| `ingredienten` | ✅ | Array van groepen met `groep` (naam of `""`) en `items` array |
| `stappen` | ✅ | Array van strings, `**vet**` wordt `<strong>` |
| `tips` | ❌ | Array van strings |
| `variaties` | ❌ | Array van strings |
| `bron` | ❌ | Bronvermelding als string |
| `extrafotos` | ❌ | Array van `{foto, bijschrift}` — wordt carousel bij 2+ foto's |
| `tags` | ✅ | Array van lowercase keywords voor het register |

### Meta labels

Gebruik consistente labels. Veelgebruikt:

| Label | Wanneer |
|-------|---------|
| `Personen` | Standaard voor de meeste gerechten |
| `Opbrengst` | Voor fermentatie, sauzen, confituren (bijv. "±2 kg") |
| `Voorber.` | Voorbereidingstijd |
| `Bereiding` | Actieve kooktijd |
| `Ferment.` | Fermentatietijd (bijv. "3-5 dagen") |
| `Niveau` | makkelijk / gemiddeld / gevorderd |

### Categorieën

Huidige categorieën in `src/_data/categories.json`:

| Slug | Titel |
|------|-------|
| `vlees` | Vlees |
| `groentes` | Groentes |
| `fermenteren` | Fermenteren |
| `sauzen` | Sauzen |
| `desserts` | Desserts |
| `technieken` | Technieken |
| `vis` | Vis |
| `brood` | Brood |
| `overig` | Overig |
| `patisserie` | Patisserie |

Nieuwe categorie toevoegen: voeg toe aan `categories.json` + `src/admin/config.yml` select widget.

---

## Naamconventies

- **Bestandsnaam:** lowercase, `-` gescheiden: `ossobuco-alla-milanese.md`
- **Foto's:** `fotos/{slug}.webp` (of `.jpg`)
- **Geen** spaties, accenten of speciale tekens in bestandsnamen
- **Tags:** lowercase, Nederlands of Engelstalig

---

## Wat is automatisch?

| Feature | Automatisch |
|---------|-------------|
| Receptpagina op `/recepten/{category}/{slug}/` | ✅ |
| Prev/next navigatie | ✅ (op basis van pageNumber) |
| Badge (Categorie / 003) | ✅ |
| Recepttelling op cover | ✅ |
| Inhoudsopgave (grid + lijst) | ✅ |
| Trefwoordenregister | ✅ (uit title + tags) |
| Hoofdstukpagina per categorie | ✅ |
| Foto carousel bij 2+ extrafotos | ✅ |

---

## Belangrijk

- **Werk direct op main branch** — geen branches of PR's nodig voor recepten.
- **pageNumber** moet uniek zijn — check bestaande recepten.
- **Foto's** gaan in root `fotos/` map (niet `src/fotos/`).
- **Body van .md is leeg** — alle data zit in YAML frontmatter.
- **Build output** (`_site/`) staat in `.gitignore`.
- **pathPrefix** is conditioneel: `/kookboek/` voor GitHub Pages, `/` voor Netlify. Gebruik altijd `| url` filter in templates voor paden.
