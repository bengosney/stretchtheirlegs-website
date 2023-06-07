module.exports = {
  map: { inline: false },
  plugins: [
    require("pixrem")(),
    require("autoprefixer")(),
    require("postcss-preset-env")({ stage: 0 }),
    require("css-mqpacker")({ sort: true }),
    require("cssnano")({ zindex: false }),
    require("@fullhuman/postcss-purgecss")({
      content: ["./**/*.html"],
      safelist: [/^nav-level-\d$/, /^level-\d$/, /^block-/, /^field-/],
      skippedContentGlobs: ["node_modules/**", ".direnv/**"],
    }),
  ],
};
