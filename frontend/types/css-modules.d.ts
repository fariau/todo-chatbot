declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

// For global CSS imports (like in layout.tsx)
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// Global style imports don't need exports