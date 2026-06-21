# Skill: Autonomous Pull Request Review

## Purpose

Review GitHub Pull Requests autonomously using multiple specialized reviewers.

This skill is intended to produce developer-quality code reviews instead of generic LLM feedback.

---

## Review Workflow

Whenever a Pull Request is requested:

1. Retrieve the PR metadata.
2. Fetch the complete diff.
3. Parse modified files.
4. Ignore generated files unless explicitly requested.
5. Delegate review to specialized agents:
   - Security Reviewer
   - Style Reviewer
   - Tests Reviewer
   - Architecture Reviewer
6. Collect every review.
7. Merge duplicate findings.
8. Produce one final review.

---

## File Priorities

Prioritize reviewing:

- Source code
- Infrastructure
- GitHub Actions
- Dockerfiles
- Configuration
- Dependency manifests

Lower priority:

- Documentation
- Images
- Lock files
- Generated code

---

## Review Philosophy

Only report actionable issues.

Avoid:

- Personal preferences
- Trivial formatting
- Unnecessary refactoring
- Over-engineering

Every finding should answer:

- What is wrong?
- Why is it important?
- How should it be fixed?

---

## Severity Levels

### Critical

Can lead to:

- Security compromise
- Data loss
- Production outage

### High

Likely bug or major maintainability issue.

### Medium

Worth fixing before merge.

### Low

Minor improvement.

### Info

Observation only.

---

## Evidence Requirement

Never speculate.

Every issue must reference:

- filename
- function
- changed lines
- relevant code

If there isn't enough evidence, do not report it.

---

## Agent Responsibilities

Security Agent

- vulnerabilities
- secrets
- authentication
- authorization
- injections
- unsafe shell execution

Style Agent

- readability
- naming
- maintainability
- duplication
- complexity

Tests Agent

- missing tests
- regression risk
- edge cases
- CI

Architecture Agent

- design
- abstractions
- module boundaries
- scalability
- coupling

---

## Final Output

Produce a review containing:

- Summary
- Blocking Issues
- Non-blocking Suggestions
- Positive Observations
- Final Recommendation

Possible recommendations:

- Approve
- Approve with Comments
- Request Changes

---

## Important Rules

Do not invent issues.

Do not review unchanged code unless necessary for context.

Prefer precision over quantity.

Five accurate comments are better than fifty generic comments.