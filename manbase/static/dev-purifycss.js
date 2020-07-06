const purify = require("purify-css");

let content = ["./js/*.js", "../templates/*.html"];
let css = ["./*.css"];
let options = {
    output: "./out.css",
    minify: true,
    info: true,
};

purify(content, css, options);