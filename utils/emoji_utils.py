import os
import re

emoji_pattern = re.compile(r'([\U0001F000-\U0010ffff])', flags=re.UNICODE)

def split_with_emojis(text):
    result = []
    buffer = ""
    for char in text:
        if emoji_pattern.match(char):
            if buffer:
                result.append(("text", buffer))
                buffer = ""
            result.append(("emoji", char))
        else:
            buffer += char
    if buffer:
        result.append(("text", buffer))
    return result


def emoji_to_filename(char):
    base = "-".join(f"{ord(c):x}" for c in char).lower()
    filename = base + ".png"

    fallback = None
    if "-fe0f" in base:
        fallback = base.replace("-fe0f", "") + ".png"
    else:
        fallback = base + "-fe0f.png"

    # ищем в обеих версиях
    path1 = os.path.join("assets/ios_emoji", filename)
    path2 = os.path.join("assets/ios_emoji", fallback)

    if os.path.exists(path1):
        return filename
    elif os.path.exists(path2):
        return fallback
    else:
        return None  # или return "placeholder.png"
