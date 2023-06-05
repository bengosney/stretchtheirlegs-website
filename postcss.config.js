module.exports = {
  map: { inline: false },
  plugins: [
    require("pixrem")(),
    require("autoprefixer")(),
    require("postcss-preset-env")({ stage: 0 }),
    require("css-mqpacker")({ sort: true }),
    require("cssnano")({ zindex: false }),
  ],
};
