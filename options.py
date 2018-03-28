# -*- coding: utf-8 -*-

"""
Module Option:
    used for menus.
"""
import sys
from os.path import join as pathjoin
from os.path import abspath

import pygame


class Option:
    """
    Class for the menu button, with mouse hovering.
    """
    hover = False

    def __init__(self, text, pos, screen, func):
        self.text = text
        self.pos = pos
        self.font = pygame.font.Font(
            rsrc_path('./font/electroharmonix.ttf'), 40)
        self.screen = screen
        self.set_surf()
        self.draw()
        self.func = func

    def draw(self):
        """
        Display texts.
        """
        self.render = self.font.render(self.text, True, self.get_color())
        self.screen.blit(self.render, self.surf)

    def get_color(self):
        """
        Return color of text, if mouse is on or not.
        """
        if self.hover:
            return (232, 95, 137)
        else:
            return (0, 0, 0)

    def set_surf(self):
        """
        Transform text in Surface()
        """
        self.render = self.font.render(self.text, True, self.get_color())
        self.surf = self.render.get_rect()
        self.surf.bottomright = self.pos


def rsrc_path(relative_path):
    """Used for pyinstaller."""
    if hasattr(sys, '_MEIPASS'):
        return pathjoin(sys._MEIPASS, relative_path)
    return pathjoin(abspath('./'), relative_path)
