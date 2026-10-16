# Brand-utkast — fsdnorge.no
Petter Gulliksen · 19. september 2026 · ikke pushet

## Konsept
Merket er en **sjansemåler-bue** (status/hub), ikke bil eller Tesla-logo.
Wordmark følger navet: `fsd` hvit · `norge` `#5b8cff` · `.no` muted.
Farger fra `site.css`: canvas `#070b14`, panel `#0e1624`, blue `#5b8cff`.

## Filer
| Fil | Bruk |
|-----|------|
| `mark-512.png` / `mark-256.png` | App-ikon / generelt merke |
| `logo-dark.png` / `logo-light.png` | Wordmark-lockup |
| `favicon.ico` + `favicon-*.png` | Faner |
| `apple-touch-icon.png` | iOS hjemskjerm |
| `og-default.png` (1200×630) | Open Graph / Twitter-kort |
| `mark.svg` / `logo-wordmark.svg` | Vektor-utkast |

## HTML (når Kåre gir grønt)
```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:image" content="https://fsdnorge.no/og-default.png">
<meta name="twitter:card" content="summary_large_image">
```

Ikke produksjon før redaksjonell OK.
