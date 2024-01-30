'use strict'
const FasterRunner = process.env.FasterRunner ? process.env.FasterRunner : "Another FasterRunner"
const API_URL = process.env.API_URL ? process.env.API_URL : ""
console.log('process args: ' + process.argv)
console.log('get env from env API_URL: ' + API_URL)
module.exports = {
    NODE_ENV: '"production"',
    FasterRunner: "'" + FasterRunner + "'",
    API_URL: "'" + API_URL + "'",
}
