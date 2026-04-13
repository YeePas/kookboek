# Mijn Kookboek — Instructies

## Mapstructuur

```
kookboek/
├── index.html                  ← Omslag / titelpagina
├── inhoud.html                 ← Inhoudsopgave (magazine grid)
├── index-trefwoorden.html      ← Trefwoordenregister (twee kolommen)
├── style.css                   ← Gedeelde styling (editorial magazine-stijl)
├── INSTRUCTIES.md              ← Dit bestand
├── fotos/                      ← Receptfoto's
│   └── kimchi.webp
└── recepten/
    ├── fermenteren/
    │   └── kimchi.html
    ├── groentes/
    │   └── spitskool-sichuan.html
    └── vlees/
        └── ossobuco-alla-milanese.html
```

Recepten worden opgeslagen in submappen per categorie onder `recepten/`. Mogelijke categorieën:

| Map | Categorie |
|-----|-----------|
| `recepten/vlees/` | Vlees |
| `recepten/vis/` | Vis & zeevruchten |
| `recepten/vegetarisch/` | Vegetarisch |
| `recepten/soepen/` | Soepen |
| `recepten/bijgerechten/` | Bijgerechten |
| `recepten/desserts/` | Desserts |
| `recepten/bakken/` | Bakken |
| `recepten/fermenteren/` | Fermenteren |
| `recepten/groentes/` | Groentes |

Je kunt nieuwe categorieën toevoegen door simpelweg een nieuwe map aan te maken.

## Design

Het kookboek gebruikt een editorial magazine-stijl geïnspireerd door The Gourmand:

- **Typografie**: Instrument Serif (Google Fonts) voor koppen, systeem sans-serif voor bodytekst
- **Kleuren**: Zwart/wit met subtiel grijs (#F2F1EE achtergrond)
- **Navigatie**: Donkere topbalk met serif-logo
- **Omslag**: Full-viewport, donkere achtergrond, grote serif-titel
- **Inhoud**: Magazine-grid met receptkaarten (foto, categorie, titel, beschrijving)
- **Recepten**: Full-width hero-foto bovenaan, content gecentreerd in 720px container
- **Register**: Twee-koloms layout met grote serif-letters

## Naamconventies

- Bestandsnamen in **kleine letters**, woorden gescheiden met **streepjes**: `ossobuco-alla-milanese.html`
- Geen spaties, accenten of speciale tekens in bestandsnamen
- Mapmamen ook in kleine letters: `recepten/vlees/`
- Foto's: `fotos/receptnaam.webp` (of .jpg)

## Nieuw recept toevoegen

### 1. Maak het HTML-bestand

Maak een nieuw bestand aan in de juiste categoriemap, bijvoorbeeld `recepten/vis/gamba-al-ajillo.html`. Gebruik dit template:

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
  <!-- Of met foto: <img class="recipe-hero" src="../../fotos/receptnaam.webp" alt="Receptnaam"> -->
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
        <div class="section-label">Ingrediënten</div>
        <ul class="ingredients">
          <li>Ingrediënt 1</li>
          <li>Ingrediënt 2</li>
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
      <div>pagina X / Y</div>
    </div>
  </div>
</div>
</body>
</html>
```

### 2. Voeg het recept toe aan de inhoudsopgave

Open `inhoud.html` en voeg een kaart toe in de `toc-grid`:

```html
<a class="toc-card" href="recepten/categorie/bestandsnaam.html">
  <div class="card-placeholder">Foto volgt</div>
  <!-- Of met foto: <img src="fotos/receptnaam.webp" alt="Receptnaam"> -->
  <div class="card-body">
    <div class="card-category">Categorie</div>
    <div class="card-title">Receptnaam</div>
    <div class="card-desc">Korte beschrijving.</div>
  </div>
</a>
```

### 3. Werk het trefwoordenregister bij

Open `index-trefwoorden.html` en voeg trefwoorden toe op de juiste alfabetische plek in de `index-columns` div:

```html
<div class="index-entry">trefwoord<a href="recepten/categorie/bestandsnaam.html">X</a></div>
```

Voeg een nieuwe letter-header toe als die nog niet bestaat:

```html
<div class="index-letter">G</div>
```

### 4. Werk het receptentotaal bij op de omslag

Open `index.html` en pas het aantal recepten aan:

```html
<p class="sub">4 recepten</p>
```

## Foto toevoegen

Sla foto's op in de `fotos/` map in de root van het project.

### In een recept:

Vervang de hero-placeholder:

```html
<!-- Verwijder deze regel: -->
<div class="recipe-hero-placeholder">Foto volgt</div>

<!-- Vervang door: -->
<img class="recipe-hero" src="../../fotos/receptnaam.webp" alt="Receptnaam">
```

### In de inhoudsopgave:

Vervang de card-placeholder:

```html
<!-- Verwijder: -->
<div class="card-placeholder">Foto volgt</div>

<!-- Vervang door: -->
<img src="fotos/receptnaam.webp" alt="Receptnaam">
```

## Styling aanpassen

Alle styling staat centraal in `style.css`. Wijzigingen daar gelden automatisch voor alle pagina's. De stijl gebruikt Google Fonts (Instrument Serif) die via `@import` wordt geladen.
