import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, size, img):
        """
        Tile simple que recibe directamente una imagen ya cargada (pygame.Surface).
        """
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.image = pygame.transform.scale(img, (size, size))
        self.rect = self.image.get_rect()

    def update_position(self, camera, size):
        wx = self.grid_x * size
        wy = self.grid_y * size
        sx, sy = camera.transform_coordinate((wx, wy))
        self.rect.topleft = (sx, sy)


# ======================================================
#                  CLASE TILE EXTENDIDA
# ======================================================
class AssetTile(Tile):
    def __init__(self, grid_x, grid_y, size, img,
                 material="concreto", estructura="sólida",
                 masa=0.0, volumen=0.0, costo=0.0,
                 resistencia=0.0, radiacion=0.0,
                 tiempo_almacenamiento=0.0, muestras=1):
        """
        Tile extendido con propiedades físicas y visuales.
        Solo acepta una imagen ya cargada como 'img'.
        """
        super().__init__(grid_x, grid_y, size, img)

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
