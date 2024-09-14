module.exports = {
  roots: ['<rootDir>/js'],  // Adjust this path to match the actual directory structure
  testMatch: ['**/?(*.)+(test).[tj]s?(x)'], // Matches test files with .test.js/.test.jsx
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest', // Use babel-jest to transpile tests
  },
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
};

