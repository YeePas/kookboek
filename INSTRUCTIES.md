# Mijn Kookboek — Instructies

## Mapstructuur

```
kookboek/
├── index.html                  ← Omslag / titelpagina
├── inhoud.html                 ← Inhoudsopgave
├── index-trefwoorden.html      ← Trefwoordenregister
├── style.css                   ← Gedeelde styling
├── INSTRUCTIES.md              ← Dit bestand
└── recepten/
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

Je kunt nieuwe categorieën toevoegen door simpelweg een nieuwe map aan te maken.

## Naamconventies

- Bestandsnamen in **kleine letters**, woorden gescheiden met **streepjes**: `ossobuco-alla-milanese.html`
- Geen spaties, accenten of speciale tekens in bestandsnamen
- Mapmamen ook in kleine letters: `recepten/vlees/`

## Nieuw recept toevoegen

### 1. Maak het HTML-bestand

Maak een nieuw bestand aan in de juiste categoriemap, bijvoorbeeld `recepten/vis/gamba-al-ajillo.html`. Gebruik dit template:

```html
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>RECEPTNAAM — Mijn Kookboek</title>
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<nav class="site-nav"><div class="site-nav-inner">
<p class="brand">MIJN KOOKBOEK</p>
<div>
  <a href="../../index.html">Omslag</a>
  <a href="../../inhoud.html">Inhoud</a>
  <a href="../../index-trefwoorden.html">Register</a>
</div>
</div></nav>
<div class="page recipe">
  <div class="recipe-badge">CATEGORIE / NR</div>
  <h1>RECEPTNAAM</h1>
  <p class="subtitle">Korte beschrijving van het recept.</p>
  <div class="recipe-photo-placeholder">FOTO ONTBREEKT</div>
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
</body>
</html>
```

### 2. Voeg het recept toe aan de inhoudsopgave

Open `inhoud.html` en voeg een regel toe onder de juiste categorie:

```html
<a class="toc-entry" href="recepten/categorie/bestandsnaam.html">
  <span>Receptnaam</span><span class="pagenum">X</span>
</a>
```

Als de categorie nog niet bestaat, voeg een nieuw blok toe:

```html
<div class="toc-category">
  <h2>Nieuwe Categorie</h2>
  <a class="toc-entry" href="recepten/categorie/bestandsnaam.html">
    <span>Receptnaam</span><span class="pagenum">X</span>
  </a>
</div>
```

### 3. Werk het trefwoordenregister bij

Open `index-trefwoorden.html` en voeg trefwoorden toe op de juiste alfabetische plek:

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
<p class="sub">2 recepten</p>
```

## Foto toevoegen

Vervang de placeholder in een recept:

```html
<!-- Verwijder deze regel: -->
<div class="recipe-photo-placeholder">FOTO ONTBREEKT</div>

<!-- Vervang door: -->
<img class="recipe-photo" src="../../fotos/bestandsnaam.jpg" alt="Receptnaam">
```

Sla foto's op in een `fotos/` map in de root van het project.

## Styling aanpassen

Alle styling staat centraal in `style.css`. Wijzigingen daar gelden automatisch voor alle pagina's.
