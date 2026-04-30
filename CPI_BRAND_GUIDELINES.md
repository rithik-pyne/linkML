# UK CPI Brand Guidelines for Dashboard

**Source**: https://www.uk-cpi.com/  
**Organization**: Centre for Process Innovation (CPI)  
**Date Extracted**: 2026-04-24

---

## 1. Brand Colors

### Primary Blue Palette
CPI uses a rich blue color scheme as their primary brand identity:

```css
/* Primary Brand Blue */
--cpi-blue-primary: #0058AA;      /* Main brand blue (tile color) */
--cpi-blue-dark-1: #004E98;       /* Darker blue */
--cpi-blue-dark-2: #004483;       /* Even darker */
--cpi-blue-dark-3: #003E77;       /* Deep blue */
--cpi-blue-dark-4: #00376B;       /* Very deep blue */
--cpi-blue-dark-5: #002F58;       /* Navy blue */
--cpi-blue-dark-6: #00274c;       /* Darkest navy */
--cpi-blue-dark-7: #001d38;       /* Almost black navy */
--cpi-blue-dark-8: #00172b;       /* Near black */

/* Lighter Blues */
--cpi-blue-light-1: #006fa0;      /* Cyan-blue */
--cpi-blue-light-2: #0072dd;      /* Bright blue */
--cpi-blue-light-3: #006692;      /* Medium cyan */
```

### Secondary Colors
```css
/* Alert/Warning Red */
--cpi-red-primary: #d3353d;       /* Alert red */
--cpi-red-dark: #af262d;          /* Dark red */
--cpi-red-light: #dc5f65;         /* Light red */

/* Accent Orange */
--cpi-orange-primary: #ff9200;    /* Orange accent */
--cpi-orange-light: #ffa833;      /* Light orange */
--cpi-orange-lighter: #ffbe66;    /* Lighter orange */
--cpi-orange-lightest: #FFBC7A;   /* Lightest orange */

/* Accent Green */
--cpi-green-teal: #007169;        /* Teal accent */
```

### Neutral & Background Colors
```css
/* Backgrounds */
--cpi-bg-primary: #ffffff;        /* White */
--cpi-bg-light-1: #FBFBFB;        /* Off-white */
--cpi-bg-light-2: #F3F6FB;        /* Very light blue-gray */
--cpi-bg-light-3: #f2f6f9;        /* Light blue background */
--cpi-bg-light-4: #e7edf2;        /* Light gray-blue */
--cpi-bg-light-5: #E7EDF2;        /* Light blue-gray */
--cpi-bg-light-6: #e0e9f7;        /* Pale blue */
--cpi-bg-light-7: #f4fbf7;        /* Mint background */
--cpi-bg-light-8: #f2fafd;        /* Ice blue */
--cpi-bg-cream: #fefbf3;          /* Cream */
--cpi-bg-pink: #F6E5E5;           /* Light pink (alerts) */

/* Grays */
--cpi-gray-50: #f4f4f4;           /* Very light gray */
--cpi-gray-100: #f4f4f5;          /* Light gray */
--cpi-gray-200: #f3f4f6;          /* Light gray variant */
--cpi-gray-300: #e5e7eb;          /* Medium-light gray */
--cpi-gray-400: #e4e7f0;          /* Gray-blue */
--cpi-gray-500: #e2e3df;          /* Gray-beige */
--cpi-gray-600: #d1d5db;          /* Medium gray */
--cpi-gray-700: #d1d1d1;          /* Medium gray */
--cpi-gray-800: #c5cde0;          /* Blue-gray */
--cpi-gray-900: #e5e5e5;          /* Border gray */

/* Black */
--cpi-black: #000000;
```

---

## 2. Logo & Branding Assets

### Logo Files
- **Safari Pinned Tab SVG**: https://www.uk-cpi.com/img/site/safari-pinned-tab.svg
- **Favicon (PNG)**: https://www.uk-cpi.com/img/site/android-chrome-192x192.png
- **High-res Logo**: https://www.uk-cpi.com/img/site/android-chrome-512x512.png

### Brand Portal
Full brand guidelines available at: https://cpi.frontify.com/d/5LG66FPfme1R/guidelines

### Logo Usage
- **Download**: https://cpi.frontify.com/d/5LG66FPfme1R/guidelines#/visual/logo
- Refer to brand portal for proper usage guidelines

---

## 3. Recommended Color Usage for Dashboard

### For Clinical Decision Support Dashboard

```css
/* Primary UI Elements */
--primary-brand: #0058AA;          /* Headers, primary buttons, logo */
--primary-dark: #003E77;           /* Hover states, active navigation */
--primary-light: #0072dd;          /* Links, accents */

/* Clinical Alerts */
--alert-critical: #d3353d;         /* Urgent alerts (rising VAF, resistance) */
--alert-warning: #ff9200;          /* Medium priority alerts */
--alert-info: #0072dd;             /* Informational notices */
--alert-success: #007169;          /* Positive outcomes (complete response) */

/* Backgrounds */
--bg-page: #FBFBFB;                /* Page background */
--bg-panel: #ffffff;               /* Panel/card backgrounds */
--bg-header: #001d38;              /* Dark header/navigation */
--bg-sidebar: #F3F6FB;             /* Sidebar background */

/* Text */
--text-primary: #000000;           /* Main text */
--text-secondary: #003E77;         /* Secondary text */
--text-muted: #d1d5db;             /* Muted/disabled text */
--text-on-dark: #ffffff;           /* Text on dark backgrounds */

/* Borders */
--border-default: #e5e5e5;         /* Card borders */
--border-focus: #0058AA;           /* Focus states */
```

---

## 4. Typography (Inferred)

CPI uses a clean, modern sans-serif approach typical of tech/innovation organizations.

**Recommended Fonts** (to match CPI aesthetic):
- **Primary**: Inter, "Helvetica Neue", Arial, sans-serif
- **Monospace** (for data): "Roboto Mono", "Courier New", monospace

**Font Weights**:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

---

## 5. Dashboard Component Color Mapping

### DisclaimerBanner
```css
background: #d3353d;  /* CPI Red */
color: #ffffff;
border: 2px solid #af262d;
```

### PatientSelector
```css
background: #ffffff;
border: 1px solid #e5e5e5;
focus: #0058AA;
```

### Timeline Chart
```css
/* VAF Line */
stroke: #0058AA;  /* CPI Primary Blue */

/* RECIST Markers */
Complete Response: #007169;  /* Teal */
Partial Response: #0072dd;   /* Light blue */
Stable Disease: #ff9200;     /* Orange */
Progressive Disease: #d3353d; /* Red */

/* Grid & Axes */
grid: #e5e5e5;
axis: #000000;
```

### Alert Panel
```css
/* Alert Types */
Urgent: #d3353d (Red)
High: #ff9200 (Orange)
Medium: #0072dd (Blue)
Low: #007169 (Teal)

/* Alert Background */
background: #F6E5E5; /* Light pink for critical */
background: #fefbf3; /* Cream for warnings */
```

### Treatment Recommendations
```css
/* Evidence Levels */
Level I (RCT): #007169;        /* Teal - highest evidence */
Level II (Phase II): #0072dd;  /* Blue - good evidence */
Level III (Retrospective): #ff9200;  /* Orange - moderate */
Level IV (Expert Opinion): #d1d5db;  /* Gray - lowest */
```

---

## 6. Design Principles

Based on CPI's brand identity:

1. **Professional & Clinical**: Use blues for trust and medical authority
2. **Clear Hierarchy**: Dark navy (#001d38) for headers, white (#ffffff) for content
3. **Alert Differentiation**: Red for critical, orange for warnings, blue for info
4. **Clean & Modern**: Minimal borders, generous whitespace, subtle shadows
5. **Accessibility**: Ensure WCAG AA contrast ratios (4.5:1 minimum)

---

## 7. Tailwind CSS Configuration

Add this to your `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        cpi: {
          blue: {
            DEFAULT: '#0058AA',
            50: '#E7EDF2',
            100: '#e0e9f7',
            200: '#0072dd',
            300: '#006fa0',
            400: '#0058AA',
            500: '#004E98',
            600: '#003E77',
            700: '#002F58',
            800: '#001d38',
            900: '#00172b',
          },
          red: {
            DEFAULT: '#d3353d',
            light: '#dc5f65',
            dark: '#af262d',
          },
          orange: {
            DEFAULT: '#ff9200',
            light: '#ffbe66',
          },
          teal: {
            DEFAULT: '#007169',
          },
        },
      },
      fontFamily: {
        sans: ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
        mono: ['Roboto Mono', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
}
```

---

## 8. Implementation Checklist

- [ ] Download CPI logo SVG from https://www.uk-cpi.com/img/site/safari-pinned-tab.svg
- [ ] Configure Tailwind with CPI color palette
- [ ] Use #0058AA for primary buttons, headers, and navigation
- [ ] Use #d3353d for critical alerts (rising VAF, resistance mutations)
- [ ] Use #001d38 for dark header/footer backgrounds
- [ ] Ensure white text on dark backgrounds for WCAG compliance
- [ ] Test all alert colors for sufficient contrast
- [ ] Add CPI logo to dashboard header/navigation

---

## 9. Reference Links

- **CPI Website**: https://www.uk-cpi.com/
- **Brand Portal**: https://cpi.frontify.com/d/5LG66FPfme1R/guidelines
- **Logo Guidelines**: https://cpi.frontify.com/d/5LG66FPfme1R/guidelines#/visual/logo
- **Social**: @ukcpi (Twitter), /ukCPI (LinkedIn)

---

**Notes**:
- Colors extracted from CPI website CSS (April 2024)
- Primary brand blue confirmed: #0058AA (msapplication-TileColor)
- Full brand guidelines require Frontify portal access
- This document provides sufficient guidance for dashboard implementation