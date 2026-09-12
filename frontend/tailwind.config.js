/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1f2937",
        secondary: "#6366f1",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
  ],
};

module.exports = config;
