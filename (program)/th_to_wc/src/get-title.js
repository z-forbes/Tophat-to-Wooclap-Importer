const { TopHatQuestionType } = require('./enums');

/**
 * Processes a TopHat question to extract the corresponding Wooclap question
 * title.
 * @param {*} question Raw question to process
 * @returns The Wooclap question title.
 */
module.exports = function getTitle(question) {
  switch (question.question_type) {
    // For FillInTheBlankQuestion, the question_text contains the blanks which
    // will be processed as the Choices.
    case TopHatQuestionType.FillInTheBlankQuestion:
      return question.display_name;
    default:
      // The `display_name` on Top Hat is sometimes used by the teacher to enter
      // the first part of the question, so we concatenate both the
      // `display_name` and the `question_text` into a single field.
      return `${question.display_name}\n${question.question_text}`.trim();
  }
};
