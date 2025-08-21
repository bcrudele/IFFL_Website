import re

# Predefined gradient options
GRADIENTS = {
    "bronze": 'linear-gradient(90deg, #cd7f32, #b87333)',
    "silver": 'linear-gradient(90deg, #c0c0c0, #dcdcdc)',
    "gold": 'linear-gradient(90deg, #ffd700, #f9a602)',
    "purple": 'linear-gradient(90deg, #a64ca6, #8431d9)',
    "special": 'linear-gradient(90deg, #ff9966, #ff5e62)',
}

def get_matches(content):
    return list(re.finditer(
        r'(<div[^>]*style="[^"]*?background:\s*#eee[^"]*?">\s*<div[^>]*?style="[^"]*?background:\s*linear-gradient\(90deg,[^;]+)',
        content
    ))

def apply_gradient(filename, style, match_filter):
    if style not in GRADIENTS:
        print(f"Invalid style '{style}'. Options are: {', '.join(GRADIENTS.keys())}")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = get_matches(content)
    if not matches:
        print("No progress bars found.")
        return

    updated_content = content
    updated_count = 0
    for match in reversed(matches):
        # Look behind the match to find nearby text content for filtering
        context = content[max(0, match.start() - 500):match.start()]
        if match_filter.lower() in context.lower():
            original = match.group(0)
            replaced = re.sub(
                r'background:\s*linear-gradient\(90deg,[^;]+',
                f'background: {GRADIENTS[style]}',
                original
            )
            updated_content = (
                updated_content[:match.start()] + replaced + updated_content[match.end():]
            )
            updated_count += 1

    if updated_count == 0:
        print(f"No matching progress bars found containing '{match_filter}'.")
        return

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Applied '{style}' gradient to {updated_count} matching progress bars in '{filename}'.")

def main():
    print("=== Progress Bar Styler ===\n")
    filename = input("Enter HTML filename (e.g., page.html): ").strip()
    print("Available styles: " + ", ".join(GRADIENTS.keys()))
    style = input("Enter gradient style: ").strip().lower()
    match_filter = input("Enter filter text to select specific progress bars (e.g., Duelist): ").strip()

    apply_gradient(filename, style, match_filter)

if __name__ == "__main__":
    main()
