import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def transform_coordinate(self, pos):
        world_x, world_y = pos
        return world_x - self.x, world_y - self.y


class Player:
    def __init__(self, x, y, tile_size, color=(50, 200, 100)):
        self.grid_pos = [x, y]
        self.color = color
        self.camera = Camera()
        self._tile_size = tile_size
        self.selected_tile_type = None  # ← tipo actual de tile seleccionado
        self._actions = {
            113: "add_tile",     # key Q
            101: "remove_tile"   # key E
        }
        self.action = "add_tile"

        self.image = pygame.Surface((self._tile_size, self._tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.hover_rect = pygame.Rect(0, 0, tile_size, tile_size)
        self.hover_visible = False


    def change_action(self, key_pressed):
        if key_pressed in self._actions:
            self.action = self._actions[key_pressed]
            print(f"Current action changed to: {self.action}")

    def execute_action(self, world, mouse_pos, mouse_button):
        wx, wy = mouse_pos[0] + self.camera.x, mouse_pos[1] + self.camera.y
        gx, gy = int(wx // world.tile_size), int(wy // world.tile_size)

        if mouse_button == 1:
            if self.action == "add_tile":
                world.add_tile(gx, gy, self.selected_tile_type )
                print("SE AGREGO")
            elif self.action == "remove_tile":
                world.remove_tile(gx, gy)
    def update_hover(self, mouse_pos, topbar_height):
        """Actualiza la posición del tile de previsualización (hover)."""
        mx, my = mouse_pos

        # No mostrar si el mouse está sobre el TopBar o no hay tile seleccionado
        if my <= topbar_height or self.selected_tile_type is None:
            self.hover_visible = False
            return

        wx, wy = mx + self.camera.x, my + self.camera.y
        gx, gy = int(wx // self._tile_size), int(wy // self._tile_size)
        sx, sy = gx * self._tile_size - self.camera.x, gy * self._tile_size - self.camera.y

        # Actualizar la posición del rectángulo del hover
        self.hover_rect.topleft = (sx, sy)
        self.hover_visible = True

    # ======================================================
    #                 DIBUJAR TILE HOVER
    # ======================================================
    def draw_hover(self, surface):
        if self.hover_visible and self.selected_tile_type:
            hover_img = self.selected_tile_type.copy()
            hover_img.set_alpha(120)  # hace semitransparente
            surface.blit(hover_img, self.hover_rect)

    def update_position(self, keys):
        self.camera.move(keys)

    def get_world_position(self):
        return self.grid_pos[0] * self._tile_size, self.grid_pos[1] * self._tile_size

    def draw(self, surface):
        x, y = self.get_world_position()
        x, y = self.camera.transform_coordinate((x, y))
        rect = pygame.Rect(x, y, self._tile_size, self._tile_size)
        pygame.draw.rect(surface, self.color, rect)
