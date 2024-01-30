'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
const FasterRunner = process.env.FasterRunner ? process.env.FasterRunner : "Another FasterRunner"
const API_URL = process.env.VUE_APP_API_URL ? process.env.VUE_APP_API_URL : ""
console.log("API_URL: " + API_URL)
module.exports = merge(prodEnv, {
    NODE_ENV: '"development"',
    FasterRunner: "'" + FasterRunner + "'"
})
