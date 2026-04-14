const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const RECIPES_DIR = path.join(ROOT, "src", "recepten");
const PHOTOS_DIR = path.join(ROOT, "fotos");
const CATEGORIES_PATH = path.join(ROOT, "src", "_data", "categories.json");

function readFileSafe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch (error) {
    return null;
  }
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?/);
  return match ? match[1] : null;
}

function getScalar(frontmatter, fieldName) {
  const regex = new RegExp(`^${fieldName}:\\s*(.+)$`, "m");
  const match = frontmatter.match(regex);
  if (!match) return null;

  let value = match[1].trim();
  if ((value.startsWith("\"") && value.endsWith("\"")) || (value.startsWith("'") && value.endsWith("'"))) {
    value = value.slice(1, -1);
  }
  return value;
}

function getSection(frontmatter, sectionName) {
  const lines = frontmatter.split("\n");
  const startIndex = lines.findIndex((line) => line.trim() === `${sectionName}:`);
  if (startIndex < 0) return [];

  const sectionLines = [];
  for (let i = startIndex + 1; i < lines.length; i++) {
    const line = lines[i];
    const isTopLevel = /^\S/.test(line);
    if (isTopLevel) break;
    sectionLines.push(line);
  }

  return sectionLines;
}

function getExtraPhotoPaths(frontmatter) {
  const section = getSection(frontmatter, "extrafotos");
  const result = [];
  for (const line of section) {
    const match = line.match(/^\s*-?\s*foto:\s*(.+)\s*$/);
    if (!match) continue;
    let value = match[1].trim();
    if ((value.startsWith("\"") && value.endsWith("\"")) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (value) result.push(value.replace(/^\/?fotos\//, ""));
  }
  return result;
}

function hasListEntries(frontmatter, fieldName) {
  const section = getSection(frontmatter, fieldName);
  return section.some((line) => /^\s*-\s+/.test(line));
}

function main() {
  const errors = [];
  const warnings = [];

  const categoriesRaw = readFileSafe(CATEGORIES_PATH);
  const allowedCategories = new Set();
  if (categoriesRaw) {
    try {
      const categories = JSON.parse(categoriesRaw);
      for (const category of categories) {
        if (category && category.slug) allowedCategories.add(String(category.slug));
      }
    } catch (error) {
      errors.push(`Kan categories.json niet parsen: ${error.message}`);
    }
  } else {
    warnings.push("categories.json ontbreekt; categorie-validatie is overgeslagen.");
  }

  const files = fs
    .readdirSync(RECIPES_DIR)
    .filter((file) => file.endsWith(".md") && file !== "recepten.json")
    .sort();

  const pageNumbers = new Map();

  for (const fileName of files) {
    const fullPath = path.join(RECIPES_DIR, fileName);
    const content = readFileSafe(fullPath);
    const relative = path.join("src", "recepten", fileName);

    if (content == null) {
      errors.push(`${relative}: bestand kon niet gelezen worden.`);
      continue;
    }

    const frontmatter = parseFrontmatter(content);
    if (!frontmatter) {
      errors.push(`${relative}: mist geldige frontmatter met --- delimiters.`);
      continue;
    }

    const requiredScalars = ["title", "subtitle", "category", "pageNumber", "order"];
    for (const field of requiredScalars) {
      const value = getScalar(frontmatter, field);
      if (!value) {
        errors.push(`${relative}: verplicht veld '${field}' ontbreekt of is leeg.`);
      }
    }

    const pageNumber = getScalar(frontmatter, "pageNumber");
    if (pageNumber) {
      if (!/^\d+$/.test(pageNumber)) {
        errors.push(`${relative}: pageNumber moet een geheel getal zijn.`);
      } else {
        if (!pageNumbers.has(pageNumber)) pageNumbers.set(pageNumber, []);
        pageNumbers.get(pageNumber).push(relative);
      }
    }

    const category = getScalar(frontmatter, "category");
    if (category && allowedCategories.size > 0 && !allowedCategories.has(category)) {
      errors.push(`${relative}: category '${category}' bestaat niet in categories.json.`);
    }

    if (!hasListEntries(frontmatter, "meta")) {
      errors.push(`${relative}: meta lijst ontbreekt of bevat geen items.`);
    }
    if (!hasListEntries(frontmatter, "ingredienten")) {
      errors.push(`${relative}: ingredienten lijst ontbreekt of bevat geen items.`);
    }
    if (!hasListEntries(frontmatter, "stappen")) {
      errors.push(`${relative}: stappen lijst ontbreekt of bevat geen items.`);
    }
    if (!hasListEntries(frontmatter, "tags")) {
      errors.push(`${relative}: tags lijst ontbreekt of bevat geen items.`);
    }

    const heroPhoto = getScalar(frontmatter, "foto");
    if (heroPhoto) {
      const normalized = heroPhoto.replace(/^\/?fotos\//, "");
      const photoPath = path.join(PHOTOS_DIR, normalized);
      if (!fs.existsSync(photoPath)) {
        errors.push(`${relative}: hero foto '${heroPhoto}' bestaat niet in fotos/.`);
      }
    }

    const extraPhotos = getExtraPhotoPaths(frontmatter);
    for (const photo of extraPhotos) {
      const photoPath = path.join(PHOTOS_DIR, photo);
      if (!fs.existsSync(photoPath)) {
        errors.push(`${relative}: extrafoto '${photo}' bestaat niet in fotos/.`);
      }
    }
  }

  for (const [pageNumber, refs] of pageNumbers.entries()) {
    if (refs.length > 1) {
      errors.push(`Dubbele pageNumber '${pageNumber}' gevonden in: ${refs.join(", ")}`);
    }
  }

  if (warnings.length > 0) {
    console.log("\nWaarschuwingen:");
    for (const warning of warnings) console.log(`- ${warning}`);
  }

  if (errors.length > 0) {
    console.error("\nContent validatie gefaald:\n");
    for (const error of errors) console.error(`- ${error}`);
    process.exit(1);
  }

  console.log(`Content validatie geslaagd (${files.length} recepten gecontroleerd).`);
}

main();