<!-- Sync Impact Report -->
<!--
Version change: 1.0.0 → 1.1.0
List of modified principles:
- Simplicity: Updated description
- Accuracy: Updated description
- Minimalism: Updated description
- Fast Builds: Updated description
- Free-tier Architecture: Updated description
- RAG Answers ONLY from Book Text: Updated description
Added sections: Key Features, Design Style & Tone, Intended Audience
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/sp.constitution.md: ✅ updated (no specific update needed for this command itself, but acknowledging its role)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Purpose

Create a clean, concise, AI-Native textbook for the hackathon project “Physical AI & Humanoid Robotics.”
Focus on embodied intelligence and the connection between AI systems (digital brain) and physical/simulated humanoid robots (body).
The book must be optimized for Docusaurus UI, GitHub Pages deployment, and free-tier RAG integration.

## Scope

The project encompasses 6 short, practical chapters:
1.  Foundations of Physical AI
2.  Humanoid Robotics Fundamentals
3.  ROS 2 for Humanoid Control
4.  Simulation Pipeline (Gazebo, Isaac Sim, Digital Twins)
5.  Vision-Language-Action (VLA) Systems
6.  Capstone: Simple AI-to-Robot Control Pipeline

Key scope aspects include a modern Docusaurus UI, "Select-text → Ask AI" integration, a RAG chatbot using Qdrant + Neon + FastAPI, optional Urdu translation mode, and a free-tier-friendly architecture.

## Core Principles

### Simplicity
Content, UI, and architecture MUST be simple, clear, and easy to understand for beginners.

### Accuracy
All technical content MUST be accurate, up-to-date, and reflect best practices in Physical AI and Humanoid Robotics.

### Minimalism
Design and implementation SHOULD be minimalist, focusing on essential features to avoid bloat and ensure fast builds.

### Fast Builds
The project's setup MUST enable rapid build times for development, testing, and deployment workflows.

### Free-tier Safe
All chosen technologies and services MUST operate within free-tier limits to ensure accessibility and zero operational cost for students.

### RAG Answers ONLY from Book Text
The integrated RAG chatbot MUST derive all its answers strictly from the textbook's content to maintain consistency and factual integrity.

## Constraints

The project MUST adhere to the following technical and operational constraints:
- No GPU dependency: The system MUST function without requiring a GPU.
- Lightweight embeddings only: Embedding models MUST be lightweight and efficient.
- Works on student laptops: The development and runtime environment MUST be compatible with typical student laptop specifications.
- Must deploy cleanly on GitHub Pages: The application MUST successfully build and deploy to GitHub Pages without issues.

## Key Features

- AI-native textbook: Content designed for AI-driven learning.
- Clean UI + short chapters: Optimized for quick and efficient learning.
- Free-tier RAG chatbot: Interactive AI assistant for concept clarification.
- Project-based learning: Practical application through hands-on projects.
- Capstone humanoid AI pipeline: A culminating project integrating AI with robotics.
- Optional bilingual (Urdu): Support for additional language localization.

## Design Style & Tone

- Short, clear paragraphs: Easy to digest and understand.
- Beginner-friendly and practical: Accessible to new learners with a focus on real-world application.
- Robotics + AI integration mindset: Emphasizing the synergy between AI and physical systems.
- Emphasis on embodied intelligence: Highlighting the connection between AI and robotic bodies.

## Intended Audience

- Robotics beginners
- AI learners
- Hackathon participants
- Students building practical humanoid control systems

## Governance

This Constitution supersedes all other practices. Amendments to this Constitution MUST be documented, undergo an approval process, and include a clear migration plan if changes impact existing systems or guidelines. All Pull Requests (PRs) and code reviews MUST verify compliance with the principles outlined herein. Any introduction of complexity MUST be thoroughly justified and demonstrate alignment with the principle of Minimalism.

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06