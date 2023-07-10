# Top Hat to Wooclap importer

This script transforms the questions from the Top Hat .csv format into a Wooclap .csv format.

# Installation

You need to install [Node.js](https://nodejs.org/en/) to run this script.

Then, install the dependencies using:

```bash
npm install
```

# Usage

Place your .csv files into the `input/` folder. Then, run the script with the following command:

```bash
node .
```

The processed files will be placed into the `output/` folder. They will be named as follows: `<original_file_name>_PROCESSED_<chunk_number>.csv` where

- `<original_file_name>` is the name of the original file.
- `<chunk_number>` is the number of the chunk (starting from 1) because the script splits the original file into chunks of 50 questions each.

The processed files can then be imported into Wooclap using the "Import from Excel" feature.

Note: running the script will clear the output folder, so be sure to move the processed files somewhere else before running the script again.
