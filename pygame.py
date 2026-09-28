import pygame
import sys
import random

pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulacion Bomberman - UNIDAD 2")
reloj = pygame.time.Clock()

# Constantes del juego
TAM_TILE = 40
FILAS = ALTO // TAM_TILE
COLUMNAS = ANCHO // TAM_TILE

# Colores y temas para los mapas (Tomando de base los colores originales)
TEMAS = {
    1: {'fondo': (166, 132, 255), 'muro': (100, 100, 150), 'bloque': (200, 150, 100)},
    2: {'fondo': (30, 80, 30), 'muro': (20, 20, 20), 'bloque': (150, 150, 150)},
    3: {'fondo': (50, 50, 50), 'muro': (255, 0, 0), 'bloque': (0, 255, 255)}
}

def generar_mapa():
    """Genera una cuadrícula: 0=Vacío, 1=Muro Fijo, 2=Bloque Destructible"""
    nuevo_mapa = []
    for f in range(FILAS):
        fila = []
        for c in range(COLUMNAS):
            # Bordes del mapa
            if f == 0 or f == FILAS - 1 or c == 0 or c == COLUMNAS - 1:
                fila.append(1)
            # Pilares intercalados (típico de Bomberman)
            elif f % 2 == 0 and c % 2 == 0:
                fila.append(1)
            # Zona segura inicial para el jugador (esquina superior izquierda)
            elif (f in [1, 2] and c in [1, 2]):
                fila.append(0)
            else:
                # Probabilidad de generar un bloque rompible
                fila.append(2 if random.random() < 0.6 else 0)
        nuevo_mapa.append(fila)
    return nuevo_mapa

# Variables del estado del juego
mapa_actual = 1
matriz_mapa = generar_mapa()

# Jugador (X, Y en píxeles, Ancho, Alto)
jugador = pygame.Rect(45, 45, 30, 30)
vel_jugador = 4

# Listas para gestionar bombas y explosiones
bombas = []
explosiones = []
RADIO_EXPLOSION = 1 # Alcance de la bomba en bloques

def colisiona_con_entorno(rect):
    """Verifica si el rectángulo del jugador choca con un muro (1) o bloque (2)"""
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if matriz_mapa[f][c] in [1, 2]:
                bloque_rect = pygame.Rect(c * TAM_TILE, f * TAM_TILE, TAM_TILE, TAM_TILE)
                if rect.colliderect(bloque_rect):
                    return True
    return False

def explotar_bomba(bomba):
    cx, cy = bomba['c'], bomba['f']
    # El centro explota
    explosiones.append({'f': cy, 'c': cx, 'tiempo': pygame.time.get_ticks()})
    
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in direcciones:
        for i in range(1, RADIO_EXPLOSION + 1):
            nx, ny = cx + (dx * i), cy + (dy * i)
            if matriz_mapa[ny][nx] == 1:
                break # El fuego choca contra muro indestructible y no avanza
            elif matriz_mapa[ny][nx] == 2:
                # Rompe el bloque y la explosión se detiene ahí
                matriz_mapa[ny][nx] = 0
                explosiones.append({'f': ny, 'c': nx, 'tiempo': pygame.time.get_ticks()})
                break
            elif matriz_mapa[ny][nx] == 0:
                # El fuego avanza por espacio vacío
                explosiones.append({'f': ny, 'c': nx, 'tiempo': pygame.time.get_ticks()})

ejecutar = True
while ejecutar:
    tiempo_actual = pygame.time.get_ticks()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutar = False
            
        if evento.type == pygame.KEYDOWN:
            # Cambiar mapas y regenerar el nivel con las teclas 1, 2 y 3
            if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                if evento.key == pygame.K_1: mapa_actual = 1
                if evento.key == pygame.K_2: mapa_actual = 2
                if evento.key == pygame.K_3: mapa_actual = 3
                matriz_mapa = generar_mapa()
                jugador.x, jugador.y = 45, 45 # Reiniciar posición
                bombas.clear()
                explosiones.clear()
                
            # Colocar bomba con la Barra Espaciadora
            if evento.key == pygame.K_SPACE:
                col_bomba = (jugador.x + jugador.width // 2) // TAM_TILE
                fila_bomba = (jugador.y + jugador.height // 2) // TAM_TILE
                bombas.append({'c': col_bomba, 'f': fila_bomba, 'tiempo': tiempo_actual})

    # --- MOVIMIENTO Y COLISIONES DEL JUGADOR ---
    teclas = pygame.key.get_pressed()
    
    # Movimiento en X
    if teclas[pygame.K_LEFT]:
        jugador.x -= vel_jugador
        if colisiona_con_entorno(jugador):
            jugador.x += vel_jugador # Cancela si colisiona
            
    if teclas[pygame.K_RIGHT]:
        jugador.x += vel_jugador
        if colisiona_con_entorno(jugador):
            jugador.x -= vel_jugador # Cancela si colisiona

    # Movimiento en Y
    if teclas[pygame.K_UP]:
        jugador.y -= vel_jugador
        if colisiona_con_entorno(jugador):
            jugador.y += vel_jugador # Cancela si colisiona
            
    if teclas[pygame.K_DOWN]:
        jugador.y += vel_jugador
        if colisiona_con_entorno(jugador):
            jugador.y -= vel_jugador # Cancela si colisiona

    # --- ACTUALIZAR BOMBAS Y EXPLOSIONES ---
    bombas_restantes = []
    for b in bombas:
        if tiempo_actual - b['tiempo'] > 2000: # Explotan tras 2 segundos
            explotar_bomba(b)
        else:
            bombas_restantes.append(b)
    bombas = bombas_restantes

    # Las explosiones duran 300 milisegundos en pantalla
    explosiones = [e for e in explosiones if tiempo_actual - e['tiempo'] < 300]

    # --- DIBUJAR PANTALLA ---
    tema = TEMAS[mapa_actual]
    pantalla.fill(tema['fondo']) 
    
    # Dibujar mapa (Muros indestructibles y bloques rompibles)
    for f in range(FILAS):
        for c in range(COLUMNAS):
            x, y = c * TAM_TILE, f * TAM_TILE
            if matriz_mapa[f][c] == 1:
                pygame.draw.rect(pantalla, tema['muro'], (x, y, TAM_TILE, TAM_TILE))
            elif matriz_mapa[f][c] == 2:
                pygame.draw.rect(pantalla, tema['bloque'], (x, y, TAM_TILE, TAM_TILE))
                # Borde negro para distinguir los bloques rompibles
                pygame.draw.rect(pantalla, (0, 0, 0), (x, y, TAM_TILE, TAM_TILE), 2)

    # Dibujar Bombas
    for b in bombas:
        bx = b['c'] * TAM_TILE + TAM_TILE // 2
        by = b['f'] * TAM_TILE + TAM_TILE // 2
        radio = 12 if (tiempo_actual // 200) % 2 == 0 else 15 # Efecto latido
        pygame.draw.circle(pantalla, (0, 0, 0), (bx, by), radio)

    # Dibujar Explosiones
    for e in explosiones:
        ex = e['c'] * TAM_TILE
        ey = e['f'] * TAM_TILE
        pygame.draw.rect(pantalla, (255, 150, 0), (ex, ey, TAM_TILE, TAM_TILE))
        pygame.draw.rect(pantalla, (255, 255, 0), (ex + 5, ey + 5, TAM_TILE - 10, TAM_TILE - 10))

    # Dibujar Jugador
    pygame.draw.rect(pantalla, (50, 50, 200), jugador)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
