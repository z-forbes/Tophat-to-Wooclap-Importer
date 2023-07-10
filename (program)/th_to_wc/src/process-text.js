/**
 * This function processes a text string and applies transformations to make it
 * compatible with Wooclap strings.
 * @param {string} text Input string to transform
 * @returns Transformed string
 */
module.exports = function processText(text = '') {
  return (
    text
      // Replace '[math]' and '[/math]' by '$'
      // this is because that's how we write LaTeX formulas
      .replaceAll('[math]', '$')
      .replaceAll('[/math]', '$')
      // Replace '\\$' by '$ $$ $' (the spacing is important)
      // this is one way of escaping the dollar sign in our implementation
      // .replaceAll(/\\\$/g, '$ $$ $')
      // Remove opening <p> tags
      .replaceAll(/<p[^>]+>/g, '')
      // Replace closing </p> tags by newlines
      .replaceAll('</p>', '\n')
      // Replace '&lt;' by '<'
      .replaceAll('&lt;', '<')
      // Replace '&gt;' by '>'
      .replaceAll('&gt;', '>')
      // Remove the extra stars from elements such as **a.** -> a.
      .replaceAll('**', '')
      // Remove non-breaking space
      .replaceAll('&nbsp;', '')
      // Replace the code blocks by triple backticks
      .replaceAll('[code]', '```')
      .replaceAll('[/code]', '```')
      // Remove leading / trailing spaces
      .trim()
  );
};
