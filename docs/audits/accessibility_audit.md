# Accessibility Audit Process

This document outlines the steps to perform an accessibility audit for the "Physical AI & Humanoid Robotics" textbook website, aiming to meet `NFR-001` (WCAG 2.1 Level AA guidelines).

## Tools Used

*   **Lighthouse**: Integrated into Chrome DevTools for automated checks.
*   **Axe DevTools**: Browser extension for automated and guided manual accessibility testing.
*   **Manual Inspection**: Essential for checking keyboard navigation, focus management, semantic structure, and content clarity.

## Audit Steps

1.  **Automated Checks (Lighthouse/Axe)**:
    *   Navigate to key pages of the deployed website (e.g., homepage, a sample chapter, a blog post).
    *   Run Lighthouse Accessibility audit and record scores and identified issues.
    *   Run Axe DevTools on each page and address reported violations.

2.  **Keyboard Navigation Test**:
    *   Ensure all interactive elements (links, buttons, navigation items) can be reached and activated using only the keyboard (Tab, Shift+Tab, Enter, Spacebar).
    *   Verify visible focus indicators are present.

3.  **Semantic Structure Review**:
    *   Inspect HTML structure to ensure appropriate use of headings (`<h1>` to `<h6>`), lists (`<ul>`, `<ol>`), landmarks (`<main>`, `<nav>`, `<aside>`, `<footer>`), and other semantic elements.
    *   Verify correct heading order (no skipped levels).

4.  **Color Contrast Check**:
    *   Use a color contrast analyzer tool (e.g., WebAIM Contrast Checker) to ensure text and interactive elements meet minimum contrast ratios against their background.

5.  **Image Alt Text Verification**:
    *   Ensure all meaningful images have descriptive `alt` text. Decorative images should have `alt=""`.

6.  **Form Element Accessibility (if applicable)**:
    *   Verify all form fields have associated `label` elements.
    *   Check for clear error messages and validation feedback.

7.  **Content Clarity and Readability**:
    *   Ensure language is clear, concise, and easy to understand.
    *   Verify appropriate reading level and sufficient line spacing.

8.  **Responsive Design Check**:
    *   Confirm the layout adapts gracefully to different screen sizes and orientations, without loss of content or functionality (related to `NFR-003`).

## Documentation

*   Record all findings, including passing checks, identified issues, and steps taken to remediate them.
*   Provide screenshots or code snippets for issues found.
*   Track progress towards WCAG 2.1 Level AA compliance.
