import type {ReactNode} from 'react';
import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

// Define the SVG components directly in the file
const BookIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={styles.featureSvg}>
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
  </svg>
);

const TerminalIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.featureSvg}>
    <rect x="2" y="4" width="20" height="16" rx="2" fill="currentColor"/>
    <path d="M5 8L9 12L5 16" stroke="#00FF00" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M11 16H14" stroke="#00FF00" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BrainIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className={styles.featureSvg}>
    <path d="M9 12a3 3 0 0 0 -3 -3h-1a2 2 0 0 0 -2 2v4a2 2 0 0 0 2 2h1a3 3 0 0 0 3 -3v-4zm6 0a3 3 0 0 1 3 -3h1a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-1a3 3 0 0 1 -3 -3v-4zm-6 -9a6 6 0 0 0 -6 6v1a2 2 0 0 0 2 2h1a3 3 0 0 1 3 -3v-4zm6 0a6 6 0 0 1 6 6v1a2 2 0 0 1 -2 2h-1a3 3 0 0 0 -3 -3v-4z" />
  </svg>
);


type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Chapters',
    Svg: BookIcon,
    description: (
      <>
        Explore the fundamentals of physical AI, from kinematics and perception 
        to the latest in humanoid locomotion.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    Svg: TerminalIcon,
    description: (
      <>
        Engage with interactive examples. Use the 'Ask the Book' feature to get 
        answers powered by our backend RAG model.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Research',
    Svg: BrainIcon,
    description: (
      <>
        Stay updated with the latest advancements in humanoid robotics and AI, 
        including topics on human-robot interaction.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
