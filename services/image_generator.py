import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils.emoji_utils import split_with_emojis, emoji_to_filename
from utils.fonts import get_font

IMG_SIZE = 512
PADDING = 40              # внешний отступ от краёв
BLOCK_PADDING = 24        # внутренний отступ внутри плашки
LINE_SPACING = 4
FONT_SIZE = 24
EMOJI_SIZE = 24
EMOJI_PATH = "assets/ios_emoji"

async def generate_quote_image(update, context):
    msg = update.message
    replied = msg.reply_to_message
    user = replied.from_user
    text = replied.text or "<медиа>"
    author_text = f"© {user.full_name}"

    bg = await get_blurred_avatar(user.id, context, update.effective_chat)
    font = get_font(FONT_SIZE)
    author_font = get_font(22)
    draw = ImageDraw.Draw(bg)

    text_area_width = IMG_SIZE - 2 * (PADDING + BLOCK_PADDING)
    wrapped_lines = wrap_with_emojis(text, font, text_area_width, draw)

    total_height = len(wrapped_lines) * (FONT_SIZE + LINE_SPACING) + 40
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    total_height += author_bbox[3] - author_bbox[1]
    y = (IMG_SIZE - total_height) // 2

    # Плашка
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [PADDING, y - 20, IMG_SIZE - PADDING, y + total_height + 20],
        radius=20,
        fill=(0, 0, 0, 100)
    )
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)

    # Текст
    for line in wrapped_lines:
        line_width = sum(draw.textlength(val, font=font) if kind == "text" else EMOJI_SIZE for kind, val in line)
        x = PADDING + BLOCK_PADDING + (text_area_width - line_width) // 2
        for kind, val in line:
            if kind == "text":
                draw.text((x + 1, y + 1), val, font=font, fill="black")
                draw.text((x, y), val, font=font, fill="white")
                x += draw.textlength(val, font=font)
            else:
                filename = emoji_to_filename(val)
                if filename:
                    path = os.path.join(EMOJI_PATH, filename)
                    if os.path.exists(path):
                        emoji_img = Image.open(path).convert("RGBA").resize((EMOJI_SIZE, EMOJI_SIZE))
                        bg.paste(emoji_img, (int(x), int(y + 4)), emoji_img)
                x += EMOJI_SIZE
        y += FONT_SIZE + LINE_SPACING

    # Автор
    y += 40
    w = draw.textlength(author_text, font=author_font)
    draw.text(((IMG_SIZE - w) // 2 + 1, y + 1), author_text, font=author_font, fill="black")
    draw.text(((IMG_SIZE - w) // 2, y), author_text, font=author_font, fill="white")

    output = io.BytesIO()
    bg.save(output, format="PNG")
    output.seek(0)
    return output


async def get_blurred_avatar(user_id, context, chat):
    try:
        photos = await context.bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            file = await context.bot.get_file(photos.photos[0][-1].file_id)
            img_bytes = await file.download_as_bytearray()
            return Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((IMG_SIZE, IMG_SIZE)).filter(ImageFilter.GaussianBlur(12))
    except:
        pass

    try:
        if chat.photo:
            file = await context.bot.get_file(chat.photo.big_file_id)
            img_bytes = await file.download_as_bytearray()
            return Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((IMG_SIZE, IMG_SIZE)).filter(ImageFilter.GaussianBlur(12))
    except:
        pass

    return Image.new("RGB", (IMG_SIZE, IMG_SIZE), (70, 70, 70))


def wrap_with_emojis(text, font, max_width, draw):
    lines = []
    for raw_line in text.splitlines():  # учитываем ручные переносы
        parts = split_with_emojis(raw_line)
        current_line, width = [], 0
        for kind, val in parts:
            if kind == "text":
                for char in val:
                    char_width = draw.textlength(char, font=font)
                    if width + char_width > max_width:
                        lines.append(current_line)
                        current_line = []
                        width = 0
                    current_line.append((kind, char))
                    width += char_width
            else:
                if width + EMOJI_SIZE > max_width:
                    lines.append(current_line)
                    current_line = []
                    width = 0
                current_line.append((kind, val))
                width += EMOJI_SIZE
        if current_line:
            lines.append(current_line)
    return lines
