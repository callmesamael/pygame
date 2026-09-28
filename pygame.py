import pygame
import sys

pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulacion de mi pantalla - UNIDAD 2")

reloj = pygame.time.Clock()

# Variable para controlar qué mapa estamos viendo (empieza en el mapa 1)
mapa_actual = 1

ejecutar = True
while ejecutar:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutar = False
        
        # Detectar cuando se presiona una tecla para cambiar de mapa
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                mapa_actual = 1
            elif evento.key == pygame.K_2:
                mapa_actual = 2
            elif evento.key == pygame.K_3:
                mapa_actual = 3

    # -(MOCKUPS)
    
    if mapa_actual == 1:
        # MAPA 1: Fondo Lila con un cuadrado azul y un círculo blanco
        pantalla.fill((166, 132, 255)) 
        
        # Figuras por dentro (Mockup de interfaz o nivel 1)
        pygame.draw.rect(pantalla, (50, 50, 200), (100, 100, 600, 400), 5) # Borde/Marco
        pygame.draw.circle(pantalla, (255, 255, 255), (400, 300), 50)     # Círculo central
        
    elif mapa_actual == 2:
        # MAPA 2: Fondo Verde Oscuro con mockups de plataformas o cajas
        pantalla.fill((30, 80, 30)) 
        
        # Figuras por dentro (Simulando suelo y obstáculos)
        pygame.draw.rect(pantalla, (200, 100, 50), (0, 500, 800, 100))    # Suelo/Tierra
        pygame.draw.rect(pantalla, (150, 150, 150), (200, 350, 150, 50))  # Plataforma flotante
        pygame.draw.rect(pantalla, (150, 150, 150), (500, 250, 150, 50))  # Otra plataforma
        
    elif mapa_actual == 3:
        # MAPA 3: Fondo Gris con diseño de laberinto o rejilla
        pantalla.fill((50, 50, 50)) 
        
        # Figuras por dentro (Líneas simulando paredes o cuadrícula)
        pygame.draw.line(pantalla, (255, 0, 0), (100, 0), (100, 600), 8)   # Pared roja izquierda
        pygame.draw.line(pantalla, (255, 0, 0), (700, 0), (700, 600), 8)   # Pared roja derecha
        pygame.draw.circle(pantalla, (0, 255, 255), (400, 150), 30)        # Meta/Objetivo celeste

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()