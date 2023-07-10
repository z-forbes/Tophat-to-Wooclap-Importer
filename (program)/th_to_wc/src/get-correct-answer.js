const { TopHatQuestionType } = require('./enums');
const getChoices = require('./get-choices');
const { NEWLINE_DELIMITER_REGEXP } = require('./shared');

/**
 * Processes a TopHat question to extract the correct answer for the Wooclap
 * question.
 * @param {*} question Raw question to process
 * @returns The correct answer for the Wooclap question.
 */
module.exports = function getCorrectAnswer(question) {
  switch (question.question_type) {
    case TopHatQuestionType.FillInTheBlankQuestion:
      return '';
    case TopHatQuestionType.MultipleChoiceQuestion:
      // If there is no correct answer in the input file, we return an empty
      // string because it's a Poll.
      if (!question.correct_answers) {
        return '';
      }

      // Map the choices to uppercase to make the comparison case-insensitive.
      const choices = getChoices(question).map(choice =>
        choice.toUpperCase().trim()
      );

      return (
        question.correct_answers
          // There can be multiple correct answers separated by a newline.
          .split(NEWLINE_DELIMITER_REGEXP)
          .map(correctAnswer => correctAnswer.toUpperCase().trim())
          .filter(correctAnswer => correctAnswer)
          // We determine the index of each correct answer in the choices array.
          // The index is 1-based in the Excel export.
          .map(correctAnswer => choices.indexOf(correctAnswer) + 1)
          .sort()
          .join(', ')
      );
    case TopHatQuestionType.WordAnswerQuestion:
      return (
        question.correct_answers
          // There can be multiple correct answers separated by a newline.
          .split(NEWLINE_DELIMITER_REGEXP)
          .map(correctAnswer => correctAnswer.trim())
          .filter(correctAnswer => correctAnswer)
          .join(';')
      );
    case TopHatQuestionType.SortingQuestion:
      return '';
    default:
      return question.correct_answers || '';
  }
};
