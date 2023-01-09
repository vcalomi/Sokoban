import soko

NORTE = (0, -1)
SUR = (0, 1)
ESTE = (1, 0)
OESTE = (-1, 0)

def solucion(estado_inicial):
    """
    Encuentra una solucion a traves de un algoritmo de backtracking
    """
    visitados = set()
    return backtracking(estado_inicial, visitados)

def backtracking(estado_nivel, visitados):
    """
    Funcion que opera de manera recursiva, probando todas las combinaciones de movimientos
    """
    agregar(visitados, estado_nivel)
    if soko.juego_ganado(estado_nivel):
        return True, []
    a = [ESTE, SUR, NORTE, OESTE]
    for accion in a:
        estado_nuevo = soko.mover(estado_nivel, accion)
        if pertenece(visitados, estado_nuevo):
            continue
        solucion_encontrada, acciones = backtracking(estado_nuevo, visitados)
        if solucion_encontrada:
            return True, concatenar(accion, acciones)
    return False, None

def agregar(visitados, estado):
    """
    Convierte el estado a un tipo de dato inmutable y lo agrega a un Set
    """
    estado_tupla = tuple(map(tuple, estado))
    visitados.add(estado_tupla)
    return visitados

def pertenece(visitados, estado):
    """
    Convierte el estado a un tipo de dato inmutable y chequea si pertenece a un Set
    """
    estado_tupla = tuple(map(tuple, estado))
    if estado_tupla in visitados:
        return True
    else:
        return False

def concatenar(accion, acciones):
    """
    Agrega una accion al conjunto de acciones
    """
    acciones.append(accion)
    return acciones