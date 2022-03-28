from pygame.font import Font


def get_dynamic_font(
    max_width: int, max_height: int, text: str, font_type: str, max_font_size: int
) -> Font:
    low = 1
    high = max_font_size

    while low < high:
        font_size = (low + high) // 2
