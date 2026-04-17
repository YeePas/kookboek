const categoriesData = require("./src/_data/categories.json");
const Image = require("@11ty/eleventy-img");
const BOOK_PAGE_OFFSET = 2;
const byCategoryCache = new WeakMap();

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeLocalImageSource(src) {
  if (!src) return "";
  const input = String(src).trim();
  if (/^https?:\/\//i.test(input)) return input;

  const withoutLeadingSlash = input.replace(/^\//, "");
  if (withoutLeadingSlash.startsWith("fotos/")) {
    return `./${withoutLeadingSlash}`;
  }

  return input.startsWith("./") ? input : `./${input}`;
}

function getCategoryOrder(categories, slug) {
  const cat = categories.find(c => c.slug === slug);
  return cat ? Number(cat.order) : 999;
}

function compareRecipesByBookOrder(a, b, categories) {
  const categoryDiff = getCategoryOrder(categories, a.data.category) - getCategoryOrder(categories, b.data.category);
  if (categoryDiff !== 0) return categoryDiff;

  const orderA = Number(a.data.order || 9999);
  const orderB = Number(b.data.order || 9999);
  if (orderA !== orderB) return orderA - orderB;

  return String(a.data.title || "").localeCompare(String(b.data.title || ""), "nl");
}

function sortRecipesForBook(recipes, categories) {
  return [...recipes].sort((a, b) => compareRecipesByBookOrder(a, b, categories));
}

function recipeNumberInBook(recipes, recipe) {
  const idx = recipes.findIndex(r => r.inputPath === recipe.inputPath);
  return idx >= 0 ? idx + 1 + BOOK_PAGE_OFFSET : null;
}

module.exports = function(eleventyConfig) {

  // Build-time asset version for cache busting (same value within one build)
  eleventyConfig.addGlobalData("assetVersion", Date.now());

  // --- Passthrough copy ---
  eleventyConfig.addPassthroughCopy("src/style.css");
  eleventyConfig.addPassthroughCopy("src/site.js");
  eleventyConfig.addPassthroughCopy("src/admin");
  eleventyConfig.addPassthroughCopy("src/CNAME");
  eleventyConfig.addPassthroughCopy({ "fotos": "fotos" });

  // --- Collections ---
  eleventyConfig.addCollection("recepten", function(collectionApi) {
    const recipes = collectionApi.getFilteredByGlob("src/recepten/*.md");
    return sortRecipesForBook(recipes, categoriesData);
  });

  // --- Filters ---

  eleventyConfig.addNunjucksAsyncShortcode(
    "responsiveImage",
    async function (src, alt = "", sizes = "100vw", className = "", widths = "480,960,1440", loading = "lazy") {
      if (!src) return "";

      const parsedWidths = String(widths)
        .split(",")
        .map((w) => parseInt(w.trim(), 10))
        .filter((w) => Number.isFinite(w) && w > 0);

      const finalWidths = parsedWidths.length ? parsedWidths : [480, 960, 1440];

      try {
        const metadata = await Image(normalizeLocalImageSource(src), {
          widths: finalWidths,
          formats: ["avif", "webp", "jpeg"],
          urlPath: "/img/",
          outputDir: "./_site/img/",
          filenameFormat: (id, imageSrc, width, format) => {
            const baseName = imageSrc.split("/").pop().split(".")[0];
            return `${baseName}-${width}w.${format}`;
          },
        });

        const imageAttributes = {
          alt,
          sizes,
          loading,
          decoding: "async",
          class: className || undefined,
        };

        return Image.generateHTML(metadata, imageAttributes, { whitespaceMode: "inline" });
      } catch (error) {
        const cls = className ? ` class=\"${escapeHtml(className)}\"` : "";
        return `<img src=\"${escapeHtml(src)}\" alt=\"${escapeHtml(alt)}\" loading=\"${escapeHtml(loading)}\" decoding=\"async\"${cls}>`;
      }
    }
  );

  // Zero-pad numbers: {{ 5 | pad(3) }} → "005"
  eleventyConfig.addFilter("pad", (num, width) => {
    return String(num).padStart(width, '0');
  });

  // Category display title from slug
  eleventyConfig.addFilter("categoryTitle", function(slug) {
    const cats = this.ctx.categories;
    if (!cats) return slug;
    const cat = cats.find(c => c.slug === slug);
    return cat ? cat.title : slug;
  });

  // Inline markdown: convert **bold** to <strong>bold</strong>
  eleventyConfig.addFilter("mdInline", (text) => {
    if (!text) return "";
    const escaped = String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");

    return escaped.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  });

  // Normalize CMS image paths so both "kimchi.webp" and "/fotos/kimchi.webp" work.
  eleventyConfig.addFilter("cmsImagePath", (value) => {
    if (!value) return "";
    return String(value).replace(/^\/?fotos\//, "");
  });

  // Group recipes by category, sorted by category order
  eleventyConfig.addFilter("groupByCategory", function(recipes) {
    const cats = this.ctx.categories;
    const groups = {};
    for (const recipe of recipes) {
      const catSlug = recipe.data.category;
      const catData = cats ? cats.find(c => c.slug === catSlug) : null;
      if (!groups[catSlug]) groups[catSlug] = { slug: catSlug, title: catData?.title || catSlug, order: catData?.order || 99, recipes: [] };
      groups[catSlug].recipes.push(recipe);
    }
    const sortedGroups = Object.values(groups).sort((a, b) => a.order - b.order);
    return sortedGroups.map(group => ({
      ...group,
      recipes: [...group.recipes].sort((a, b) => Number(a.data.order || 9999) - Number(b.data.order || 9999))
    }));
  });

  // Global recipe number in book order (1..N)
  eleventyConfig.addFilter("recipeNumber", function(recipe) {
    if (!this.ctx._recipeNumberMap) {
      const all = this.ctx.collections.recepten || [];
      const map = new Map();
      all.forEach((r, idx) => map.set(r.inputPath, idx + 1 + BOOK_PAGE_OFFSET));
      this.ctx._recipeNumberMap = map;
    }

    return this.ctx._recipeNumberMap.get(recipe.inputPath) || null;
  });

  // Build keyword index from recipe collection
  eleventyConfig.addFilter("buildKeywordIndex", function(recipes) {
    const entries = {};
    for (const recipe of recipes) {
      const d = recipe.data;
      // Add recipe title as keyword
      addEntry(entries, d.title, recipe);
      // Add all tags
      if (d.tags) {
        for (const tag of d.tags) {
          addEntry(entries, tag, recipe);
        }
      }
    }
    // Sort and group by first letter
    const sorted = Object.keys(entries).sort((a, b) => a.localeCompare(b, 'nl'));
    const result = [];
    let currentLetter = null;
    for (const term of sorted) {
      const letter = term.charAt(0).toUpperCase();
      if (letter !== currentLetter) {
        currentLetter = letter;
        result.push({ letter, entries: [] });
      }
      result[result.length - 1].entries.push({
        term,
        recipes: sortRecipesForBook(entries[term], this.ctx.categories || categoriesData)
      });
    }
    return result;
  });

  // Get previous recipe in sorted order
  eleventyConfig.addFilter("prevRecipe", function(currentPage) {
    const all = this.ctx.collections.recepten;
    const current = all.find(r => r.inputPath === currentPage.inputPath);
    if (!current) return null;
    const inCategory = all.filter(r => r.data.category === current.data.category);
    const idx = inCategory.findIndex(r => r.inputPath === currentPage.inputPath);
    return idx > 0 ? inCategory[idx - 1] : null;
  });

  // Get next recipe in sorted order
  eleventyConfig.addFilter("nextRecipe", function(currentPage) {
    const all = this.ctx.collections.recepten;
    const current = all.find(r => r.inputPath === currentPage.inputPath);
    if (!current) return null;
    const inCategory = all.filter(r => r.data.category === current.data.category);
    const idx = inCategory.findIndex(r => r.inputPath === currentPage.inputPath);
    return idx >= 0 && idx < inCategory.length - 1 ? inCategory[idx + 1] : null;
  });

  // Get sorted categories as array (already sorted, just return copy)
  eleventyConfig.addFilter("sortedCategories", function(cats) {
    return [...cats].sort((a, b) => a.order - b.order);
  });

  // Filter recipes by category
  eleventyConfig.addFilter("byCategory", function(recipes, cat) {
    let grouped = byCategoryCache.get(recipes);
    if (!grouped) {
      grouped = new Map();
      for (const recipe of recipes) {
        const key = recipe.data.category;
        if (!grouped.has(key)) grouped.set(key, []);
        grouped.get(key).push(recipe);
      }
      byCategoryCache.set(recipes, grouped);
    }

    return grouped.get(cat) || [];
  });

  // Build ingredient index from recipe collection
  eleventyConfig.addFilter("buildIngredientIndex", function(recipes) {
    const UNITS = /^(g|gr|kg|ml|l|dl|cl|el|tl|eetlepels?|theelepels?|stuks?|st|snuf|scheut(?:je)?|bos(?:je)?|takje(?:s)?|plak(?:ken|jes?)?|blad(?:je|eren)?|teen|tenen|cm|mm|druppels?|blik(?:ken|je)?|potje|zakje|pak|klontje|handvol|mespuntje)\.?\s+/i;
    const EXCLUDED_INGREDIENTS = new Set(["peper en zout", "zout en peper"]);

    function extractIngredient(raw) {
      let s = raw.trim();
      // Remove leading qualifiers
      s = s.replace(/^(max\.?|ca\.?|evt\.?|circa|ongeveer|eventueel)\s*/i, '');
      // Remove leading numbers, fractions, ranges
      s = s.replace(/^[\d.,½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞\s/+–-]+/, '');
      // Remove unit word
      s = s.replace(UNITS, '');
      // Clean up leading punctuation
      s = s.replace(/^[\s,.:]+/, '').trim();
      // Remove parenthetical notes
      s = s.replace(/\s*\(.*?\)/g, '').trim();
      // Remove trailing qualifiers
      s = s.replace(/\s*(naar smaak|indien nodig|optioneel|naar wens|of meer)$/i, '').trim();
      // Take first part before comma
      const ci = s.indexOf(',');
      if (ci > 0) s = s.substring(0, ci).trim();
      if (s.length < 2) return null;
      return s.charAt(0).toUpperCase() + s.slice(1);
    }

    const entries = {};
    for (const recipe of recipes) {
      if (!recipe.data.ingredienten) continue;
      for (const group of recipe.data.ingredienten) {
        if (!group.items) continue;
        for (const item of group.items) {
          const ingredient = extractIngredient(item);
          if (!ingredient) continue;
          const key = ingredient.toLowerCase();
          if (EXCLUDED_INGREDIENTS.has(key)) continue;
          if (!entries[key]) entries[key] = { term: ingredient, recipes: [] };
          if (!entries[key].recipes.find(r => r.inputPath === recipe.inputPath)) {
            entries[key].recipes.push(recipe);
          }
        }
      }
    }

    const sorted = Object.keys(entries).sort((a, b) => a.localeCompare(b, 'nl'));
    const result = [];
    let currentLetter = null;
    for (const key of sorted) {
      const letter = key.charAt(0).toUpperCase();
      if (letter !== currentLetter) {
        currentLetter = letter;
        result.push({ letter, entries: [] });
      }
      result[result.length - 1].entries.push({
        term: entries[key].term,
        recipes: sortRecipesForBook(entries[key].recipes, this.ctx.categories || categoriesData)
      });
    }
    return result;
  });

  // Exclude admin from template processing (passthrough only)
  eleventyConfig.ignores.add("src/admin/**");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    pathPrefix: process.env.PATH_PREFIX || "/",
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};

function addEntry(entries, term, recipe) {
  if (!entries[term]) entries[term] = [];
  // Avoid duplicates
  if (!entries[term].find(r => r.inputPath === recipe.inputPath)) {
    entries[term].push(recipe);
  }
}
