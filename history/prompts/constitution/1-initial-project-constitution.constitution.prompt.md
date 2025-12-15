---
id: 1
title: Initial Project Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: gemini
feature: none
branch: {{BRANCH}}
user: {{USER}}
command: /sp.constitution
labels: [constitution, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
tests:
[]
---

## Prompt

/sp.constitution

System Rules:

- Build a Physical AI & Humanoid Robotics learning website using Docusaurus.
- All code must be clean, documented and modular.
- Use Firebase for authentication only.
- Use MDX for course content.
- All chapters must contain a <ChapterTranslate /> component at the top.
- UI must follow a modern design trend.
- Pages must be mobile responsive.
- Do not generate Urdu pages manually; translation toggle will handle Urdu.
- Navigation: Home, Modules, Weekly Breakdown, Login, Signup.
- Use Firebase email/password authentication.
- Use AuthContext + ProtectedRoute architecture.
- Store authentication using localStorage session method.
- No backend server except Firebase.
- Deployment target: Vercel.
- All chapters English only.

## Response snapshot

I have created the project constitution and updated the plan template to reflect the new principles.

## Outcome

- ✅ Impact: Created the initial project constitution and updated related templates.
- 🧪 Tests: No tests were run.
- 📁 Files: Created and updated 2 files.
- 🔁 Next prompts: The user can now start creating features.
- 🧠 Reflection: The process of creating the constitution from the user's prompt was straightforward. The key was to map the user's rules to the principles in the template.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (none): none
