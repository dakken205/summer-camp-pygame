import pygame
from pygame import Surface, Rect

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 600

screen_size = min(screen_width, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platform")

tile_size = screen_size // 20
game_over = 0
main_menu = True

# fmt: off
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 2, 0, 2, 2, 2, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1], 
[1, 2, 2, 2, 2, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# fmt: on
bg_img = pygame.transform.scale(
    pygame.image.load("img/sky.png"), (screen_width, screen_height)
)
restart_img = pygame.transform.scale(
    pygame.image.load("img/restart_btn.png"),
    (screen_size * 0.3, screen_size * 0.1),
)
start_img = pygame.transform.scale(
    pygame.image.load("img/start_btn.png"),
    (screen_size * 0.2, screen_size * 0.1),
)
exit_img = pygame.transform.scale(
    pygame.image.load("img/exit_btn.png"),
    (screen_size * 0.2, screen_size * 0.1),
)

font = pygame.font.SysFont("Bauhaus 93", int(screen_size * 0.1))

blue = (0, 0, 255)


def draw_text(text, font: pygame.font.Font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def in_display(x, y):
    return 0 <= x < screen_width and 0 <= y < screen_height


def in_world(x, now):
    return 0 <= x < now + ((screen_width - tile_size) / 2)


def draw_grid():
    for line in range(int(20 * (screen_width / screen_height))):
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (0, (line + 1) * tile_size),
            (screen_width, (line + 1) * tile_size),
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            ((line + 1) * tile_size, 0),
            ((line + 1) * tile_size, screen_height),
        )


class Button:
    def __init__(self, x, y, image: Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
        img_r = pygame.image.load("img/player_R.png")
        img_l = pygame.image.load("img/player_L.png")
        self.image_r = pygame.transform.scale(
            img_r, (screen_size * 0.04, screen_size * 0.08)
        )
        self.image_l = pygame.transform.scale(
            img_l, (screen_size * 0.04, screen_size * 0.08)
        )
        self.image = self.image_r
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.bg_x = x

    def update(self, game_over):
        dx = 0
        bg_dx = 0
        dy = 0

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False:
                self.vel_y = -int(screen_size * 0.025)
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if (
                self.rect.x <= (screen_width - tile_size) / 2
                or self.bg_x <= (screen_width - tile_size) / 2
            ):
                if key[pygame.K_RIGHT]:
                    dx += 5
                    bg_dx += 5
                    self.direction += 1
                if key[pygame.K_LEFT]:
                    self.direction -= 1
                    dx -= 5
                    bg_dx -= 5
                if (key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False) or (
                    key[pygame.K_RIGHT] and key[pygame.K_LEFT]
                ):
                    self.direction = 0
            else:
                if key[pygame.K_RIGHT]:
                    self.direction = 1
                    bg_dx += 5
                if key[pygame.K_LEFT]:
                    self.direction = -1
                    bg_dx -= 5
                if (key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False) or (
                    key[pygame.K_RIGHT] and key[pygame.K_LEFT]
                ):
                    self.direction = 0

            # direction
            if self.direction == 1:
                self.image = self.image_r
            if self.direction == -1:
                self.image = self.image_l

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            for tile in world.tile_list_g:
                if tile[1].colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    dx = 0
                    bg_dx = 0
                if tile[1].colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            for tile in world.tile_list_p:
                if tile[1].colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    game_over = 1
                    dx = 0
                    bg_dx = 0
                    dy = 0
            for tile in world.tile_list_d:
                if tile[1].colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
                    game_over = -1
                    dx = 0
                    bg_dx = 0
                    dy = 0

            # update player coordinates
            if in_display(self.rect.x, self.rect.y):
                self.rect.x += dx
                self.rect.y += dy
            # else:
            #     self.rect.x -= dx
            #     self.rect.y -= dy

            self.bg_x += bg_dx

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

            return game_over
            # draw player onto screen
            # screen.blit(self.image, self.rect)
            # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        else:
            return game_over

    def draw(self):
        screen.blit(self.image, self.rect)

    def tile_x_y(self):
        map_x = self.bg_x - ((screen_width - tile_size) / 2)
        if map_x < 0:
            return 0
        else:
            return map_x


class World:
    def __init__(self, data, map_x):
        self.tile_list_g: list[tuple[Surface, Rect]] = []
        self.tile_list_p: list[tuple[Surface, Rect]] = []
        self.tile_list_d: list[tuple[Surface, Rect]] = []
        self.map_x = map_x

        # load images
        soil_img = pygame.image.load("img/soil.png")
        green_img = pygame.image.load("img/green.png")
        poll_img = pygame.image.load("img/goalpoll.png")
        ball_img = pygame.image.load("img/goalball.png")
        fall_img = pygame.image.load("img/death.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(soil_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - self.map_x
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list_g.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(green_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - self.map_x
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list_g.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(poll_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - self.map_x
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list_p.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(ball_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - self.map_x
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list_p.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(fall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size - self.map_x
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list_d.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list_g:
            screen.blit(tile[0], tile[1])
        for tile in self.tile_list_p:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


player = Player(tile_size * 2, screen_height - (tile_size * 13 / 5) + tile_size)

restart_button = Button(
    screen_width // 2 - int(screen_width * 0.15),
    screen_height // 2,
    restart_img,
)
start_button = Button(
    screen_width // 2 - int(screen_width * 0.35), screen_height // 2, start_img
)
exit_button = Button(
    screen_width // 2 + int(screen_width * 0.15), screen_height // 2, exit_img
)

run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world = World(world_data, player.tile_x_y())

        player.update(game_over)

        world.draw()

        draw_grid()

        player.draw()

        game_over = player.update(game_over)

        if game_over == -1:
            draw_text(
                "GAME OVER!",
                font,
                blue,
                (screen_width // 2) - int(screen_width * 0.2),
                screen_height // 2 - int(screen_height * 0.1),
            )
            if restart_button.draw():
                player = Player(
                    tile_size * 2, screen_height - (tile_size * 13 / 5) + tile_size
                )
                game_over = 0

        elif game_over == 1:
            draw_text(
                "CLEAR!",
                font,
                blue,
                (screen_width // 2) - int(screen_width * 0.14),
                screen_height // 2 - int(screen_height * 0.1),
            )
            if restart_button.draw():
                player = Player(
                    tile_size * 2, screen_height - (tile_size * 13 / 5) + tile_size
                )
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()

pygame.quit()
