declare module '*.svg' {
  import React = require('react');
  export const ReactComponent: React.FC<React.SVGProps<SVGSVGElement>>;
  const src: string;
  export default src;
}

declare module '@theme/Heading' {
  import type { ComponentProps } from 'react';

  const Heading: React.ComponentType<ComponentProps<'h1'> & { as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' }>;
  export default Heading;
}
