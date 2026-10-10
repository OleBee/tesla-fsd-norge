#!/usr/bin/env bash
# Renderer delingsbildet 1:1 i 1200×630 (ingen skalering = skarp tekst).
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p assets/og
google-chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --screenshot="$PWD/assets/og/tadnorge-og.png" \
  "file://$PWD/scripts/og/og-image.html" 2>/dev/null
python3 - <<'PY'
from PIL import Image
im = Image.open("assets/og/tadnorge-og.png").convert("RGB")
assert im.size == (1200, 630), im.size
im.save("assets/og/tadnorge-og.png", optimize=True)
print("ok", im.size)
PY
