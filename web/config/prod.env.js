'use strict'
const FasterRunner = process.env.FasterRunner ? process.env.FasterRunner : "Another FasterRunner"
module.exports = {
    NODE_ENV: '"production"',
    FasterRunner: "'" + FasterRunner + "'"
}
