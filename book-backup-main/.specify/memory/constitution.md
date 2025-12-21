<<<<<<< HEAD
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
=======
# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### [PRINCIPLE_6_NAME]


[PRINCIPLE__DESCRIPTION]

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
>>>>>>> 04a085f8ef614d6047417366f8b016a1d678189d
