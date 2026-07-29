const { getDefaultConfig } = require("expo/metro-config");

const config = getDefaultConfig(__dirname);

config.resolver.blockList = [
  /android\/build\/.*/,
  /modules\/.*\/android\/build\/.*/,
];

module.exports = config;
