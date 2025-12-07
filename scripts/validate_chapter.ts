import fs from 'fs';

const requiredHeadings = [
  'Objectives',
  'Theoretical Foundation',
  'Practical Implementation',
  'Case Study',
  'Exercises',
  'Chapter Summary',
  'Further Reading',
];

export function validateChapter(markdownContent: string): boolean {
  for (const heading of requiredHeadings) {
    if (!markdownContent.includes(`## ${heading}`)) {
      console.error(`Missing heading: ## ${heading}`);
      return false;
    }
  }
  return true;
}


const filePath = process.argv[2];
if (!filePath) {
  console.error('Please provide a file path.');
  process.exit(1);
}

const content = fs.readFileSync(filePath, 'utf-8');
if (validateChapter(content)) {
  console.log(`${filePath} is valid.`);
} else {
  console.error(`${filePath} is invalid.`);
  process.exit(1);
}

