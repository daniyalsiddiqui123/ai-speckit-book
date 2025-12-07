# Tasks: Robotics Textbook Structure

**Input**: Design documents from `/specs/001-robotics-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: A Test-Driven Development (TDD) approach is used. Validation and test tasks are included before implementation tasks.

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize the Docusaurus project and configure the basic structure.

- [x] T001 Verify the existing Docusaurus project in the `my-website/` directory.
- [x] T002 [P] Configure project metadata (title, tagline, URL) in `my-website/docusaurus.config.js`.
- [x] T003 [P] Configure the sidebar for the docs in `my-website/docusaurus.config.js` to reflect the 4-part structure.
- [x] T004 Create the main directory structure for the 4 parts of the textbook inside `my-website/docs/`: `part1-foundations/`, `part2-perception-actuation/`, `part3-intelligence-learning/`, `part4-advanced-topics/`.
- [x] T005 [P] Create a directory for shared code examples at `my-website/code-examples/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create reusable components and validation scripts required by all content chapters.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T006 [P] Create a test for a reusable React component for simple visual aids in `my-website/src/components/__tests__/SimpleVisualAid.test.tsx`.
- [x] T007 Implement the reusable React component for simple visual aids in `my-website/src/components/SimpleVisualAid.tsx`.
- [x] T008 [P] Create a test script in `my-website/scripts/validate_chapter.test.ts` to check if a Markdown file contains the required H2 headings (Objectives, Theory, etc.).
- [x] T009 Implement the chapter validation script in `my-website/scripts/validate_chapter.ts`.


**Checkpoint**: Foundation ready - content creation can now begin.

---

## Phase 3: User Story 1 - Instructor Course Planning (Priority: P1) 🎯 MVP

**Goal**: Create the complete, templated file structure for all 16 chapters, making the textbook's outline navigable for an instructor.

**Independent Test**: The Docusaurus site can be built and served locally. An instructor can see all 16 chapter titles in the sidebar, navigate to each, and see the placeholder headings.

### Tests for User Story 1 ⚠️

- [x] T011 Create a test script in `my-website/scripts/validate_structure.test.ts` that verifies all 16 chapter markdown files exist in the correct directories.

### Implementation for User Story 1

- [x] T012 [P] [US1] Create 16 placeholder markdown files for all chapters within the `my-website/docs/partX-*/` directories (e.g., `chap1-intro-physical-ai.md`).
- [x] T013 [US1] Run the structure validation script `my-website/scripts/validate_structure.test.ts` and ensure it passes.
- [x] T014 [P] [US1] For each of the 16 markdown files, add the required H2 placeholder headings (e.g., `## Objectives`, `## Theoretical Foundation`, etc.).
- [x] T015 [US1] Run the chapter validation script `my-website/scripts/validate_chapter.ts` against all 16 files to ensure they pass.

**Checkpoint**: At this point, the full skeleton of the textbook is complete and navigable.

---

## Phase 4: User Story 2 - Student Topic-Based Learning (Priority: P2)

**Goal**: Populate one sample chapter (Chapter 7: Kinematics) with all content types to validate the student learning experience.

**Independent Test**: A user can navigate to the "Kinematics" chapter and find complete text, a working code example, and a visual aid, and can successfully answer an exercise.

### Tests for User Story 2 ⚠️


- [x] T016 [P] [US2] Create a test for the specific kinematics visual aid component in `my-website/src/components/__tests__/KinematicsVisual.test.tsx`.

### Implementation for User Story 2

- [x] T017 [US2] Write the "Theoretical Foundation" and "Case Study" content in `my-website/docs/part2-perception-actuation/chap7.md`.


- [x] T018 [US2] Implement the simple visual aid for kinematics in `my-website/src/components/KinematicsVisual.tsx` and embed it in the chapter markdown file.
- [x] T019 [US2] Write the "Exercises" and "Summary" sections in `my-website/docs/part2-perception-actuation/chap7.md`.

**Checkpoint**: User Story 2 is a complete, vertical slice of a chapter, demonstrating full functionality.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Finalize the project with deployment automation and quality checks.

- [x] T020 [P] Configure and implement a Markdown linting process for the `my-website/docs/` directory.
- [x] T021 [P] Configure and implement a code formatting process (e.g., Prettier for TypeScript/JavaScript) for all source code.
- [x] T022 Create and configure the CI/CD pipeline for deployment in `.github/workflows/deploy.yml`.
- [x] T023 Perform and document an accessibility audit against the deployed site to meet `NFR-001`.
- [x] T024 Perform and document a performance audit using Lighthouse to meet `NFR-002`.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion. BLOCKS all user stories.
- **User Stories (Phase 3 & 4)**: Depend on Foundational completion.
- **Polish (Phase 5)**: Can be done in parallel with user stories but must be completed before final delivery.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Can start after Foundational (Phase 2). It is independent of User Story 1.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Deploy the site with the full skeleton and placeholder chapters. This is the MVP, demonstrating the complete structure for stakeholder review.

### Incremental Delivery

1.  Complete MVP (US1).
2.  Complete Phase 4 (US2) to create a fully-featured sample chapter.
3.  Use the pattern from Phase 4 to complete all remaining chapters.
4.  Complete Phase 5 to finalize and automate the project.
