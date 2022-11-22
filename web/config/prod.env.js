"use strict";
const FasterRunner = process.env.FasterRunner ? process.env.FasterRunner : "彩贝壳";
module.exports = {
  NODE_ENV: '"production"',
  FasterRunner: "'" + FasterRunner + "'"
};
