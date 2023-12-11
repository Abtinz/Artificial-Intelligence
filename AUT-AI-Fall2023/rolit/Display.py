import pygame
from util import load_images
from copy import deepcopy
import sys

# Define colors
FOREST_GREEN = (144, 238, 144)
LIGHT_GREEN = (34, 139, 34)

FPS = 20

class Piece(pygame.sprite.Sprite):
    
    def __init__(self, images_dict, init_color, position, square_size=100):
        super(Piece, self).__init__()
        self.pos = position
        self.sprite_size = (square_size, square_size)
        self.square_size = square_size
        self.current_color = init_color

        self.images_dict = images_dict
        self.images = []
        self.index = 0
        self.image = self.images_dict[f'{self.current_color}_out'][0]

        self.rect = pygame.Rect(position[1] * self.square_size, position[0] * self.square_size, (position[1] + 1) * self.square_size, (position[0] + 1) * self.square_size)

    def update(self):
        
        if self.index < len(self.images):
            self.image = self.images[self.index]
            self.index += 1

    def change_color(self, color):
        prev_color = self.current_color
        self.current_color = color
        self.images = self.images_dict[f'{prev_color}_out'] + self.images_dict[f'{self.current_color}_in']
        self.index = 0

class Display:

    def initialize(self, board, players, steps_taken=0):
        pass

    def update(self, board):
        pass

class GraphicalDisplay(Display):

    def __init__(self, size=800) -> None:
        super(Display, self).__init__()
        self.screen = None
        self.size=size
        self.square_size = self.size // 8
        self.sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.images_dict, self.colors = load_images([lambda img: pygame.transform.scale(img, (self.square_size, self.square_size))])
        self.board = [[-1] * 8 for _ in range(8)]
        self.player_count = 2

    def initialize(self, board, players, steps_taken=0):
        pygame.init()
        self.player_count = players
    
        # Set up the Pygame window
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Rolit Board")

        # Introduce the players
        self.introduce_players()

        # Update the Pygame display
        self.update(board)

    def introduce_players(self):
        print(f'your color is {self.colors[0]}.')
        print('the rest of the players are:')
        for index in range(1, self.player_count):
            print(f'player #{index} is shown by the color {self.colors[index]}.')
        print()

    def draw_board(self):
        # Draw the board
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                if (row + col) % 2 == 0:
                    color = LIGHT_GREEN
                else:
                    color = FOREST_GREEN
                pygame.draw.rect(self.screen, color, [x, y, self.square_size, self.square_size])

    def compare_boards(self, new_board):

        new_sprites, changed_sprites = [], []
        for i in range(len(new_board)):
            for j in range(len(new_board[i])):

                if self.board[i][j] == new_board[i][j]: # if it has not changed, skip
                    continue

                if self.board[i][j] == -1: # was empty before but it is changed now
                    new_sprite = ((i, j), new_board[i][j])
                    new_sprites.append(new_sprite)

                elif new_board[i][j] == -1: # piece is removed, not possible but mentioned for clarity
                    continue

                else:
                    changed_sprite = ((i, j), new_board[i][j])
                    changed_sprites.append(changed_sprite)

        self.board = deepcopy(new_board)
        return new_sprites, changed_sprites

    def add_sprite(self, position, index):
        
        if index < len(self.colors):
            color = self.colors[index]
        else:
            print('wrong index! not enough colors in palette!')
            return
        
        new_piece = Piece(self.images_dict, color, position, square_size=self.square_size)
        self.sprites.add(new_piece)

    def update_sprite(self, position, index):

        if index < len(self.colors):
            color = self.colors[index]
        else:
            print('wrong index! not enough colors in palette!')
            return

        for sprite in self.sprites.sprites():
            if sprite.pos == position:
                sprite.change_color(color)
                break

    def update(self, board):
        new_sprites, changed_sprites = self.compare_boards(board)

        for (position, index) in new_sprites:
            self.add_sprite(position, index)
        
        for (position, index) in changed_sprites:
            self.update_sprite(position, index)

        for _ in range(10):
            self.draw_board()

            self.sprites.update()
            self.sprites.draw(self.screen)

            # Update the Pygame display
            pygame.display.update()

            self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class ConsoleDisplay(Display):

    def __init__(self) -> None:
        super().__init__()
        self.signs = {-1: '.', 0: 'B', 1: 'R', 2: 'Y', 3: 'G'}
        self.player_count = 1
        self.index = 0

    def initialize(self, board, player_count, steps_taken):
        self.index = steps_taken
        self.player_count = player_count
        self.introduce_players()
        self.update(board)

    def introduce_players(self):
        print(f'your character is {self.signs[0]}.')
        print('the rest of the players are:')
        for index in range(1, self.player_count):
            print(f'player #{index} is shown by the character {self.signs[index]}.')
        print()

    def print_turn(self):
        print(f'it is {self.signs[self.index % self.player_count]}\'s turn')
        
    def print_void(self):
        print("\n"*20)

    def print_board(self, board):
        def print_horizontal():
            for i in range(48):
                print(f'-', end="")
            print('-')
        print_horizontal()
        for i in range(len(board)):
            for j in range(len(board[i])):
                print(f'|{self.signs[board[i][j]].center(5)}', end="")
            print('|')
            print_horizontal()
        print()

    def update(self, board):
        
        if self.index % self.player_count == 0:
            self.print_void()

        self.print_turn()
        self.print_board(board)
        self.index += 1