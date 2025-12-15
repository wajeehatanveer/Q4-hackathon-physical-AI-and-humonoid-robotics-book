import React, { JSX, useEffect, type ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

// Import AOS (Animate On Scroll)
import AOS from 'aos';
import 'aos/dist/aos.css'; // Import AOS CSS

// Placeholder for module data with new icons (emojis for now, can be replaced by Lucide/Heroicons later)
const modulesOverview = [
  {
    title: 'Foundational Concepts',
    description: 'Explore the core principles of Physical AI and Humanoid Robotics.',
    link: '/docs',
    icon: '💡', // Placeholder icon
  },
  {
    title: 'ROS 2 Mastery',
    description: 'Master the Robotic Operating System 2 (ROS 2) for robust control.',
    link: '/docs/module1/ros2-intro',
    icon: '🤖', // Placeholder icon
  },
  {
    title: 'Digital Twin Simulations',
    description: 'Dive into high-fidelity physics simulation with Gazebo and Unity.',
    link: '/docs/module2/gazebo-physics',
    icon: '💻', // Placeholder icon
  },
  {
    title: 'AI-Powered Robot Brains',
    description: 'Advanced perception, learning, and training with NVIDIA Isaac™.',
    link: '/docs/module3/isaac-sim',
    icon: '🧠', // Placeholder icon
  },
  {
    title: 'Vision-Language-Action (VLA)',
    description: 'Converge Large Language Models (LLMs) and Robotics for intelligent actions.',
    link: '/docs/module4/voice-to-action',
    icon: '🗣️', // Placeholder icon
  },
];

function HomepageHero(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      {/* Floating Blur Circles */}
      <div className={styles.blurCircle1}></div>
      <div className={styles.blurCircle2}></div>
      <div className={styles.blurCircle3}></div>

              <div className={clsx('container', styles.heroContent)}>
              <div className={styles.heroTextContent}>
                <Heading as="h1" className={clsx('hero__title', styles.heroTitle)} data-aos="slide-right">
                  {siteConfig.title} {/* Uses the updated title from config */}
                </Heading>
                <p className={clsx('hero__subtitle', styles.heroSubtitle)} data-aos="slide-left" data-aos-delay="200">
                  Explore the future of intelligent robots.
                </p>
                <div className={styles.buttons} data-aos="fade-up" data-aos-delay="400">
                  <Link className={clsx('button button--lg', styles.ctaButton)} to="/docs/">
                    Start Your Journey
                  </Link>
                </div>
              </div>
              <div className={styles.heroImageContainer} data-aos="fade-left" data-aos-delay="500">
                <img src="/img/robot-futuristic.svg" alt="Futuristic Robot" className={styles.heroImage} />
              </div>
            </div>    </header>
  );
}

function HomepageModulesOverview(): JSX.Element {
  return (
    <section className={styles.modules}>
      <div className="container">
        <Heading as="h2" className={clsx('text--center', styles.sectionHeading)} data-aos="fade-up">
          What You Will Learn
        </Heading>
        <div className="row">
          {modulesOverview.map((module, idx) => (
            <div key={idx} className={clsx('col col--4', styles.moduleItem)} data-aos="fade-up" data-aos-delay={idx * 150}>
              <Link to={module.link} className={styles.moduleCard}>
                <div className="text--center">
                  <span className={styles.moduleIcon}>{module.icon}</span>
                  <Heading as="h3" className={styles.moduleTitle}>{module.title}</Heading>
                </div>
                <p className={styles.moduleDescription}>{module.description}</p>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

import { useChatStore } from '../store/useChatStore';

function AskTheAISection(): JSX.Element {
  const { openChat } = useChatStore();

  const handleOpenChatbot = () => {
    openChat();
  };

  return (
    <section className={styles.askTheAI}>
      <div className="container text--center" data-aos="fade-up">
        <Heading as="h2" className={styles.sectionHeading}>
          Have a Question?
        </Heading>
        <p className={styles.sectionSubheading}>
          Our AI assistant, trained on the content of this book, is here to help.
        </p>
        <div className={styles.buttons}>
          <button
            className={clsx('button button--primary button--lg', styles.ctaButton)}
            onClick={handleOpenChatbot}
          >
            Open Humanoid Assistant
          </button>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  // Initialize AOS when the component mounts
  useEffect(() => {
    AOS.init({
      duration: 1000, // animation duration
      once: true,      // whether animation should happen only once - while scrolling down
    });
    AOS.refresh(); // re-init AOS on route change if needed
  }, []); // Empty dependency array means this effect runs once on mount

  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Learn about Physical AI and Humanoid Robotics.">
      <HomepageHero />
      <main>
        <HomepageModulesOverview />
        <AskTheAISection />
        {/* <HomepageFeatures /> - Keeping this commented out as it's not used */}
      </main>
    </Layout>
  );
}
