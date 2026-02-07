# CLAUDE.md

## Project Overview

Classic Analog Clock Widget — a standalone HTML/CSS/JavaScript web widget that displays a real-time analog clock with a digital time readout and Hebrew date. Designed for embedding in Notion, blogs, dashboards, or any website.

**Live demo:** https://dor-zommer.github.io/widgets/

## Tech Stack

- **HTML5** — RTL layout with `lang="he"` for Hebrew support
- **CSS3** — Flexbox, transforms, media queries, box-shadow effects
- **Vanilla JavaScript** — No frameworks or libraries; uses native `Date` and `Intl` APIs

**No build system, package manager, bundler, linter, or test framework.** This is a zero-dependency static site.

## File Structure

```
widgets/
├── index-html-file.html   # Entry point — clock markup and layout
├── script-js-file.js      # Clock logic — angle calculations, DOM updates, 1s interval
├── style-css-file.css     # All styling — clock face, hands, responsive breakpoints
├── README.md              # User-facing documentation (Hebrew)
└── CLAUDE.md              # This file
```

There are no subdirectories, config files, or generated artifacts.

## How It Works

`script-js-file.js` contains a single `updateClock()` function that:

1. Reads the current time via `new Date()`
2. Calculates rotation angles: seconds (6 deg/s), minutes (6 deg/min + smooth seconds), hours (30 deg/hr + smooth minutes)
3. Applies CSS `transform: rotate()` to hand elements via `getElementById`
4. Updates the digital display (`HH:MM:SS` with zero-padding)
5. Updates the date string using `toLocaleDateString('he-IL')` with full weekday

The clock initializes on `DOMContentLoaded` and ticks every 1000ms via `setInterval`.

## Running Locally

Open `index-html-file.html` directly in a browser. No server or build step is needed.

For a local server: `python3 -m http.server 8000` and visit `http://localhost:8000`.

## Code Conventions

- **CSS classes:** kebab-case (`.clock-container`, `.hour-hand`, `.digital-display`)
- **JS variables/functions:** camelCase (`updateClock`, `secondAngle`, `dateString`)
- **HTML IDs:** camelCase (`hourHand`, `minuteHand`, `digitalTime`)
- **File names:** descriptive with type suffix (`script-js-file.js`, `style-css-file.css`)
- **Language/locale:** Hebrew (`he-IL`) for date display; RTL document direction

## Responsive Design

One breakpoint at `max-width: 480px` scales down the clock face from 280px to 240px and adjusts hand lengths and font sizes.

## Key Implementation Details

- Clock hands use `transform-origin: bottom center` and are positioned at `bottom: 50%; left: 50%`
- Z-index layering: hour (3) > minute (2) > second (1), center dot (10)
- Second hand is colored red (`#e74c3c`); hour and minute hands are dark (`#333`)
- The initial rotation offset is -90 degrees (CSS hands start pointing up; angles are calculated from 3 o'clock position)

## Deployment

The project is deployed via GitHub Pages as a static site. No CI/CD pipeline exists. To deploy:

1. Push changes to the appropriate branch
2. Enable GitHub Pages in repository settings pointing to the branch root

## Guidelines for AI Assistants

- This is a small, self-contained widget. Keep changes minimal and focused.
- There is no build step — changes to any file take effect immediately when reloaded in a browser.
- There are no tests. Verify changes visually by opening the HTML file.
- Preserve the Hebrew locale and RTL direction.
- Do not introduce build tools, frameworks, or dependencies unless explicitly requested.
- The README is in Hebrew — maintain that language if editing it.
