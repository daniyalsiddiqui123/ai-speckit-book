// This would be a test file for a node.js script, using a test runner like Jest.
// For simplicity, I will write a simple test that can be run with ts-node.

import { validateChapter } from './validate_chapter';

const passing_markdown = `
# Title

## Objectives
...

## Theoretical Foundation
...

## Practical Implementation
...

## Case Study
...

## Exercises
...

## Chapter Summary
...

## Further Reading
...
`;

const failing_markdown = `
# Title

## Objectives
...

## Theory (Incorrect Heading)
...
`;

if (validateChapter(passing_markdown)) {
  console.log('Passing markdown test passed.');
} else {
  console.error('Passing markdown test failed.');
  process.exit(1);
}

if (!validateChapter(failing_markdown)) {
  console.log('Failing markdown test passed.');
} else {
  console.error('Failing markdown test failed.');
  process.exit(1);
}
