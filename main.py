import soko
import gamelib
from pilas import Pila
import backtracking

NORTE = (0, -1)
SUR = (0, 1)
ESTE = (1, 0)
OESTE = (-1, 0)
REINICIAR = "r"
SALIR = "Escape"
DESHACER = "z"
REHACER = "x"
PISTAS = "h"
PASAR_NIVEL = "n"
TAMAÑO_IMAGENES = 64


def juego_crear(niveles, numero_nivel):
    """
    Inicializa la grilla correspondiente al numero de nivel
    """
    juego = soko.crear_grilla(niveles[numero_nivel])
    return juego

def juego_mostrar(juego, nivel):
    """
    Se encarga de dibujar los elementos relacionados al juego
    """
    x,y = soko.dimensiones(juego)
    gamelib.resize(x*115, y*65)

    for j in range(0, y*65, TAMAÑO_IMAGENES):
        for i in range(0, x*115, TAMAÑO_IMAGENES):
            gamelib.draw_image('img/ground.gif', i, j)
    
    for i in range(len(juego)):
        for j in range(len(juego[i])):
            if juego[i][j] == '#':
                gamelib.draw_image('img/wall.gif', j*TAMAÑO_IMAGENES, i*TAMAÑO_IMAGENES)
            if juego[i][j] == soko.JUGADOR or juego[i][j] == soko.JUGADOR_OBJETIVO:
                gamelib.draw_image('img/player.gif', j*TAMAÑO_IMAGENES, i*TAMAÑO_IMAGENES)
            if juego[i][j] == soko.CAJA or juego[i][j] == soko.CAJA_OBJETIVO:
                gamelib.draw_image('img/box.gif', j*TAMAÑO_IMAGENES, i*TAMAÑO_IMAGENES)
            if juego[i][j] == soko.OBJETIVO or juego[i][j] == soko.JUGADOR_OBJETIVO or juego[i][j] == soko.CAJA_OBJETIVO:
                gamelib.draw_image('img/goal.gif', j*TAMAÑO_IMAGENES, i*TAMAÑO_IMAGENES)

    gamelib.draw_text(f"Estas en el nivel {nivel}", (x*115)-100, (y*65)-20, fill="black", italic=True, bold=True)

    return juego

def cargar_niveles(nombre_archivo):
    """
    Carga todos los niveles en memoria y los devuelve en un diccionario
    """
    diccionario_niveles = {}
    contador_nivel = 1
    with open(nombre_archivo) as lvl:

        lineas = lvl.readlines() 
        for i in range(len(lineas)):
            lineas[i] = lineas[i].rstrip("\n")
            if lineas[i] == f"Level {contador_nivel}" and not contador_nivel in diccionario_niveles:
                diccionario_niveles[contador_nivel] = [] 
            if not "Level" in lineas[i] and not "'" in lineas[i] and not lineas[i] == "": 
                diccionario_niveles[contador_nivel].append(lineas[i])
            if lineas[i] == "":
                contador_nivel += 1
            
    return diccionario_niveles

def que_hace_la_tecla(tecla, archivo_instrucciones):
    """
    Devuelve la instruccion validada correspondiente a la tecla presionada.
    """
    instruccion = 0
    with open(archivo_instrucciones, 'r') as ev:

        for linea in ev:
            linea = linea.rstrip("\n").split()

            for i in range(len(linea)):
                if tecla == linea[0]:
                    instruccion = linea[2]

    instruccion = validacion_instruccion(instruccion)
                
    return instruccion

def validacion_instruccion(instruccion):
    """
    Devuelve la instruccion validada o 0 si no es una instruccion valida.
    """
    if instruccion == "NORTE":
        return NORTE
    if instruccion == "SUR":
        return SUR
    if instruccion == "ESTE":
        return ESTE
    if instruccion == "OESTE":
        return OESTE
    if instruccion == 'REINICIAR':
        return REINICIAR
    if instruccion == "SALIR":
        return SALIR
    if instruccion == "DESHACER":
        return DESHACER
    else:
        return 0
      

def actualizar_juego(juego, instruccion):
    """
    Modifica el juego en base al movimiento realizado.
    """
    juego = soko.mover(juego, instruccion)
    return juego

def main():
    # Titulo e icono de la ventana del juego
    gamelib.title("Sokoban")
    gamelib.icon("img/player.gif")

    # Inicializar el estado del juego
    i = -1
    contador_nivel = 1
    niveles = cargar_niveles("niveles.txt")
    juego = juego_crear(niveles, contador_nivel)
    pila_deshacer = Pila()
    pila_rehacer = Pila()
    pistas_encontradas = False
    error_de_recursion = False
    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        juego_mostrar(juego, contador_nivel)

        if pistas_encontradas:
            gamelib.draw_text("Tu solucion esta lista", 100, 20, fill="black", italic=True, bold=True)

        if error_de_recursion:
            gamelib.draw_text("El nivel no tiene pistas", 100, 20, fill="black", italic=True, bold=True)

        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key

        instruccion = que_hace_la_tecla(tecla, "teclas.txt")

        if tecla == SALIR:
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if tecla == REINICIAR:
            # El usuario presionó la tecla r, reiniciar el nivel.
            pila_deshacer = Pila()
            pila_rehacer = Pila()
            juego = juego_crear(niveles, contador_nivel)

        if tecla == PISTAS:
            # El usuario presiono la tecla h, buscar solucion al nivel(hasta nivel 19 inclusive sin errores)
            try:
                pistas_encontradas, movimientos = backtracking.solucion(juego)
                i = len(movimientos)-1
            except RecursionError:
                error_de_recursion = True
        
        if tecla == PASAR_NIVEL:
            # El usuario presiono la tecla n, realizar un movimiento de los encontrados en solucion
            if i >= 0:
                pila_deshacer.apilar(juego)
                juego = actualizar_juego(juego, movimientos[i])
                i -= 1

        if tecla == DESHACER:
            # El usuario presiono la tecla z, regresar al movimiento anterior
            if not pila_deshacer.esta_vacia():
                pila_rehacer.apilar(juego)
                juego = soko.crear_grilla(pila_deshacer.desapilar())
        
        if tecla == REHACER:
            # El usuario presiono la tecla x, volver al movimiento deshecho
            if not pila_rehacer.esta_vacia():
                pila_deshacer.apilar(juego)
                juego = soko.crear_grilla(pila_rehacer.desapilar())
        
        if instruccion != REINICIAR and instruccion != SALIR and instruccion != 0 and instruccion != DESHACER:
            pila_deshacer.apilar(juego)
            juego = actualizar_juego(juego, instruccion)
                
        
        if soko.juego_ganado(juego):
            pila_deshacer = Pila() #Reinicia las pilas de deshacer y rehacer cuando cambia el nivel
            pila_rehacer = Pila()
            pistas_encontradas = False
            error_de_recursion = False
            if contador_nivel < len(niveles):
                contador_nivel += 1
                juego = juego_crear(niveles, contador_nivel)
            else:
                break

gamelib.init(main)