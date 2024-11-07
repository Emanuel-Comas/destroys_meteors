import pygame
import random

# Inicializar Pygame
pygame.init()  # Inicia todos los módulos de Pygame

# Configuración de la pantalla
ANCHO, ALTO = 800, 600  # Establece las dimensiones de la ventana del juego (800x600 píxeles)
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego con las dimensiones especificadas
pygame.display.set_caption("Destrucción de Meteoritos")  # Establece el título de la ventana

# Colores
NEGRO = (0, 0, 0)  # Color negro para el fondo
BLANCO = (255, 255, 255)  # Color blanco para los disparos y el texto

# Cargar imágenes
nave_imagen = pygame.image.load("transbordador-espacial.png")  # Carga la imagen de la nave
nave_imagen = pygame.transform.scale(nave_imagen, (50, 50))  # Redimensiona la imagen de la nave a 50x50 píxeles
meteorito_imagen = pygame.image.load("meteorito.png")  # Carga la imagen del meteorito
meteorito_imagen = pygame.transform.scale(meteorito_imagen, (50, 50))  # Redimensiona la imagen del meteorito a 50x50 píxeles
nave_rect = nave_imagen.get_rect()  # Obtiene el rectángulo que rodea la nave (necesario para manejar su posición)

# Configuración de la nave
nave_rect.centerx = ANCHO // 2  # Coloca la nave en el centro horizontal de la pantalla
nave_rect.bottom = ALTO - 10  # Coloca la nave en la parte inferior de la pantalla, 10 píxeles arriba del borde
nave_velocidad = 7  # Define la velocidad de movimiento de la nave

# Configuración de meteoritos
meteoritos = []  # Lista para almacenar todos los meteoritos
meteorito_velocidad = 1  # Velocidad a la que caen los meteoritos
meteorito_intervalo = 30  # Intervalo (en cuadros) para la generación de nuevos meteoritos
meteorito_tamano = (50, 50)  # Tamaño de cada meteorito (50x50 píxeles)

# Configuración del reloj
reloj = pygame.time.Clock()  # Reloj para controlar la velocidad de actualización del juego (FPS)

# Lista de disparos
disparos = []  # Lista para almacenar los disparos disparados por la nave
disparo_velocidad = 10  # Velocidad de los disparos (se mueve hacia arriba)

# Puntuación
puntuacion = 0  # Puntuación inicial del jugador
fuente_puntuacion = pygame.font.SysFont("Arial", 30)  # Fuente para mostrar la puntuación en pantalla

# Color para el mensaje de Game Over (rojo)
ROJO = (255, 0, 0)

# Función para mostrar el mensaje de "Game Over"
def mostrar_game_over():
    fuente_game_over = pygame.font.SysFont("Arial", 60)  # Fuente de texto para el mensaje de "Game Over"
    mensaje = fuente_game_over.render("GAME OVER", True, ROJO)  # Renderiza el texto "GAME OVER" en color rojo
    # Coloca el mensaje de "Game Over" en el centro de la pantalla
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - mensaje.get_height() // 2))
    pygame.display.flip()  # Actualiza la pantalla para que el mensaje sea visible
    pygame.time.wait(2000)  # Espera 2 segundos antes de finalizar el juego

# Bucle principal del juego
jugando = True  # Variable que indica si el juego sigue en marcha
contador_meteoritos = 0  # Contador para generar meteoritos a intervalos regulares

while jugando:
    # Manejo de eventos (detectar teclas y acciones del jugador)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Si el jugador cierra la ventana
            jugando = False  # Finaliza el bucle principal y termina el juego
        elif evento.type == pygame.KEYDOWN:  # Si una tecla es presionada
            if evento.key == pygame.K_SPACE:  # Si la tecla presionada es el espacio
                # Crear un disparo en la posición actual de la nave
                disparo_rect = pygame.Rect(nave_rect.centerx - 5, nave_rect.top, 10, 20)
                disparos.append(disparo_rect)  # Añadir el disparo a la lista de disparos

    # Obtener teclas presionadas para mover la nave
    teclas = pygame.key.get_pressed()

    # Movimiento de la nave
    if teclas[pygame.K_LEFT] and nave_rect.left > 0:  # Si se presiona la flecha izquierda y la nave no está en el borde izquierdo
        nave_rect.x -= nave_velocidad  # Mover la nave a la izquierda
    if teclas[pygame.K_RIGHT] and nave_rect.right < ANCHO:  # Si se presiona la flecha derecha y la nave no está en el borde derecho
        nave_rect.x += nave_velocidad  # Mover la nave a la derecha

    # Generar meteoritos a intervalos
    contador_meteoritos += 1  # Incrementar el contador para generar meteoritos a intervalos regulares
    if contador_meteoritos > meteorito_intervalo:  # Si el contador supera el intervalo
        # Crear un meteorito en una posición aleatoria en el eje horizontal, pero fuera de la pantalla al principio
        meteorito_rect = pygame.Rect(random.randint(0, ANCHO - meteorito_tamano[0]), -50, *meteorito_tamano)
        meteoritos.append(meteorito_rect)  # Añadir el meteorito a la lista de meteoritos
        contador_meteoritos = 0  # Reiniciar el contador de meteoritos

    # Mover meteoritos
    for meteorito in meteoritos[:]:  # Iterar sobre la lista de meteoritos
        meteorito.y += meteorito_velocidad  # Mover el meteorito hacia abajo
        if meteorito.top > ALTO:  # Si el meteorito sale de la pantalla por la parte inferior
            meteoritos.remove(meteorito)  # Eliminar el meteorito de la lista

        # Verificar si un meteorito toca la nave (colisión)
        if meteorito.colliderect(nave_rect):  # Si hay colisión entre la nave y el meteorito
            jugando = False  # Terminar el juego
            mostrar_game_over()  # Mostrar el mensaje de "Game Over"
            break  # Salir del bucle de meteoritos

    # Mover disparos
    for disparo in disparos[:]:  # Iterar sobre la lista de disparos
        disparo.y -= disparo_velocidad  # Mover el disparo hacia arriba
        if disparo.bottom < 0:  # Si el disparo sale de la pantalla por la parte superior
            disparos.remove(disparo)  # Eliminar el disparo de la lista

        # Verificar si hay colisión entre un disparo y los meteoritos
        for meteorito in meteoritos[:]:
            if disparo.colliderect(meteorito):  # Si el disparo colisiona con un meteorito
                meteoritos.remove(meteorito)  # Eliminar el meteorito
                disparos.remove(disparo)  # Eliminar el disparo
                puntuacion += 10  # Aumentar la puntuación por destruir un meteorito
                break  # Salir del bucle para evitar eliminar más de un meteorito por disparo

    # Rellenar la pantalla con el color negro (limpiar la pantalla)
    pantalla.fill(NEGRO)

    # Dibujar la nave en su nueva posición
    pantalla.blit(nave_imagen, nave_rect)

    # Dibujar todos los meteoritos
    for meteorito in meteoritos:
        pantalla.blit(meteorito_imagen, meteorito)

    # Dibujar todos los disparos
    for disparo in disparos:
        pygame.draw.rect(pantalla, BLANCO, disparo)  # Dibujar el disparo como un rectángulo blanco

    # Mostrar la puntuación en la pantalla
    texto_puntuacion = fuente_puntuacion.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))  # Colocar el texto de la puntuación en la esquina superior izquierda

    # Actualizar la pantalla para mostrar todos los cambios
    pygame.display.flip()

    # Controlar los frames por segundo (FPS)
    reloj.tick(60)  # Limitar la tasa de refresco a 60 FPS

# Salir del juego
pygame.quit()  # Finaliza Pygame y cierra la ventana
