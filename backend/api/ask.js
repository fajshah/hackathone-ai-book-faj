const fs = require('fs').promises;
const path = require('path');

// Function to load textbook content from the docs directory
async function loadTextbookContent() {
  try {
    const docsDir = path.join(__dirname, '..', '..', 'frontend', 'text-book', 'docs');
    let content = "";

    // Read all files in the docs directory and subdirectories
    const chapterDirs = await fs.readdir(docsDir);

    for (const chapterDir of chapterDirs) {
      const chapterPath = path.join(docsDir, chapterDir);
      const stats = await fs.stat(chapterPath);

      if (stats.isDirectory()) {
        const files = await fs.readdir(chapterPath);

        for (const file of files) {
          if (file.endsWith('.md')) {
            const filePath = path.join(chapterPath, file);
            const fileContent = await fs.readFile(filePath, 'utf-8');

            content += `\n\n---\n\n${fileContent}`;
          }
        }
      } else if (chapterDir.endsWith('.md')) {
        // Handle files directly in docs directory (like intro.md)
        const filePath = path.join(docsDir, chapterDir);
        const fileContent = await fs.readFile(filePath, 'utf-8');

        content += `\n\n---\n\n${fileContent}`;
      }
    }

    console.log(`Loaded textbook content from ${chapterDirs.length} directories`);
    return content;
  } catch (error) {
    console.error('Error loading textbook content:', error);

    // Return default content in case of error
    const defaultContent = `# Physical AI & Humanoid Robotics Textbook

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
The final chapter integrates all concepts into a complete autonomous humanoid robot system.`;

    return defaultContent;
  }
}

// Simple text-based search function to find relevant content
function findRelevantContent(textbookContent, query) {
  const paragraphs = textbookContent.split('\n\n---\n\n');
  const queryLower = query.toLowerCase();

  // Find paragraphs that contain the query terms
  const relevantParagraphs = paragraphs.filter(paragraph => {
    return paragraph.toLowerCase().includes(queryLower) ||
           queryLower.split(' ').some(word => word.length > 3 && paragraph.toLowerCase().includes(word));
  });

  // If we didn't find specific matches, return the first few paragraphs as general context
  if (relevantParagraphs.length === 0) {
    return paragraphs.slice(0, 3).join('\n\n---\n\n');
  }

  // Return up to 3 relevant paragraphs
  return relevantParagraphs.slice(0, 3).join('\n\n---\n\n');
}

// Main function to answer questions based on textbook content
async function askQuestion(query) {
  console.log(`Processing query: "${query}"`);

  try {
    // Load the textbook content
    const textbookContent = await loadTextbookContent();
    console.log(`Textbook content loaded, length: ${textbookContent.length}`);

    // Find relevant content based on the query
    const relevantContent = findRelevantContent(textbookContent, query);
    console.log(`Relevant content found, length: ${relevantContent.length}`);

    // Generate a response based on the relevant content
    const response = `Based on the Physical AI and Humanoid Robotics textbook:

${relevantContent}

For more detailed information, please refer to the relevant chapters in the textbook.`;

    return response;
  } catch (error) {
    console.error('Error in askQuestion function:', error);
    return `I encountered an error while processing your request: ${error.message}. Please try asking your question again.`;
  }
}

// Export the function for use in other modules
module.exports = { askQuestion };

// If this file is run directly, provide a simple test
if (require.main === module) {
  const testQuery = "What is Physical AI?";
  askQuestion(testQuery).then(response => {
    console.log('\nResponse:');
    console.log(response);
  });
}