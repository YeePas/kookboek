module.exports = function(eleventyConfig) {

  // --- Passthrough copy ---
  eleventyConfig.addPassthroughCopy("src/style.css");
  eleventyConfig.addPassthroughCopy("src/admin");
  eleventyConfig.addPassthroughCopy("src/CNAME");
  eleventyConfig.addPassthroughCopy({ "fotos": "fotos" });

  // --- Collections ---
  eleventyConfig.addCollection("recepten", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/recepten/*.md")
      .sort((a, b) => a.data.pageNumber - b.data.pageNumber);
  });

  // --- Filters ---

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
    return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
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
    return Object.values(groups).sort((a, b) => a.order - b.order);
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
        recipes: entries[term].sort((a, b) => a.data.pageNumber - b.data.pageNumber)
      });
    }
    return result;
  });

  // Get previous recipe in sorted order
  eleventyConfig.addFilter("prevRecipe", function(currentPage) {
    const all = this.ctx.collections.recepten;
    const idx = all.findIndex(r => r.inputPath === currentPage.inputPath);
    return idx > 0 ? all[idx - 1] : null;
  });

  // Get next recipe in sorted order
  eleventyConfig.addFilter("nextRecipe", function(currentPage) {
    const all = this.ctx.collections.recepten;
    const idx = all.findIndex(r => r.inputPath === currentPage.inputPath);
    return idx >= 0 && idx < all.length - 1 ? all[idx + 1] : null;
  });

  // Get sorted categories as array (already sorted, just return copy)
  eleventyConfig.addFilter("sortedCategories", function(cats) {
    return [...cats].sort((a, b) => a.order - b.order);
  });

  // Filter recipes by category
  eleventyConfig.addFilter("byCategory", function(recipes, cat) {
    return recipes.filter(r => r.data.category === cat);
  });

  // Build ingredient index from recipe collection
  eleventyConfig.addFilter("buildIngredientIndex", function(recipes) {
    const UNITS = /^(g|gr|kg|ml|l|dl|cl|el|tl|eetlepels?|theelepels?|stuks?|st|snuf|scheut(?:je)?|bos(?:je)?|takje(?:s)?|plak(?:ken|jes?)?|blad(?:je|eren)?|teen|tenen|cm|mm|druppels?|blik(?:ken|je)?|potje|zakje|pak|klontje|handvol|mespuntje)\.?\s+/i;

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
        recipes: entries[key].recipes.sort((a, b) => a.data.pageNumber - b.data.pageNumber)
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
