import * as fs from 'fs/promises';
import * as path from 'path';
import { glob } from 'glob';

interface TextbookSection {
  id: string;
  title: string;
  content: string;
  chapter: string;
  section?: string;
}

export class TextbookService {
  private sections: TextbookSection[] = [];
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    await this.loadTextbookContent();
    this.initialized = true;
  }

  private async loadTextbookContent(): Promise<void> {
    try {
      const docsDir = path.join(__dirname, '..', '..', 'frontend', 'text-book', 'docs');
      const files = await glob('**/*.md', { cwd: docsDir });

      for (const file of files) {
        const filePath = path.join(docsDir, file);
        const content = await fs.readFile(filePath, 'utf-8');

        // Extract chapter and section info from file path
        const pathParts = file.split(path.sep);
        const chapter = pathParts[0] || 'intro';
        const section = pathParts[1]?.replace('.md', '') || '';

        // Parse content into sections
        const sections = this.parseMarkdownSections(content, chapter, section, file);
        this.sections.push(...sections);
      }

      console.log(`Loaded ${this.sections.length} textbook sections`);
    } catch (error) {
      console.error('Error loading textbook content:', error);
      // Fallback to sample content if docs aren't available
      this.sections = this.getSampleContent();
    }
  }

  private parseMarkdownSections(content: string, chapter: string, section: string, filePath: string): TextbookSection[] {
    const sections: TextbookSection[] = [];
    const lines = content.split('\n');
    let currentSection = '';
    let currentContent = '';

    for (const line of lines) {
      if (line.startsWith('# ')) {
        // New main section
        if (currentSection && currentContent) {
          sections.push({
            id: `${chapter}-${section}-${this.generateId(currentSection)}`,
            title: currentSection,
            content: currentContent.trim(),
            chapter,
            section: section || filePath
          });
        }
        currentSection = line.replace('# ', '').trim();
        currentContent = line + '\n';
      } else if (line.startsWith('## ')) {
        // New subsection
        currentContent += line + '\n';
      } else {
        currentContent += line + '\n';
      }
    }

    // Add the last section
    if (currentSection && currentContent) {
      sections.push({
        id: `${chapter}-${section}-${this.generateId(currentSection)}`,
        title: currentSection,
        content: currentContent.trim(),
        chapter,
        section: section || filePath
      });
    }

    return sections;
  }

  private generateId(text: string): string {
    return text.toLowerCase().replace(/[^a-z0-9]/g, '-').substring(0, 20);
  }

  private getSampleContent(): TextbookSection[] {
    return [
      {
        id: 'intro-welcome',
        title: 'Welcome to Physical AI & Humanoid Robotics',
        content: '# Welcome to Physical AI & Humanoid Robotics\n\nThis is an introductory textbook about Physical AI and Humanoid Robotics. The book covers topics such as embodied intelligence, robot operating systems, digital twin simulation, AI brain systems, vision-language-action systems, and capstone projects.',
        chapter: 'intro',
        section: 'welcome'
      },
      {
        id: 'ch1-intro-physical-ai',
        title: 'Introduction to Physical AI & Embodied Intelligence',
        content: '# Chapter 1: Introduction to Physical AI & Embodied Intelligence\n\n## 1.1 What is Physical AI?\n\nPhysical AI represents a paradigm shift in artificial intelligence, moving beyond the purely digital realm of algorithms and data to interact with the physical world. It is the branch of AI that endows machines, particularly robots, with the ability to perceive, reason about, and act upon their environment in a physically embodied manner.',
        chapter: 'ch1',
        section: 'intro-physical-ai'
      },
      {
        id: 'ch2-humanoid-robotics',
        title: 'Basics of Humanoid Robotics',
        content: '# Chapter 2: Basics of Humanoid Robotics\n\nHumanoid robotics focuses on creating robots with human-like characteristics and capabilities. This includes understanding human anatomy, kinematics, and the mechanics of human-like movement.',
        chapter: 'ch2',
        section: 'humanoid-robotics'
      }
    ];
  }

  async search(query: string, topK: number = 5): Promise<TextbookSection[]> {
    if (!this.initialized) {
      await this.initialize();
    }

    const queryLower = query.toLowerCase();
    const results: { section: TextbookSection; score: number }[] = [];

    for (const section of this.sections) {
      let score = 0;

      // Score based on title match
      if (section.title.toLowerCase().includes(queryLower)) {
        score += 100;
      }

      // Score based on content match
      const contentLower = section.content.toLowerCase();
      const matches = contentLower.match(new RegExp(queryLower, 'g'));
      if (matches) {
        score += matches.length * 10;
      }

      // Additional scoring for important keywords
      const keywords = ['physical ai', 'humanoid', 'robotics', 'embodied', 'intelligence'];
      for (const keyword of keywords) {
        if (contentLower.includes(keyword)) {
          score += 5;
        }
      }

      if (score > 0) {
        results.push({ section, score });
      }
    }

    // Sort by score and return top K
    return results
      .sort((a, b) => b.score - a.score)
      .slice(0, topK)
      .map(item => item.section);
  }

  async getFullTextbook(): Promise<string> {
    if (!this.initialized) {
      await this.initialize();
    }

    return this.sections.map(section => section.content).join('\n\n---\n\n');
  }
}