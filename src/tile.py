import pygame
GRAY = (180, 180, 180)
class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, size, color=GRAY):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update_position(self, camera, size):
        wx = self.grid_x * size
        wy = self.grid_y * size
        sx, sy = camera.transform_coordinate((wx, wy))
        self.rect.topleft = (sx, sy)

        
class AssetTile(Tile):
    def __init__(self, grid_x, grid_y, size, color=(150, 150, 150),
                 material="concreto", estructura="sólida", 
                 masa=0.0, volumen=0.0, costo=0.0, 
                 resistencia=0.0, radiacion=0.0, 
                 tiempo_almacenamiento=0.0, muestras=1):
        super().__init__(grid_x, grid_y, size, color)
        self.material = material
        self.estructura = estructura
        self.masa = masa
        self.volumen = volumen
        self.costo = costo
        self.resistencia = resistencia
        self.radiacion = radiacion
        self.tiempo_almacenamiento = tiempo_almacenamiento
        self.muestras = muestras

        # --- Aplica transparencia inicial ---
        self.update_alpha_by_resistencia()

    def update_alpha_by_resistencia(self):
        """Cambia la transparencia (alpha) del tile según la resistencia."""
        alpha = max(50, min(255, int(self.resistencia * 255)))
        self.image.set_alpha(alpha)