/* eslint-disable camelcase */
const getChoices = require('./get-choices');
const getCorrectAnswer = require('./get-correct-answer');
const getQuestionType = require('./get-question-type');
const getTitle = require('./get-title');
const processText = require('./process-text');

/**
 * Processes a raw TopHat question from the CSV to transform it into a Wooclap
 * question.
 * @param {*} data Raw question to process
 * @returns The corresponding Wooclap question.
 */
module.exports = function processQuestion(data) {
  // Some columns are left unused for now.
  const rawQuestion = {
    // item_id,
    question_type: data.question_type,
    display_name: data.display_name,
    question_text: data.question_text,
    correct_answers: data.correct_answers,
    multiple_choice_list: data.multiple_choice_list,
    // sort_randomized_options,
    match_a: data.match_a,
    match_b: data.match_b,
    // randomized_match_b,
  };

  // Process the values to remove HTML tags, extra spaces, etc.
  rawQuestion.question_text = processText(rawQuestion.question_text);
  rawQuestion.display_name = processText(rawQuestion.display_name);
  rawQuestion.correct_answers = processText(rawQuestion.correct_answers);
  rawQuestion.multiple_choice_list = processText(
    rawQuestion.multiple_choice_list
  );
  rawQuestion.match_a = processText(rawQuestion.match_a);
  rawQuestion.match_b = processText(rawQuestion.match_b);

  const processedQuestion = {
    Type: getQuestionType(rawQuestion),
    Title: getTitle(rawQuestion),
    Correct: getCorrectAnswer(rawQuestion),
    Choices: getChoices(rawQuestion),
  };

  return processedQuestion;
};
