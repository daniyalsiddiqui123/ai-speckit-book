<!--
Sync Impact Report:
Version change:  → 1.0.0
Modified principles: None
Added sections: Core Principles, Technical Stack, Quality, Content, and Workflow Standards, Governance
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .gemini/commands/sp.adr.toml: ✅ updated
  - .gemini/commands/sp.analyze.toml: ✅ updated
  - .gemini/commands/sp.checklist.toml: ✅ updated
  - .gemini/commands/sp.clarify.toml: ✅ updated
  - .gemini/commands/sp.constitution.toml: ✅ updated
  - .gemini/commands/sp.git.commit_pr.toml: ✅ updated
  - .gemini/commands/sp.implement.toml: ✅ updated
  - .gemini/commands/sp.phr.toml: ✅ updated
  - .gemini/commands/sp.plan.toml: ✅ updated
  - .gemini/commands/sp.specify.toml: ✅ updated
  - .gemini/commands/sp.tasks.toml: ✅ updated
Follow-up TODOs: None
-->
# Project Principles & Standards Constitution

## Core Principles

### Spec-Driven Workflow
Create specs before writing chapters.

### Clarity, Accuracy, and Simplicity
Maintain clarity, accuracy, and simplicity in all explanations.

### Consistent Terminology
Use consistent terminology across Physical AI, Robotics, and Humanoid Systems.

### Architectural Decision Records (ADRs)
Document important decisions using ADRs.

### Modularity and Maintainability
Keep all content modular, structured, and easy to update.

### Clean MDX Formatting
Use clean MDX formatting and avoid unnecessary complexity.

## Technical Stack

- Docusaurus 3+
- Spec-Kit Plus (CLI + ADR + Spec workflows)
- Git + GitHub for version control
- TypeScript for custom components
- Deployment using GitHub Pages or Vercel

## Quality, Content, and Workflow Standards

### Quality Requirements
- All specs must be approved before generating content.
- All generated chapters must be manually reviewed before merging.
- Maintain consistent tone, formatting, and depth across chapters.
- Include learning objectives and theory in every chapter.
- Validate all code snippets (Python, JS, TS).
- Keep file structure clean and organized.

### Content Standards
- Minimum 800 words per chapter.
- Provide clear explanations of Physical AI and Humanoid Robotics concepts.
- Include references to credible research or documentation.
- No plagiarism; all content must be original or properly cited.

### Workflow Requirements
- Commit early and often.
- Each major update should go through PR review.
- Tag releases using semantic versioning (vX.Y.Z).
- Maintain CHANGELOG.md for tracking updates.

## Governance
The Constitution outlines the core principles and standards guiding this project.
Amendments to this Constitution require:
- Documentation of proposed changes and their rationale.
- Approval through a pull request review process by designated maintainers.
- A migration plan for any backward-incompatible changes.
Compliance reviews will be conducted periodically to ensure adherence to these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07