const { TopHatQuestionType } = require('./enums');

/**
 * Processes a TopHat question to extract the corresponding Wooclap question
 * type.
 * @param {*} question Raw question to process
 * @returns The Wooclap question type.
 */
module.exports = function getQuestionType(question) {
  switch (question.question_type) {
    case TopHatQuestionType.FillInTheBlankQuestion:
      return 'FillInTheBlanks';
    case TopHatQuestionType.LongAnswerQuestion:
      return 'OpenQuestion';
    case TopHatQuestionType.MatchingQuestion:
      return 'Matching';
    case TopHatQuestionType.MultipleChoiceQuestion:
      if (question.correct_answers) {
        return 'MCQ';
      }

      return 'Poll';
    case TopHatQuestionType.NumericalAnswerQuestion:
      return 'GuessNumber';
    case TopHatQuestionType.SortingQuestion:
      return 'Sorting';
    case TopHatQuestionType.WordAnswerQuestion:
      return 'OpenQuestion';
  }
};
