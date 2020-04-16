///Code credit: https://github.com/SethPoulsen/sql-teaching/blob/master/extractSubmissions.js
"use strict";
const fs = require("fs-extra");
const JSONStream = require('JSONStream');

// const semester = "su19";
const semester = "fa19";
const file = "./data/cs411/" + semester + "/submissions.json";
const variantsFile = "./data/cs411/" + semester + "/variants.json";

let variantToQuestion = {};
let variants = JSON.parse(fs.readFileSync(variantsFile));
for (let i = 0; i < variants.length; ++i) {
    let variant = variants[i];
    variantToQuestion[variant["id"]] = variant["question_id"];
}

let sorted = {};
const jsonstream = JSONStream.parse("*");
jsonstream.on('close', () => {
    console.log("done");

    for (let key in sorted) {
        let dir = "./submissions/" + key;
        if (!fs.existsSync(dir)){
            fs.mkdirSync(dir);
        }

        for (let innerKey in sorted[key]) {
            fs.writeFileSync(dir + "/" + innerKey + ".sql", sorted[key][innerKey]);
        }
    }
});


jsonstream.on('data', (data) => {
    let submission = data;
    let id = variantToQuestion[submission["variant_id"]];
    
    if (!id) {
        console.error("Variant ID failed to map to Question ID");
    }
    let answers = submission["submitted_answer"]["_files"];

    if (!answers) {
        return;
    }

    if (submission["score"] !== 1) {
        return;
    }

    let answer = null;
    for (let j = 0; j < answers.length; ++j) {
        if (answers[j]["name"] !== "query.js") {
            answer = answers[j]["contents"];
            // for(let key in answers[j]) {
            //     if (key.startsWith("_file_editor")) {
            //         answer = answers[j][key];
            //     }
            // }
        }
    }

    if (answer === null) {
        return;
    }

    if (!(id in sorted)) {
        sorted[id] = {};
    }
    
    let buff = new Buffer(answer, 'base64');
    let text = buff.toString('utf-8');
    sorted[id][submission["auth_user_id"]] = text;

});

fs.createReadStream(file, {encoding: 'utf8'})
    .pipe(jsonstream);