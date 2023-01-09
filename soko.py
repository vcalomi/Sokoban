JUGADOR = "@"
JUGADOR_OBJETIVO = "+"
CAJA = "$"
CAJA_OBJETIVO = "*"
OBJETIVO = "."



def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []
    
    for i in range(len(desc)):
        grilla.append([])
        for j in range(len(desc[i])):
            grilla[i].append(desc[i][j])
    
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    cant_filas_columnas = (len(grilla[0]), len(grilla))
    return cant_filas_columnas

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    if grilla[f][c] == "#":
        return True
    else:
        return False

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    if grilla[f][c] == "." or grilla[f][c] == "*" or grilla[f][c] == "+":
        return True
    else:
        return False

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    if grilla[f][c] == "$" or grilla[f][c] == "*":
        return True
    else:
        return False

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    if grilla[f][c] == "@" or grilla[f][c] == "+":
        return True
    else:
        return False

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if grilla[i][j] == '.' or grilla[i][j] == '$':
                return False
    return True

def casos_borde(grilla, direccion, pos_jugador):
    
    condicion_filas = pos_jugador[0]+direccion[1] >= 0 and pos_jugador[0]+direccion[1] <= len(grilla)

    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            condicion_columnas = pos_jugador[1]+direccion[0] >= 0 and pos_jugador[1]+direccion[0] <= len(grilla[pos_jugador[0]])

    return condicion_filas, condicion_columnas


def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    grilla_actualizada = copiar_grilla(grilla) 

    pos_jugador = obtener_pos_jugador(grilla) 

    caracter_jugador = grilla[pos_jugador[0]][pos_jugador[1]]
    
    siguiente_caracter = grilla[pos_jugador[0]+direccion[1]][pos_jugador[1]+direccion[0]]

    condicion_filas, condicion_columnas = casos_borde(grilla, direccion, pos_jugador)
    
    if condicion_columnas == True and condicion_filas == True and siguiente_caracter == CAJA or siguiente_caracter == CAJA_OBJETIVO:

        direcciones_con_caja(grilla_actualizada, direccion, pos_jugador, caracter_jugador)
        
    elif condicion_columnas == True and condicion_filas == True:
        
        direcciones_sin_caja(grilla_actualizada, direccion, pos_jugador, caracter_jugador)

    return grilla_actualizada

def direcciones_sin_caja(grilla, direccion, pos_jugador, carac_jugador):
    """
    Mueve al jugador en la direccion indicada si en ella no se encuentra una caja.
    """
    coordenada_y_jugador = pos_jugador[0]
    coordenada_x_jugador = pos_jugador[1]
    
    coordenada_direccion_y = pos_jugador[0]+direccion[1] 
    coordenada_direccion_x = pos_jugador[1]+direccion[0] 

    if grilla[coordenada_direccion_y][coordenada_direccion_x] == " ":
        grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR
        grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
        if carac_jugador == JUGADOR_OBJETIVO:
            grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO

    elif grilla[coordenada_direccion_y][coordenada_direccion_x] == OBJETIVO:

        grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
        grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR_OBJETIVO
        if carac_jugador == JUGADOR_OBJETIVO:
            grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO
    
def direcciones_con_caja(grilla, direccion, pos_jugador, carac_jugador):
    """
    Mueve al jugador en la direccion indicada si en ella se encuentra una caja.
    """
    coordenada_y_jugador = pos_jugador[0] 
    coordenada_x_jugador = pos_jugador[1] 

    coordenada_direccion_y = pos_jugador[0]+direccion[1] 
    coordenada_direccion_x = pos_jugador[1]+direccion[0] 

    coordenada_siguiente_caja_y = pos_jugador[0]+(direccion[1]*2) 
    coordenada_siguiente_caja_x = pos_jugador[1]+(direccion[0]*2) 
    

    if grilla[coordenada_direccion_y][coordenada_direccion_x] == CAJA:

        if grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] == " ":

            grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
            grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR
            grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] = CAJA
            if carac_jugador == "+":
                grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO

        elif grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] == OBJETIVO:

            grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
            grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR
            grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] = CAJA_OBJETIVO
            if carac_jugador == JUGADOR_OBJETIVO:
                grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO

    if grilla[coordenada_direccion_y][coordenada_direccion_x] == CAJA_OBJETIVO:
        
        if grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] == " ":
            
            grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
            grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR_OBJETIVO
            grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] = CAJA
            if carac_jugador == JUGADOR_OBJETIVO:
                grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO
            

        elif grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] == OBJETIVO:

            grilla[coordenada_y_jugador][coordenada_x_jugador] = " "
            grilla[coordenada_direccion_y][coordenada_direccion_x] = JUGADOR_OBJETIVO
            grilla[coordenada_siguiente_caja_y][coordenada_siguiente_caja_x] = CAJA_OBJETIVO
            if carac_jugador == JUGADOR_OBJETIVO:
                grilla[coordenada_y_jugador][coordenada_x_jugador] = OBJETIVO
    
    return grilla



def obtener_pos_jugador(grilla):
    """
    Devuelve una tupla con la posicion del jugador en el formato fila, columna.
    """
    pos_jugador = []

    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if grilla [i][j] == "@" or grilla[i][j] == "+":
                pos_jugador = [i, j]
                break
    return pos_jugador

def copiar_grilla(grilla):
    """
    Devuelve una copia por valor de la grilla original.
    """
    grilla_actualizada = []

    for i in range(len(grilla)):
        grilla_actualizada.append([])
        for j in range(len(grilla[i])):
            grilla_actualizada[i].append(grilla[i][j])

    return grilla_actualizada