const { TopHatQuestionType } = require('./enums');
const { NEWLINE_DELIMITER_REGEXP } = require('./shared');

/**
 * Processes a TopHat question to extract the corresponding choices for the
 * Wooclap question.
 * @param {*} question Raw question to process
 * @returns The array of choices for the Wooclap question.
 */
module.exports = function getChoices(question) {
  switch (question.question_type) {
    case TopHatQuestionType.FillInTheBlankQuestion:
      // The blanks are separated by the pipe symbol.
      const blanks = question.correct_answers
        // The correct answers are separated by the pipe symbol.
        .split('|')
        .map(blank =>
          blank
            // The variations of the correct answers are separated by the
            // \v symbol.
            .replace(/\v/g, ', ')
            // Remove the "blank1:" prefix.
            .replace(/blank(\d+):/g, '')
            .trim()
        );

      return [
        // eslint-disable-next-line arrow-body-style
        question.question_text.replace(/<blank(\d+)>/g, (_, blankIdx) => {
          // Keeping the below code in comment in case it's useful later because
          // it might be more robust if the blanks are not ordered in the input
          // file.
          // const regexp = new RegExp(`blank${blankIdx}: ([^|]*)`);
          // const blankText = question.correct_answers.match(regexp)[1].trim();

          // The `blankIdx` is an index starting from 1 instead of 0.
          return `[${blanks[blankIdx - 1]}]`;
        }),
      ];
    case TopHatQuestionType.MatchingQuestion:
      // Note that The `match_b` can contain more elements than `match_a`. This
      // is because Top Hat allows having extra choices to make the student
      // think.
      // When translating those questions to Wooclap, we can just ignore the
      // extra elements. The other elements are mapped one-to-one (first element
      // of `match_a` is mapped to the first element of `match_b`, etc.).

      const matchSources = question.match_a
        .split(NEWLINE_DELIMITER_REGEXP)
        .filter(matchSource => matchSource)
        .map(matchSource => matchSource.trim());

      const matchDestinations = question.match_b
        .split(NEWLINE_DELIMITER_REGEXP)
        .filter(matchDestination => matchDestination)
        .map(matchDestination => matchDestination.trim());

      return matchSources.map(
        (matchSource, idx) => `${matchSource} --- ${matchDestinations[idx]}`
      );
    case TopHatQuestionType.MultipleChoiceQuestion:
      return question.multiple_choice_list
        .split(NEWLINE_DELIMITER_REGEXP)
        .map(choice => choice.trim())
        .filter(choice => choice);
    case TopHatQuestionType.SortingQuestion:
      return question.correct_answers
        .split(NEWLINE_DELIMITER_REGEXP)
        .filter(choice => choice)
        .map(choice => choice.trim());
    default:
      return [];
  }
};
