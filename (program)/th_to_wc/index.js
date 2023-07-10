/* eslint-disable no-console */

const fs = require('fs');
const path = require('path');
const util = require('util');

const csv = require('csv-parser');
const { stringify } = require('csv-stringify/sync');

const processQuestion = require('./src/process-question');

const inputFolder = path.resolve(__dirname, './input');
const outputFolder = path.resolve(__dirname, './output');
const writeFileAsync = util.promisify(fs.writeFile);

function processFile(filePath) {
  const headers = ['Type', 'Title', 'Correct', 'Choices'];
  const processedQuestions = [];

  // Extract the filename without the extension from the filepath
  const filename = path.basename(filePath, path.extname(filePath));

  console.log(`Processing ${filename}...`);

  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (data) => {
      const processedQuestion = processQuestion(data);

      processedQuestions.push([
        processedQuestion.Type,
        processedQuestion.Title,
        processedQuestion.Correct,
        ...processedQuestion.Choices,
      ]);
    })
    .on('end', async () => {
      // Only keep the questions that have a type because we don't support every
      // single question type from Top Hat.
      const filteredProcessedQuestions = processedQuestions.filter(
        ([processedQuestionType]) => !!processedQuestionType
      );

      // Write the `results` array by chunks to make the file smaller.
      const CHUNK_SIZE = 50;
      let chunkIdx = 1;
      while (filteredProcessedQuestions.length > 0) {
        const chunk = filteredProcessedQuestions.splice(0, CHUNK_SIZE);

        // eslint-disable-next-line no-await-in-loop
        await writeFileAsync(
          path.resolve(outputFolder, `${filename}_PROCESSED_${chunkIdx}.csv`),
          stringify([headers, ...chunk])
        );

        console.log(
          `${filename}: chunk ${chunkIdx} of ${chunk.length} questions`
        );

        chunkIdx++;
      }

      console.log('Done');
    });
}

function processFiles() {
  // Create output folder if it doesn't exist
  if (!fs.existsSync(outputFolder)) {
    fs.mkdirSync(outputFolder);
  }

  // Clean the output folder before processing the files
  fs.readdirSync(outputFolder).forEach((file) => {
    fs.unlinkSync(path.resolve(outputFolder, file));
  });

  // Use a glob pattern to process multiple files at once
  const files = fs.readdirSync(inputFolder);
  const filePaths = files.map((file) => path.resolve(inputFolder, `./${file}`));

  filePaths.forEach(processFile);
}

processFiles();
