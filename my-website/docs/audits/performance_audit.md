# Performance Audit Process

This document outlines the steps to perform a performance audit for the "Physical AI & Humanoid Robotics" textbook website, aiming to meet `NFR-002` (p99 page load time < 2 seconds).

## Tools Used

*   **Lighthouse**: Integrated into Chrome DevTools for comprehensive performance analysis.
*   **WebPageTest**: For more advanced multi-location testing and waterfall analysis.

## Audit Steps

1.  **Baseline Measurement (Lighthouse)**:
    *   Navigate to key pages of the deployed website (e.g., homepage, a sample chapter, a blog post).
    *   Open Chrome DevTools, go to the Lighthouse tab.
    *   Run a "Performance" audit with "Desktop" and "Mobile" settings.
    *   Record the scores (Performance, FCP, LCP, CLS, TBT) for each page.

2.  **Identify Bottlenecks**:
    *   Review Lighthouse audit reports for recommendations on optimizing images, reducing JavaScript bundle size, leveraging browser caching, and minimizing render-blocking resources.
    *   Analyze the "Network" tab in Chrome DevTools during page load to identify large assets or slow requests.

3.  **Advanced Analysis (WebPageTest - Optional but Recommended)**:
    *   Use WebPageTest to test page load performance from various geographic locations and network conditions.
    *   Analyze waterfall charts to identify request dependencies and timing issues.

4.  **Optimization Strategy**:
    *   Prioritize optimizations based on impact and effort.
    *   Focus on Core Web Vitals (LCP, FID/INP, CLS).

5.  **Re-audit and Compare**:
    *   After implementing optimizations, re-run Lighthouse and WebPageTest audits.
    *   Compare new scores with baseline measurements to quantify improvements.

## Documentation

*   Record all audit results, including initial scores, identified issues, implemented optimizations, and final scores.
*   Provide screenshots of key performance metrics before and after optimizations.
*   Track progress towards achieving the `NFR-002` target.
