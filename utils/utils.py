from tkinter import font

import pygame
from pygame import Surface, Rect
from pygame.font import Font, SysFont

from algorithm.class_matchmaking.matchmaking import Layout


def get_dynamic_font(
    max_width: int, max_height: int, text: str, font_type: str, max_font_size: int
) -> Font:
    low = 1
    high = max_font_size

    while low < high:
        font_size = (low + high) // 2
        font = SysFont(font_type, font_size)

        width, height = font.size(text)

        if width > max_width or height > max_height:
            high = font_size - 1
        else:
            low = font_size + 1

    return font


def lowest_font(text_data: list[tuple[int, int, str, str, int]]) -> Font:
    fonts = (get_dynamic_font(*data) for data in text_data)
    return min(fonts, key=lambda font: font.get_height())


def gradientRect(
    left_colour: tuple[int, int, int],
    right_colour: tuple[int, int, int],
    target_rect: Rect,
) -> tuple[Surface, Rect]:
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(
        colour_rect, (target_rect.width, target_rect.height)
    )
    return colour_rect, target_rect


def create_gradient(
    colors: list[tuple[int, int, int]], window_width: int, window_height: int
) -> tuple[Surface, int]:
    width, height = window_width // 2, window_height
    gradient = pygame.Surface((width * (len(colors) - 1), height))
    for i in range(len(colors) - 1):
        gradient.blit(
            *gradientRect(
                colors[i], colors[i + 1], pygame.Rect(i * width, 0, width, height)
            )
        )
    return gradient, width


def amount_of_valid_seats(layout: Layout) -> int:
    res = 0

    for 
