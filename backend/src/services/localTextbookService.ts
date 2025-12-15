import { promises as fs } from 'fs';
import * as path from 'path';

// Define the structure for our textbook content
interface TextbookChapter {
  id: string;
  title: string;
  content: string;
  sections: TextbookSection[];
}

interface TextbookSection {
  id: string;
  title: string;
  content: string;
}

interface SearchMatch {
  chapterId: string;
  chapterTitle: string;
  sectionId?: string;
  sectionTitle?: string;
  content: string;
  score: number;
}

// Service class for handling local textbook content
export class LocalTextbookService {
  private textbookContent: TextbookChapter[] = [];
  private readonly docsDir: string;

  constructor() {
    this.docsDir = path.join(__dirname, '..', '..', '..', 'frontend', 'text-book', 'docs');
  }

  // Load textbook content from the docs directory
  async loadTextbookContent(): Promise<TextbookChapter[]> {
    if (this.textbookContent.length > 0) {
      return this.textbookContent; // Return cached content if already loaded
    }

    try {
      const chapterDirs = await fs.readdir(this.docsDir);
      const chapters: TextbookChapter[] = [];

      for (const chapterDir of chapterDirs) {
        const chapterPath = path.join(this.docsDir, chapterDir);
        const stats = await fs.stat(chapterPath);

        if (stats.isDirectory()) {
          // Process chapter directory
          const chapterFiles = await fs.readdir(chapterPath);
          let chapterContent = '';
          const sections: TextbookSection[] = [];

          for (const file of chapterFiles) {
            if (file.endsWith('.md')) {
              const filePath = path.join(chapterPath, file);
              const fileContent = await fs.readFile(filePath, 'utf-8');

              // Extract title from markdown (first heading)
              const titleMatch = fileContent.match(/^#\s+(.+)$/m);
              const title = titleMatch ? titleMatch[1] : chapterDir;

              const section: TextbookSection = {
                id: `${chapterDir}-${file}`,
                title,
                content: fileContent
              };

              sections.push(section);
              chapterContent += `\n\n---\n\n${fileContent}`;
            }
          }

          if (sections.length > 0) {
            chapters.push({
              id: chapterDir,
              title: sections[0].title, // Use first section's title as chapter title
              content: chapterContent,
              sections
            });
          }
        } else if (chapterDir.endsWith('.md')) {
          // Handle files directly in docs directory (like intro.md)
          const filePath = path.join(this.docsDir, chapterDir);
          const fileContent = await fs.readFile(filePath, 'utf-8');

          // Extract title from markdown (first heading)
          const titleMatch = fileContent.match(/^#\s+(.+)$/m);
          const title = titleMatch ? titleMatch[1] : chapterDir.replace('.md', '');

          const section: TextbookSection = {
            id: chapterDir,
            title,
            content: fileContent
          };

          chapters.push({
            id: chapterDir.replace('.md', ''),
            title,
            content: fileContent,
            sections: [section]
          });
        }
      }

      this.textbookContent = chapters;
      console.log(`Loaded ${chapters.length} chapters from textbook`);
      return chapters;
    } catch (error) {
      console.error('Error loading textbook content:', error);
      // Return default content in case of error
      const defaultChapters: TextbookChapter[] = [{
        id: 'default',
        title: 'Physical AI & Humanoid Robotics Textbook',
        content: `# Physical AI & Humanoid Robotics Textbook

## Introduction
This is an introductory textbook about Physical AI and Humanoid Robotics. The book covers topics such as embodied intelligence, robot operating systems, digital twin simulation, AI brain systems, vision-language-action systems, and capstone projects.

## Chapter 1: Introduction to Physical AI & Embodied Intelligence
Physical AI represents a paradigm shift in artificial intelligence, moving beyond the purely digital realm of algorithms and data to interact with the physical world. It is the branch of AI that endows machines, particularly robots, with the ability to perceive, reason about, and act upon their environment in a physically embodied manner.

## Chapter 2: Basics of Humanoid Robotics
Humanoid robotics focuses on creating robots with human-like characteristics and capabilities. This includes understanding human anatomy, kinematics, and the mechanics of human-like movement.

## Chapter 3: ROS 2 Fundamentals
Robot Operating System (ROS) 2 is the framework used for developing robot applications. It provides services such as hardware abstraction, device drivers, libraries, and tools to aid in the development of robot applications.

## Chapter 4: Digital Twin & Simulation
Digital twin technology creates virtual replicas of physical systems, allowing for simulation, analysis, and optimization before implementation in the real world.

## Chapter 5: AI Robot Brain
The AI brain encompasses the decision-making systems, planning algorithms, and cognitive architectures that enable robots to operate intelligently in complex environments.

## Chapter 6: Vision-Language-Action Systems
Modern robotics systems integrate computer vision, natural language processing, and action execution to create sophisticated human-robot interaction capabilities.

## Chapter 7: Capstone: The Autonomous Humanoid
The final chapter integrates all concepts into a complete autonomous humanoid robot system.`,
        sections: [{
          id: 'default-intro',
          title: 'Introduction',
          content: `# Physical AI & Humanoid Robotics Textbook

This is an introductory textbook about Physical AI and Humanoid Robotics. The book covers topics such as embodied intelligence, robot operating systems, digital twin simulation, AI brain systems, vision-language-action systems, and capstone projects.`
        }]
      }];

      this.textbookContent = defaultChapters;
      return defaultChapters;
    }
  }

  // Search for relevant content based on query
  async search(query: string): Promise<SearchMatch[]> {
    const chapters = await this.loadTextbookContent();
    const queryLower = query.toLowerCase();
    const matches: SearchMatch[] = [];

    // Search through chapters and sections
    for (const chapter of chapters) {
      // Search in chapter content
      const chapterScore = this.calculateRelevanceScore(chapter.content, queryLower);
      if (chapterScore > 0) {
        matches.push({
          chapterId: chapter.id,
          chapterTitle: chapter.title,
          content: chapter.content,
          score: chapterScore
        });
      }

      // Search in sections
      for (const section of chapter.sections) {
        const sectionScore = this.calculateRelevanceScore(section.content, queryLower);
        if (sectionScore > 0) {
          matches.push({
            chapterId: chapter.id,
            chapterTitle: chapter.title,
            sectionId: section.id,
            sectionTitle: section.title,
            content: section.content,
            score: sectionScore
          });
        }
      }
    }

    // Sort matches by relevance score (highest first)
    return matches.sort((a, b) => b.score - a.score).slice(0, 5); // Return top 5 matches
  }

  // Calculate relevance score based on query terms matching
  private calculateRelevanceScore(content: string, query: string): number {
    const contentLower = content.toLowerCase();
    const queryTerms = query.split(/\s+/).filter(term => term.length > 2); // Only consider terms longer than 2 chars

    if (queryTerms.length === 0) return 0;

    let score = 0;
    for (const term of queryTerms) {
      if (contentLower.includes(term)) {
        // Give higher score for exact matches
        score += 10;
        // Additional points for multiple occurrences
        const occurrences = (contentLower.match(new RegExp(term, 'g')) || []).length;
        score += occurrences;
      }
    }

    // Boost score if the query terms appear in close proximity
    for (const term of queryTerms) {
      if (contentLower.includes(term)) {
        const termIndex = contentLower.indexOf(term);
        for (const otherTerm of queryTerms) {
          if (term !== otherTerm && contentLower.includes(otherTerm)) {
            const otherTermIndex = contentLower.indexOf(otherTerm);
            const distance = Math.abs(termIndex - otherTermIndex);
            // Boost score if terms are close together (max boost when within 100 chars)
            if (distance < 100) {
              score += Math.max(0, 10 - distance / 10);
            }
          }
        }
      }
    }

    return score;
  }

  // Get content summary for the textbook
  async getTextbookSummary(): Promise<string> {
    const chapters = await this.loadTextbookContent();
    return `The textbook contains ${chapters.length} chapters covering topics such as Physical AI, Humanoid Robotics, ROS 2, Digital Twin Simulation, AI Robot Brains, Vision-Language-Action Systems, and Autonomous Humanoids.`;
  }
}