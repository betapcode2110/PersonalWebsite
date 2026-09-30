# Review Round 1 Handoff Report — Neo-Brutalist Home Page Redesign

## Overview
Review and quality hardening for the Neo-Brutalist redesign of the Personal Website Home Page (`index.astro`, `HeroSection.astro`, `NoteCard.astro`, `global.css`, `Timeline.astro`).

---

## 1. Issues Identified in Prior Attempt

### Issue 1: Severe text crushing & horizontal layout overflow on mobile in `NoteCard.astro`
- **Input**: Viewport width $\le$ 640px (e.g. standard mobile viewports: 375px, 390px, 412px, 320px).
- **Expected**: Text on the left remains readable with adequate width ($\ge 180$px); thumbnail/cover image on right displays proportionally; no card horizontal overflow.
- **Actual**: Prior attempt hardcoded `w-[280px] shrink-0` on the image container. In a 375px mobile viewport with `px-6` (available width = 327px), subtracting 280px left a mere 47px column (minus 40px padding = 7px of readable width), causing single-character vertical wraps. On viewports below 360px, the card physically clipped and breached viewport bounds.
- **Root cause**: Hardcoded desktop fixed width `w-[280px]` with `shrink-0` without responsive breakpoints.
- **Fix**: Made the image container responsive (`w-28 sm:w-52 md:w-[280px] shrink-0`), reduced mobile padding (`p-4 sm:p-5`), and made the placeholder icon responsive (`text-2xl sm:text-4xl`), while strictly preserving `flex flex-row items-stretch justify-between` on all viewports.

### Issue 2: Horizontal page blowout from unconstrained `HeroSection.astro` email link & flex layout
- **Input**: Mobile viewport $\le$ 640px.
- **Expected**: Avatar and intro card stay within 100% viewport width without introducing horizontal page scroll.
- **Actual**: `flex gap-5 items-stretch` forced a 144px avatar side-by-side with an intro card containing `tranhoan2971999@gmail.com` (~213px in 14px monospace) + 48px padding + 20px gap = 425px, blowing past the 327px mobile container width and overflowing off the right of the screen.
- **Root cause**: Rigid horizontal row on mobile and missing word-break rules on email address.
- **Fix**: Changed top row layout to `flex-col sm:flex-row gap-4 sm:gap-5 items-start sm:items-stretch`, allowed avatar to size to `w-32 h-32 sm:w-36 sm:h-36`, and applied `break-all sm:break-normal` to the email link.

### Issue 3: 4th category tab ("shader") clipped and container missing neo-brutalist white background in `index.astro`
- **Input**: Mobile viewport $\le$ 480px.
- **Expected**: All 4 tabs ("all", "tech art", "mobile game", "shader") remain visible or gracefully scrollable; container background matches the white card styling from the reference image.
- **Actual**: Tab buttons had `text-sm` (14px monospace) and container had `overflow-hidden` with no background color specified, causing "shader" to be clipped off-screen and the page background to bleed through between tabs.
- **Root cause**: Rigid text size, missing `overflow-x-auto`, and omitted `bg-white` on `#category-tabs`.
- **Fix**: Added `bg-white`, `overflow-x-auto sm:overflow-hidden`, and updated buttons to `px-2 text-xs sm:text-sm whitespace-nowrap`.

### Issue 4: Fragile script timing and duplicate listener risk in category tabs client script
- **Input**: Script execution when `document.readyState !== 'loading'` (e.g. deferred module execution or Astro view transitions / client routing).
- **Expected**: Click listeners attach reliably without duplicate bindings.
- **Actual**: Used only `document.addEventListener('DOMContentLoaded', initCategoryTabs)`. In environments where `DOMContentLoaded` had already fired when the module executed, the listener would never trigger. Furthermore, repeated invocations would attach duplicate listeners.
- **Root cause**: No check for `document.readyState` or guard against multiple bindings.
- **Fix**: Added `if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', ...); } else { initCategoryTabs(); }`, registered `astro:page-load`, and added `container.dataset.bound = 'true'` guard.

### Issue 5: Non-brutalist fuzzy shadow on card hover in `src/styles/global.css`
- **Input**: Hovering over `.card-hover`.
- **Expected**: Crisp neo-brutalist hard offset shadow.
- **Actual**: `box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);` (soft blurred drop-shadow).
- **Root cause**: Residual legacy style not converted to neo-brutalism.
- **Fix**: Updated `.card-hover:hover` to `box-shadow: 3px 3px 0px #000; transform: translate(-2px, -2px);`.

---

## 2. Summary of Changes
- `src/components/HeroSection.astro`: Responsive `flex-col sm:flex-row`, `break-all sm:break-normal` on email link, maintained `border-2 border-black rounded-none bg-white`.
- `src/components/NoteCard.astro`: Maintained horizontal flex layout (`flex-row items-stretch justify-between`), made right image container responsive (`w-28 sm:w-52 md:w-[280px] shrink-0`), adjusted padding (`p-4 sm:p-5`), and responsive icon (`text-2xl sm:text-4xl`).
- `src/pages/index.astro`: Added `bg-white` and `overflow-x-auto sm:overflow-hidden` to `#category-tabs`, adjusted tab button typography (`px-2 text-xs sm:text-sm whitespace-nowrap`), and hardened client script against readyState timing and duplicate bindings.
- `src/styles/global.css`: Replaced blurred hover shadow with crisp neo-brutalist hard shadow (`box-shadow: 3px 3px 0px #000; transform: translate(-2px, -2px)`).
- `src/components/Timeline.astro`: Added `break-all sm:break-normal` to email link.

---

## 3. Verification Record
- **`npm.cmd run build`**: 7 pages built in 1.35s with exit code 0.
- **`npm.cmd run astro check`**: 16 files checked, 0 errors, 0 warnings.
- **Real Browser Visual Regression (Headless Edge/Chromium)**:
  - Desktop (1024x1400): Verified neo-brutalist 2px black borders, sharp corners, white tab container, and 280px image thumbnails (`desktop_after_fix.png`).
  - Mobile (375x1800): Verified horizontal overflow eliminated (`bad=0`), intro card readable, all 4 category tabs visible, and note cards maintaining text on left and image on right without text squishing (`mobile_after_fix.png`).
  - Ultra-narrow (320x1800): Verified 0 overflow bugs on 320px viewport (`mobile_320_after_fix.png`).
- **Real Browser Interactive Test**:
  - Ran headless Edge script clicking each category tab in sequence (`test_interactive.html`):
    - Clicking "Tech Art" toggled active state classes (`tab-active bg-black text-white font-semibold`), stripped inactive classes, and showed only Tech Art notes (`style.display === ''`) while hiding others (`style.display === 'none'`).
    - Clicking "Shader" isolated Shader notes.
    - Clicking "all" restored all 5 notes.
    - Verified result: `INTERACTIVE_TEST_SUCCESS`.
