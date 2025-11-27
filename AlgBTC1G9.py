from collections import deque

import greedy_aleatorio as gr
import evaluacion as ev
import random
import numpy as np
import logs


def intercambio_2_opt(solucion, i, j):
    #print("Ejecutando intercambio 2-opt...")
    nueva_solucion = solucion.copy()
    nueva_solucion[i], nueva_solucion[j] = nueva_solucion[j], nueva_solucion[i]
    return nueva_solucion

def insertar_corto_plazo(memoria, i, j):
    if i < j:
        elemento = (i, j)
    else:
        elemento = (j, i)
    if elemento in memoria:
        memoria.remove(elemento)
    memoria.append(elemento)

def movimiento_en_tabu(memoria, movimiento):
    if movimiento[0] > movimiento[1]:
        movimiento = (movimiento[1], movimiento[0])
    return movimiento in memoria

def reiniciar_memoria_corto_plazo(memoria):
    memoria.clear()

def actualizar_memoria_largo_plazo(memoria_largo_plazo, tam, solucion):
    for pos in range(tam):
        unidad = solucion[pos]
        memoria_largo_plazo[unidad][pos] += 1
        if unidad != pos:
            memoria_largo_plazo[pos][unidad] += 1 # Simetría


def intensificacion_estrategica(tam, memoria_largo_plazo, aleatorio, k):
    # Generar una solución basada en la memoria a largo plazo
    # Cogemos las k mejores unidades para cada posición y seleccionamos aleatoriamente entre ellas
    solucion = [-1] * tam
    usadas = set()

    for pos in range(tam):
        # Obtener las k mejores unidades para la posición actual
        mejores_unidades = np.argsort(-memoria_largo_plazo[:, pos])[:k]

        # Cogemos una de forma aleatoria entre las mejores que no estén usadas
        for unidad in aleatorio.sample(list(mejores_unidades), len(mejores_unidades)):
            if unidad not in usadas:
                solucion[pos] = int(unidad)
                usadas.add(unidad)
                break

        # Si no se encontró ninguna unidad disponible, asignar aleatoriamente
        if solucion[pos] == -1:
            unidad_aleatoria = aleatorio.randint(0, tam - 1)
            while unidad_aleatoria in usadas:
                unidad_aleatoria = aleatorio.randint(0, tam - 1)
            solucion[pos] = int(unidad_aleatoria)
            usadas.add(unidad_aleatoria)

    return solucion

def diversificacion_estrategica(tam, memoria_largo_plazo, aleatorio, k):
    # Generar una solución basada en la memoria a largo plazo
    # Cogemos las k unidades menos visitadas para cada posición y seleccionamos aleatoriamente entre ellas
    solucion = [-1] * tam
    usadas = set()
    for pos in range(tam):
        menos_visitadas = np.argsort(memoria_largo_plazo[:, pos])[:k]
        # Cogemos una de forma aleatoria entre las mejores que no estén usadas
        for unidad in aleatorio.sample(list(menos_visitadas), len(menos_visitadas)):
            if unidad not in usadas:
                solucion[pos] = int(unidad)
                usadas.add(unidad)
                break

        # Si no se encontró ninguna unidad disponible, asignar aleatoriamente
        if solucion[pos] == -1:
            unidad_aleatoria = aleatorio.randint(0, tam - 1)
            while unidad_aleatoria in usadas:
                unidad_aleatoria = aleatorio.randint(0, tam - 1)
            solucion[pos] = int(unidad_aleatoria)
            usadas.add(unidad_aleatoria)

    return solucion

def busqueda_tabu(tam, matriz_flujo, matriz_distancia, num_max_iteraciones, aleatorio, K, tenencia_tabu, oscilacion_estrategica, estancamiento, log):
    print("Ejecutando búsqueda tabu...")

    # Generar solución inicial con algoritmo greedy
    log.log("Ejecuccuón de Greedy Aleatorio para obtener solución inicial de Búsqueda Tabu")
    solucion = gr.greedy_aleatorio(tam, matriz_flujo, matriz_distancia, aleatorio, K, log)
    coste_solucion = ev.evaluacion(tam, matriz_flujo, matriz_distancia, solucion)
    mejor_solucion = solucion
    coste_mejor = coste_solucion

    log.log_solucion_inicial(solucion, coste_solucion)

    num_iteraciones = 0

    # Definir DLB
    DLB = [0] * tam

    # Crear memoria a corto plazo (Lista circular de tamaño tenencia_tabu)
    memoria_corto_plazo = deque(maxlen=tenencia_tabu)

    #Creamos memoria a largo plazo
    memoria_largo_plazo = np.zeros((tam, tam))

    # Contador de oscilación y estancamiento
    num_oscilacion = 0  # Contador de movimientos sin mejora
    num_oscilacion_estancamiento = num_max_iteraciones * estancamiento  # Umbral para detectar estancamiento

    while num_iteraciones < num_max_iteraciones:
        mejor_vecino = solucion
        mejor_coste_vecino = coste_solucion
        primera_iter = True

        #Exploramos con el DLB
        while not all(DLB) and num_iteraciones < num_max_iteraciones:
            for i in range(tam):
                if DLB[i] == 0:
                    mejora = False
                    pos_j = i
                    for j in range(tam -1):
                        pos_j = (pos_j + 1) % tam
                        #print("i:", i, "j:", j)
                        if i != pos_j:
                            solucion = intercambio_2_opt(mejor_vecino, i, pos_j)
                            coste_solucion = ev.factorizacion(tam, matriz_flujo, matriz_distancia, solucion, i, pos_j, mejor_coste_vecino)
                            # print(coste_solucion)

                            movimiento = (i, pos_j)
                            es_tabu = movimiento_en_tabu(memoria_corto_plazo, movimiento)

                            if coste_solucion < coste_mejor:
                                aspiracion = True
                                mejor_solucion = solucion
                                coste_mejor = coste_solucion
                                num_oscilacion = 0 # Reiniciamos el contador de oscilación
                            else:
                                aspiracion = False

                            if es_tabu and not aspiracion:
                                continue  # Saltar movimientos tabu sin aspiración

                            if coste_solucion < mejor_coste_vecino:
                                log.log_movimiento(num_iteraciones, i, pos_j, solucion, coste_solucion,True)
                                mejor_vecino = solucion
                                mejor_coste_vecino = coste_solucion
                                DLB[i] = 0
                                DLB[j] = 0
                                mejora = True
                                num_oscilacion += 1 # Contamos un movimiento sin mejora
                                num_iteraciones += 1  # Contamos la iteración aquí porque hemos evaluado un vecino
                                insertar_corto_plazo(memoria_corto_plazo, i, pos_j)
                                break

                    if mejora == False:
                        DLB[i] = 1  # Marcar como no mejorable

        if num_iteraciones >= num_max_iteraciones: # Salir si se alcanza el máximo de iteraciones
            break

        # En este punto quiere decir que el DLB =1 para todos
        # Nos movemos al mejor vecino encontrado
        if mejor_vecino is not None:
            solucion = mejor_vecino
            num_iteraciones += 1
            num_oscilacion += 1
            coste_solucion = mejor_coste_vecino
            log.log_movimiento(num_iteraciones, -1, -1, mejor_vecino, mejor_coste_vecino, True if coste_solucion < coste_mejor else False)
            reiniciar_memoria_corto_plazo(memoria_corto_plazo)
            DLB = [0] * tam  # Reiniciar DLB para la nueva solución


    return mejor_solucion

def main():
    # tam = 4
    # matriz_flujo = [
    #     [0, 3, 8, 3],
    #     [3, 0, 2, 4],
    #     [8, 2, 0, 5],
    #     [3, 4, 5, 0]
    # ]
    # matriz_distancia = [
    #     [0, 12, 6, 4],
    #     [12, 0, 6, 8],
    #     [6, 6, 0, 7],
    #     [4, 8, 7, 0]
    # ]
    tam, matriz_flujo, matriz_distancia = practica1.importar_fichero("material/ford01.dat")
    seed = 77385850
    K = 5
    aleatorio = random.Random(seed)
    asignacion = busqueda_tabu(tam, matriz_flujo, matriz_distancia,
    5000, aleatorio, K, 3, 0.5, 0.05)
    coste_solucion = ev.evaluacion(tam, matriz_flujo, matriz_distancia, asignacion)
    print("Asignación final (unidad -> localización):")
    print(asignacion)
    print("Coste de la solución encontrada:", coste_solucion)



if __name__ == "__main__":
    main()