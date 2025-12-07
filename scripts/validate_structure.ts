import fs from 'fs';
import path from 'path';

function validateStructure(baseDir: string, expectedFileCount: number): boolean {
    let fileCount = 0;
    const parts = ['part1-foundations', 'part2-perception-actuation', 'part3-intelligence-learning', 'part4-advanced-topics'];
    for (const part of parts) {
        const partDir = path.join(baseDir, part);
        if (fs.existsSync(partDir)) {
            const files = fs.readdirSync(partDir).filter(f => f.endsWith('.md'));
            fileCount += files.length;
        }
    }
    console.log(`Found ${fileCount} markdown files.`);
    return fileCount === expectedFileCount;
}

const docsDir = 'my-website/docs';
const expectedFiles = 16;

if (validateStructure(docsDir, expectedFiles)) {
  console.log(`Validation successful: Found ${expectedFiles} markdown files.`);
  process.exit(0);
} else {
  console.error(`Validation failed: Did not find ${expectedFiles} markdown files.`);
  process.exit(1);
}
