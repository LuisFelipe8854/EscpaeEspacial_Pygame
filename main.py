import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Espacial")

# Cargar imágenes
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (60, 60))

# Cargar la fuente
font = pygame.font.Font("assets\PressStart2P-Regular.ttf", 18)
main_font = pygame.font.Font("assets\PressStart2P-Regular.ttf", 50)

# Cargar música de fondo
pygame.mixer.music.load("assets/background_music.mp3")  # Ruta al archivo de música
pygame.mixer.music.set_volume(1)  # Ajustar el volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproducir en bucle indefinido


# Posición inicial del jugador
player_pos = [WIDTH // 2, HEIGHT - 60]  # [x, y]
# velocidad del jugador
player_speed = 5

# Fuente para texto


# Función: Dibujar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect()
    rect.center = (x, y)
    surface.blit(textobj, rect)

import random

# Cargar imagen del enemigo
enemy_img = pygame.image.load("assets/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

# Lista para enemigos
enemigos = []
bullets = []



# Velocidad mínima y máxima de los enemigos
MIN_VELOCIDAD = 1
MAX_VELOCIDAD = 10
TIEMPO_MAXIMO = 300000  # 5 minutos en milisegundos

# Crear enemigos iniciales
def crear_enemigos(cantidad):
    for _ in range(cantidad):
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-600, -50)
        velocidad = MIN_VELOCIDAD  # Inicia con la velocidad mínima
        enemigos.append({"x": x, "y": y, "velocidad": velocidad})

# Modificar la función de mover y dibujar enemigos para detectar Game Over
# Modificar la función de mover y dibujar enemigos para detectar Game Over
def mover_dibujar_enemigos(tiempo_transcurrido):
    # Calcular la velocidad actual en función del tiempo transcurrido
    if tiempo_transcurrido > 0:  # Solo actualizar la velocidad si el tiempo transcurrido es mayor a 0
        factor_tiempo = min(tiempo_transcurrido / TIEMPO_MAXIMO, 1)  # Normaliza entre 0 y 1
        velocidad_actual = MIN_VELOCIDAD + factor_tiempo * (MAX_VELOCIDAD - MIN_VELOCIDAD)
    else:
        velocidad_actual = MIN_VELOCIDAD  # Usar la velocidad mínima al inicio del juego

    for enemigo in enemigos:
        if tiempo_transcurrido > 0:  # Solo mover enemigos si el tiempo transcurrido es mayor a 0
            enemigo["y"] += enemigo["velocidad"]
            enemigo["velocidad"] = velocidad_actual  # Actualiza la velocidad del enemigo

            # Si el enemigo cruza el borde inferior de la pantalla, termina el juego
            if enemigo["y"] > HEIGHT:
                game_over()
                return  # Salir de la función para reiniciar el juego

            # Detectar colisión con el jugador
            jugador_rect = pygame.Rect(player_pos[0], player_pos[1], player_img.get_width(), player_img.get_height())
            enemigo_rect = pygame.Rect(enemigo["x"], enemigo["y"], enemy_img.get_width(), enemy_img.get_height())
            if jugador_rect.colliderect(enemigo_rect):
                game_over()
                return  # Salir de la función para reiniciar el juego

        # Dibujar el enemigo
        screen.blit(enemy_img, (enemigo["x"], enemigo["y"]))

# Cargar sonido de disparo
shoot_sound = pygame.mixer.Sound("assets\Sounds\SoundShot.wav")  # Ruta al archivo de sonido
shoot_sound.set_volume(0.1)  # Ajustar el volumen (0.0 a 1.0)

# Función para disparar balas
def shoot_bullet(x, y):
    bullet = pygame.Rect(x + player_img.get_width() // 2 - 2, y, 4, 10)
    bullets.append(bullet)
    shoot_sound.play()  # Reproducir el sonido de disparo

# Menú principal
def main_menu():
    while True:
        # Dibujar el fondo (imagen)
        screen.blit(background_img, (0, 0))  # Dibujar la imagen de fondo
        draw_text("ESCAPE ESPACIAL", main_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Presiona ENTER para comenzar", font, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2)
        # Dibujar instrucciones adicionales
        draw_text("Presiona ESPACIO para disparar", font, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("y sobrevive lo más que puedas", font, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2 + 80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Sal del menú y empieza el juego

        pygame.display.update()


# Variable global para el puntaje
puntos = 0

# Función para calcular los puntos por colisión
def calcular_puntos(velocidad_enemigos):
    # El puntaje base es 15, y aumenta en +5 por cada incremento en la velocidad de los enemigos
    return 15 + int((velocidad_enemigos - MIN_VELOCIDAD) * 5)

# Función para dibujar el puntaje en pantalla
def dibujar_puntaje(puntos):
    texto_puntaje = f"Puntos: {puntos}"
    draw_text(texto_puntaje, font, (255, 255, 255), screen, 100, 30)  # Posición en la esquina superior izquierda

# Lista para animaciones de puntos
puntos_animaciones = []

# Función para dibujar las animaciones de puntos
def dibujar_puntos_animaciones():
    for animacion in puntos_animaciones[:]:
        texto, x, y, tiempo_creacion = animacion
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_creacion > 1000:  # Mostrar por 1 segundo
            puntos_animaciones.remove(animacion)
        else:
            draw_text(texto, font, (255, 255, 0), screen, x, y)

explosion_sound = pygame.mixer.Sound("assets\Sounds\SoundExplosionLarge.wav")  # Ruta al archivo de sonido
explosion_sound.set_volume(0.1)  # Ajustar el volumen (0.0 a 1.0)

# Modificar la función de colisión para reproducir el sonido
def colision_enemigo():
    global enemigos, bullets, puntos, puntos_animaciones
    for bullet in bullets[:]:
        for enemigo in enemigos[:]:
            # Crear un rectángulo para la bala y el enemigo
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            enemigo_rect = pygame.Rect(enemigo["x"], enemigo["y"], enemy_img.get_width(), enemy_img.get_height())
            
            # Detectar colisión
            if bullet_rect.colliderect(enemigo_rect):
                # Reproducir el sonido de explosión
                explosion_sound.play()

                # Eliminar la bala y el enemigo
                bullets.remove(bullet)
                enemigos.remove(enemigo)
                
                # Dibujar explosión
                pygame.draw.circle(screen, (255, 0, 0), (enemigo["x"] + 25, enemigo["y"] + 25), 30)
                pygame.display.update()

                # Calcular y actualizar los puntos
                velocidad_enemigos = enemigo["velocidad"]
                puntos_obtenidos = calcular_puntos(velocidad_enemigos)
                puntos += puntos_obtenidos

                # Agregar animación de puntos
                puntos_animaciones.append((f"+{puntos_obtenidos}", enemigo["x"] + 25, enemigo["y"] - 20, pygame.time.get_ticks()))

                # Crear un nuevo enemigo en una posición aleatoria
                x = random.randint(0, WIDTH - 50)
                y = random.randint(-600, -50)
                velocidad = random.randint(2, 5)
                enemigos.append({"x": x, "y": y, "velocidad": velocidad})

                break  # Sal del bucle interno para evitar errores

# Cargar imagen del fondo
background_img = pygame.image.load("assets/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

# Función para pausar el juego
def pausar_juego():
    pausado = True

    # Crear una superficie semitransparente
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Superficie del tamaño de la pantalla
    overlay.set_alpha(77)  # 30% de transparencia (255 * 0.3 ≈ 77)
    overlay.fill((0, 0, 0))  # Color negro semitransparente

    while pausado:
        # Dibujar el fondo del juego actual
        screen.blit(background_img, (0, 0))  # Redibujar el fondo
        # Dibujar todos los componentes del juego (jugador, enemigos, balas, etc.)
        screen.blit(player_img, (player_pos[0], player_pos[1]))
        mover_dibujar_enemigos(0)  # Dibujar enemigos sin moverlos
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)
        dibujar_puntaje(puntos)
        dibujar_puntos_animaciones()

        # Dibujar la superficie semitransparente
        screen.blit(overlay, (0, 0))

        # Dibujar el texto de pausa
        draw_text("PAUSA", main_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Presiona ENTER para continuar", font, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Reanudar el juego
                    pausado = False

        pygame.display.update()

# Cargar sonido de muerte
death_sound = pygame.mixer.Sound("assets/Sounds/GameOver.wav")  # Ruta al archivo de sonido
death_sound.set_volume(0.5)  # Ajustar el volumen (0.0 a 1.0)

# Función para reiniciar el estado del juego
def reiniciar_juego():
    global enemigos, bullets, player_pos, puntos, start_time
    enemigos.clear()  # Vaciar la lista de enemigos
    bullets.clear()  # Vaciar la lista de balas
    player_pos = [WIDTH // 2, HEIGHT - 60]  # Restablecer la posición del jugador
    puntos = 0  # Reiniciar el puntaje

    # Reiniciar el tiempo de inicio
    start_time = pygame.time.get_ticks()

    # Crear enemigos iniciales con velocidad mínima
    for _ in range(5):  # Cambia el número según la cantidad inicial de enemigos
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-600, -50)
        velocidad = MIN_VELOCIDAD  # Reiniciar la velocidad al valor mínimo
        enemigos.append({"x": x, "y": y, "velocidad": velocidad})

# Variable global para el puntaje máximo y el número de juegos
max_puntaje = 0
num_juegos = 0

# Función para mostrar la pantalla de Game Over
def game_over():
    global max_puntaje, puntos, num_juegos

    # Incrementar el número de juegos
    num_juegos += 1

    # Actualizar el puntaje máximo si el puntaje actual es mayor
    if puntos > max_puntaje:
        max_puntaje = puntos

    pygame.mixer.music.stop()  # Detener la música de fondo
    death_sound.play()  # Reproducir el sonido de muerte

    while True:
        # Dibujar el fondo
        screen.blit(background_img, (0, 0))

        # Mostrar texto de Game Over
        draw_text("GAME OVER", main_font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 4)
        draw_text(f"Tu puntaje fue: {puntos}", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2)

        # Mostrar el puntaje máximo solo si no es el primer juego
        if num_juegos > 1:
            draw_text(f"Máximo puntaje: {max_puntaje}", font, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2 + 50)

        draw_text("Presiona ENTER para empezar de nuevo", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 100)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Reiniciar el juego
                    reiniciar_juego()  # Reiniciar el estado del juego
                    pygame.mixer.music.play(-1)  # Reanudar la música de fondo
                    return  # Salir de la función para reiniciar el juego

        pygame.display.update()


# Bucle principal del juego
def game_loop():
    global player_pos, puntos, start_time
    running = True
    clock = pygame.time.Clock()

    reiniciar_juego()  # Asegurarse de que el juego comience con un estado limpio

    # Control de disparos
    shoot_delay = 200  # Milisegundos entre disparos
    last_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo

    while running:
        # Dibujar fondo (imagen)
        screen.blit(background_img, (0, 0))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pausar el juego
                    pausar_juego()

        # Calcular tiempo transcurrido desde el inicio del juego
        current_time = pygame.time.get_ticks()
        tiempo_transcurrido = current_time - start_time

        # Calcular la velocidad actual de los enemigos
        factor_tiempo = min(tiempo_transcurrido / TIEMPO_MAXIMO, 1)  # Normaliza entre 0 y 1
        velocidad_enemigos = MIN_VELOCIDAD + factor_tiempo * (MAX_VELOCIDAD - MIN_VELOCIDAD)

        # Ajustar la velocidad del jugador (inicia en 2 y aumenta el doble que la de los enemigos)
        player_speed = 4 + (velocidad_enemigos - MIN_VELOCIDAD) * 2

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_img.get_width():
            player_pos[0] += player_speed

        # Disparar balas continuamente al mantener presionada la barra espaciadora
        if keys[pygame.K_SPACE] and current_time - last_shot_time > shoot_delay:
            shoot_bullet(player_pos[0], player_pos[1])
            last_shot_time = current_time

        # Dibujar al jugador
        screen.blit(player_img, (player_pos[0], player_pos[1]))

        # Mover y dibujar enemigos con velocidad ajustada
        mover_dibujar_enemigos(tiempo_transcurrido)

        # Actualizar y dibujar disparos
        for bullet in bullets[:]:
            bullet.y -= 10  # velocidad de la bala
            pygame.draw.rect(screen, (255, 255, 0), bullet)
            if bullet.y < 0:
                bullets.remove(bullet)

        # Detectar colisiones entre balas y enemigos
        colision_enemigo()

        # Dibujar el puntaje en pantalla
        dibujar_puntaje(puntos)

        # Dibujar las animaciones de puntos
        dibujar_puntos_animaciones()

        # Actualizar pantalla
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main_menu()
        game_loop()
    except Exception as e:
        print("Ocurrió un error:", e)
        pygame.quit()
        input("Presiona Enter para cerrar...")


