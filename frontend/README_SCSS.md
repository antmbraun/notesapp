# SCSS Structure

This project uses SCSS for styling with a modular architecture.

## Directory Structure

```
src/scss/
├── base/           # Base styles and resets
│   └── _reset.scss
├── components/     # Component-specific styles
│   ├── _note-card.scss
│   └── _form.scss
├── layout/         # Layout styles
│   └── _app.scss
├── utils/          # Variables, mixins, and utilities
│   ├── _variables.scss
│   └── _mixins.scss
└── main.scss       # Main entry point (imports all)
```

## Build Process

Vite automatically compiles SCSS files when you run:
- `npm run dev` - Development server with hot reload
- `npm run build` - Production build

No additional build step is needed - Vite handles SCSS compilation automatically.

## Usage

Import the main SCSS file in your components:
```jsx
import './scss/main.scss'
```

## Adding New Styles

1. **Variables**: Add to `utils/_variables.scss`
2. **Mixins**: Add to `utils/_mixins.scss`
3. **Components**: Create new files in `components/` and import in `main.scss`
4. **Layout**: Add to `layout/_app.scss` or create new layout files

## Naming Convention

- Use kebab-case for file names: `_my-component.scss`
- Use BEM or similar for class names: `.note-card`, `.note-card__title`

