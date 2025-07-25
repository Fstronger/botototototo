from PIL import ImageFont

def get_font(size):
    try:
        return ImageFont.truetype("assets/fonts/Noah-BoldItalic.ttf", size)
    except Exception as e:
        print(f"[Ошибка загрузки шрифта] {e}")
        return ImageFont.load_default()