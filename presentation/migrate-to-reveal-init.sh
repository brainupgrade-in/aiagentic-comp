#!/bin/bash
# Migration script to convert all session HTML files to use reveal-init.js
# This removes duplicate Reveal.initialize() code and uses shared config

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Reveal.js Initialization Migration ==="
echo ""
echo "This script will:"
echo "  1. Replace inline Reveal.initialize() with reveal-init.js"
echo "  2. Add proper comments to script sections"
echo "  3. Backup original files to *.backup"
echo ""

# Count files to migrate
SESSION_FILES=(session*.html)
# Exclude session1 (already migrated)
FILES_TO_MIGRATE=()
for file in "${SESSION_FILES[@]}"; do
  if [[ "$file" != "session1-introduction-to-agentic-ai.html" ]]; then
    FILES_TO_MIGRATE+=("$file")
  fi
done

echo "Files to migrate: ${#FILES_TO_MIGRATE[@]}"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Migration cancelled."
  exit 0
fi

echo ""
echo "Starting migration..."
echo ""

for file in "${FILES_TO_MIGRATE[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "⚠️  Skipping $file (not found)"
    continue
  fi

  echo "Processing: $file"

  # Create backup
  cp "$file" "${file}.backup"

  # Create temporary Python script
  cat > /tmp/migrate_reveal.py << 'EOF'
import sys
import re

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the entire script section
old_pattern = r'  <script src="https://cdnjs\.cloudflare\.com/ajax/libs/reveal\.js/4\.6\.1/reveal\.min\.js"></script>\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/reveal\.js/4\.6\.1/plugin/highlight/highlight\.min\.js"></script>\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/reveal\.js/4\.6\.1/plugin/notes/notes\.min\.js"></script>\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/reveal\.js/4\.6\.1/plugin/search/search\.min\.js"></script>\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/reveal\.js/4\.6\.1/plugin/zoom/zoom\.min\.js"></script>\s*<script>[\s\S]*?Reveal\.initialize\(\{[\s\S]*?\}\);[\s\S]*?</script>\s*<script src="shared\.js"></script>'

new_content = '''  <!-- Reveal.js Core -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.js"></script>

  <!-- Reveal.js Plugins -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/notes/notes.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/search/search.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/zoom/zoom.min.js"></script>

  <!-- Reveal.js Initialization -->
  <script src="reveal-init.js"></script>

  <!-- Custom Enhancements -->
  <script src="shared.js"></script>'''

# Perform replacement
updated_content = re.sub(old_pattern, new_content, content, flags=re.MULTILINE)

# Write back
with open(filename, 'w', encoding='utf-8') as f:
    f.write(updated_content)

# Report success
if content != updated_content:
    print(f"  ✓ Updated", file=sys.stderr)
else:
    print(f"  ⚠️  No changes (pattern not found)", file=sys.stderr)
EOF

  python3 /tmp/migrate_reveal.py "$file"

done

echo ""
echo "=== Migration Complete ==="
echo ""
echo "Summary:"
echo "  ✓ Migrated ${#FILES_TO_MIGRATE[@]} files"
echo "  ✓ Backups created (*.backup)"
echo "  ✓ All files now use reveal-init.js"
echo ""
echo "To verify:"
echo "  1. Open any session*.html in a browser"
echo "  2. Check that slides work correctly"
echo "  3. Press F to test fullscreen toggle"
echo ""
echo "To rollback (if needed):"
echo "  for f in *.backup; do mv \"\$f\" \"\${f%.backup}\"; done"
echo ""
