#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The project is an implementation of the game Gomoku Ninuki.

With artificial intelligence (AI) capable of winning.
"""
import sys

import gameplay
import pygame
from options import Option, rsrc_path

__author__ = "Zackary Beaugelin"
__contact__ = "beaug001@cougars.csusm.edu"
__copyright__ = "Copyright 2018, Zackary Beaugelin"
__credits__ = ["Zackary Beaugelin"]
__date__ = "2018/03/28"
__deprecated__ = False
__email__ = "beaug001@cougars.csusm.edu"
__license__ = "GPLv3"
__maintainer__ = "Zackary Beaugelin"
__status__ = "Production"
__version__ = "1.0.0"


class Launcher:
    """
    Class allowing pygame to load.
    """
    pygame.init()
    pygame.display.set_caption('Gomoku')
    pygame.display.set_icon(pygame.image.load(rsrc_path('./img/ico.png')))

    def __init__(self):
        self.screen = pygame.display.set_mode((770, 770))
        self.options = [
            Option("Player VS Player", (750, 430), self.screen,
                   gameplay.load_p_vs_p),
            Option("Player VS IA", (750, 480), self.screen,
                   gameplay.load_p_vs_ai),
            Option("Quit", (750, 750), self.screen, gameplay.r_false)
        ]

    def launch(self):
        """
        Create the menu, launch the corresponding gamemode.
        """
        run = True
        while run:
            pygame.event.pump()
            background = pygame.image.load(rsrc_path('./img/MenuBG.jpg'))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                for option in self.options:
                    if option.surf.collidepoint(pygame.mouse.get_pos()):
                        option.hover = True
                        if (event.type == pygame.MOUSEBUTTONDOWN
                                and event.button == 1):
                            run = option.func(self.screen)
                    else:
                        option.hover = False
                    option.draw()
            for option in self.options:
                option.hover = bool(
                    option.surf.collidepoint(pygame.mouse.get_pos()))
                option.draw()
            pygame.display.update()

    def exit(self):
        """
        Exit.
        """
        _ = self
        pygame.quit()
        return 0


if __name__ == '__main__':
    __game__ = Launcher()
    __game__.launch()
    sys.exit(__game__.exit())
