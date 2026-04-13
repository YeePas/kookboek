module.exports = function(eleventyConfig) {

  // --- Passthrough copy ---
  eleventyConfig.addPassthroughCopy("src/style.css");
  eleventyConfig.addPassthroughCopy("src/admin");
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
