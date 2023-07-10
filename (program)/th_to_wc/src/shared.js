module.exports = {
  // The input file is not super clean and the newline characters are not always
  // consistent. We use this regexp to split the string on all possible newline
  // variants.
  NEWLINE_DELIMITER_REGEXP: /\n|\n\v|\v/,
};
