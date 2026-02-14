#!/usr/bin/env python3
"""
Remove inline font-size and color styles from HTML files and replace with CSS classes.
"""
import re
import sys
from pathlib import Path

# Mapping of inline styles to CSS classes
FONT_SIZE_MAP = {
    'font-size:0.52em': 'text-052',
    'font-size:0.54em': 'text-054',
    'font-size:0.55em': 'text-xs',
    'font-size:0.6em': 'text-060',
    'font-size:0.65em': 'text-sm',
    'font-size:0.68em': 'text-068',
    'font-size:0.7em': 'text-070',
    'font-size:0.72em': 'text-072',
    'font-size:0.75em': 'text-base',
    'font-size:0.78em': 'text-078',
    'font-size:0.8em': 'text-080',
    'font-size:0.82em': 'text-082',
    'font-size:0.85em': 'text-085',
    'font-size:0.9em': 'text-lg',
    'font-size:1em': 'text-100',
    'font-size:1.05em': 'text-xl',
    'font-size:1.1em': 'text-110',
    'font-size:1.2em': 'text-120',
    'font-size:1.3em': 'text-130',
    'font-size:1.4em': 'text-140',
    'font-size:1.5em': 'text-150',
    'font-size:1.6em': 'text-160',
    'font-size:2.5em': 'text-2xl',
    'font-size:2.8em': 'text-280',
    'font-size:3em': 'text-3xl',
}

COLOR_MAP = {
    'color:#111': 'color-black',
    'color:#90caf9': 'color-lightblue',
    'color:#999': 'color-dim',
    'color:#aaa': 'color-muted',
    'color:#ccc': 'color-light',
    'color:#ce93d8': 'color-purple',
    'color:#e57373': 'color-red',
    'color:#ffb74d': 'color-orange',
    'color:#fff': 'color-white',
    'color:var(--accent)': 'color-accent',
    'color:var(--accent2)': 'color-green',
    'color:var(--accent3)': 'color-orange',
    'color:var(--accent4)': 'color-red',
}

BORDER_COLOR_MAP = {
    'border-color:#999': 'border-dim',
    'border-color:#ce93d8': 'border-purple',
    'border-color:var(--accent)': 'border-accent',
    'border-color:var(--accent2)': 'border-green',
    'border-color:var(--accent3)': 'border-orange',
    'border-color:var(--accent4)': 'border-red',
}

# Combined classes for common combinations
COMBINED_MAP = {
    ('font-size:0.65em', 'color:#aaa'): 'text-sm-muted',
    ('font-size:0.65em', 'color:#ccc'): 'text-sm-light',
    ('font-size:0.6em', 'color:#aaa'): 'text-060-muted',
    ('font-size:0.7em', 'color:#999'): 'text-070-dim',
    ('font-size:0.7em', 'color:#ccc'): 'text-070-light',
    ('font-size:0.75em', 'color:#ccc'): 'text-base-dim',
    ('font-size:0.8em', 'color:#999'): 'text-080-dim',
    ('font-size:0.8em', 'color:#aaa'): 'text-080-muted',
    ('font-size:0.8em', 'color:#ccc'): 'text-080-light',
    ('font-size:0.9em', 'color:#ccc'): 'text-lg-dim',
    ('font-size:0.55em', 'color:#aaa'): 'text-xs-muted',
    ('font-size:1.1em', 'color:var(--accent)'): 'text-110-accent',
    ('font-size:1.3em', 'color:#999'): 'text-130-dim',
}

def parse_style_attr(style_str):
    """Parse style attribute into dict of properties."""
    props = {}
    for prop in style_str.split(';'):
        prop = prop.strip()
        if ':' in prop:
            key, value = prop.split(':', 1)
            props[key.strip()] = value.strip()
    return props

def props_to_style_str(props):
    """Convert props dict back to style string."""
    if not props:
        return ''
    return '; '.join(f'{k}:{v}' for k, v in props.items()) + ';'

def replace_inline_styles(html_content):
    """Replace inline font-size and color styles with CSS classes."""

    def replace_style(match):
        tag_start = match.group(1)  # Everything before style attribute
        style_content = match.group(2)  # The style attribute content
        tag_end = match.group(3)  # Everything after style attribute

        # Parse existing style properties
        style_props = parse_style_attr(style_content)

        # Extract font-size, color, and border-color
        font_size = None
        color = None
        border_color = None
        if 'font-size' in style_props:
            font_size = f"font-size:{style_props['font-size']}"
        if 'color' in style_props:
            color = f"color:{style_props['color']}"
        if 'border-color' in style_props:
            border_color = f"border-color:{style_props['border-color']}"

        # Determine CSS classes to add
        css_classes = []

        # Check for combined class first
        if font_size and color:
            combined_key = (font_size, color)
            if combined_key in COMBINED_MAP:
                css_classes.append(COMBINED_MAP[combined_key])
                # Remove both properties
                del style_props['font-size']
                del style_props['color']
            else:
                # Add individual classes
                if font_size in FONT_SIZE_MAP:
                    css_classes.append(FONT_SIZE_MAP[font_size])
                    del style_props['font-size']
                if color in COLOR_MAP:
                    css_classes.append(COLOR_MAP[color])
                    del style_props['color']
        else:
            # Add individual classes
            if font_size and font_size in FONT_SIZE_MAP:
                css_classes.append(FONT_SIZE_MAP[font_size])
                del style_props['font-size']
            if color and color in COLOR_MAP:
                css_classes.append(COLOR_MAP[color])
                del style_props['color']

        # Handle border-color
        if border_color and border_color in BORDER_COLOR_MAP:
            css_classes.append(BORDER_COLOR_MAP[border_color])
            del style_props['border-color']

        # Build the replacement
        result = tag_start

        # Add CSS classes to existing class attribute or create new one
        if css_classes:
            # Check if there's already a class attribute
            class_match = re.search(r'class="([^"]*)"', tag_start)
            if class_match:
                existing_classes = class_match.group(1)
                new_classes = existing_classes + ' ' + ' '.join(css_classes)
                result = tag_start.replace(f'class="{existing_classes}"', f'class="{new_classes}"')
            else:
                # Add class attribute before style
                result = tag_start + f' class="{" ".join(css_classes)}"'

        # Add remaining style properties if any
        remaining_style = props_to_style_str(style_props)
        if remaining_style:
            result += f' style="{remaining_style}"'

        result += tag_end
        return result

    # Pattern to match style attributes
    # Captures: (tag start with potential class) style="(content)" (tag end)
    pattern = r'(<[^>]*?)\s*style="([^"]*)"([^>]*>)'

    # Replace all matches
    result = re.sub(pattern, replace_style, html_content)

    return result

def clean_empty_styles(html_content):
    """Remove empty style attributes."""
    return re.sub(r'\s*style=""\s*', ' ', html_content)

def clean_duplicate_classes(html_content):
    """Remove duplicate classes in class attributes."""
    def dedupe_classes(match):
        classes = match.group(1).split()
        unique_classes = []
        seen = set()
        for cls in classes:
            if cls not in seen:
                unique_classes.append(cls)
                seen.add(cls)
        return f'class="{" ".join(unique_classes)}"'

    return re.sub(r'class="([^"]*)"', dedupe_classes, html_content)

def process_file(filepath):
    """Process a single HTML file."""
    print(f"Processing {filepath.name}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count initial inline styles
    initial_count = len(re.findall(r'style="[^"]*(?:font-size|color|border-color)[^"]*"', content))

    # Replace inline styles
    content = replace_inline_styles(content)
    content = clean_empty_styles(content)
    content = clean_duplicate_classes(content)

    # Count remaining inline styles
    final_count = len(re.findall(r'style="[^"]*(?:font-size|color|border-color)[^"]*"', content))

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Replaced {initial_count - final_count} inline styles ({final_count} remaining)")
    return initial_count - final_count, final_count

def main():
    # Get all session HTML files
    presentation_dir = Path(__file__).parent
    html_files = sorted(presentation_dir.glob('session*.html'))

    if not html_files:
        print("No session HTML files found!")
        return 1

    total_replaced = 0
    total_remaining = 0

    for filepath in html_files:
        replaced, remaining = process_file(filepath)
        total_replaced += replaced
        total_remaining += remaining

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total inline styles replaced: {total_replaced}")
    print(f"  Total inline styles remaining: {total_remaining}")
    print(f"{'='*60}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
