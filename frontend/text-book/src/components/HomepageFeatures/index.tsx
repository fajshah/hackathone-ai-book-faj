import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Interactive Book',
    description: (
      <>
        Explore the Physical AI & Humanoid Robotics textbook with interactive features,
        real-time examples, and hands-on learning experiences.
      </>
    ),
  },
  {
    title: 'AI-Powered Learning',
    description: (
      <>
        Get personalized answers to your questions about robotics, AI, and humanoid systems
        using advanced AI technology.
      </>
    ),
  },
  {
    title: 'Robotics Concepts',
    description: (
      <>
        Master complex robotics concepts through visual explanations,
        practical examples, and real-world applications.
      </>
    ),
  },
];

function Feature({title, description}: FeatureItem) {
  // Define images based on the title
  const getImage = (title: string) => {
    switch(title) {
      case 'Interactive Book':
        return (
          <img
            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231e3a8a'%3E%3Cpath d='M12 2l-7 4v16l7-4 7 4V6l-7-4zM12 4.15L19 8v12l-7-4-7 4V8l7-3.85z'/%3E%3Cpath d='M9 10h6v2H9v-2zm0 4h6v2H9v-2z'/%3E%3C/svg%3E"
            alt="Interactive Book"
            className={styles.featureSvg}
          />
        );
      case 'AI-Powered Learning':
        return (
          <img
            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231e3a8a'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/%3E%3C/svg%3E"
            alt="AI Learning"
            className={styles.featureSvg}
          />
        );
      case 'Robotics Concepts':
        return (
          <img
            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231e3a8a'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2V7zm0 8h2v2h-2v-2z'/%3E%3C/svg%3E"
            alt="Robotics"
            className={styles.featureSvg}
          />
        );
      default:
        return (
          <img
            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231e3a8a'%3E%3Cpath d='M12 2l-7 4v16l7-4 7 4V6l-7-4z'/%3E%3C/svg%3E"
            alt="Default"
            className={styles.featureSvg}
          />
        );
    }
  };

  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className="text--center padding-horiz--md">
        <div className="text--center">
          {getImage(title)}
        </div>
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
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