import time
import evaluacion
import greedy_aleatorio
import random
import individuo
import logs
import estadisticas
import numpy as np
from collections import deque
def creacion_sol_aleatorias( num_sol, aleatorio, tam_sol,m_flujo,m_distacias):


    poblacion_aleatoria=[]

    for i in range(num_sol):
        solucion = list(range(tam_sol))
        aleatorio.shuffle(solucion)
        individuo_aleatorio = individuo.Individuo(solucion)
        poblacion_aleatoria.append(individuo_aleatorio)

    return poblacion_aleatoria

def poblacion_inicial(tam_sol, k, tam_poblacion, tam_greedy, m_flujo, m_distancia, aleatorio,elite):
    #creo las soluciones aleatorias puras
    tam_Aleatorios=tam_poblacion- tam_poblacion*tam_greedy
    tam_greedy_sol=tam_poblacion*tam_greedy

    poblacion_aleatoria=creacion_sol_aleatorias(int(tam_Aleatorios),aleatorio,tam_sol,m_flujo,m_distancia)

    poblacion_greedy = []

    for i in range(int(tam_greedy_sol)):
        sol=greedy_aleatorio.greedy_aleatorio(tam_sol, m_flujo,m_distancia,aleatorio,k)
        individuo_greedy= individuo.Individuo(sol)


        poblacion_greedy.append(individuo_greedy)

    poblacion=poblacion_greedy+poblacion_aleatoria

    return poblacion

'''
Se define una función de cruce OX2 con un número de posiciones seleccionadas de forma aleatoria según la probabilidad de cruce indicada por el usuairo en los parámetros
'''
def cruce_ox2(i, j, aleatorio, probabilidad_cruce):
    # Primero generamos una lista con los elemento de j que se van a cambiar
    hijo = individuo.Individuo([item for item in i.asignacion])
    lista_seleccionados=[item for item in j.asignacion if aleatorio.random() < 0.5]
    lista_seleccionados_restantes = [item for item in lista_seleccionados]
    for indice in range(len(hijo.asignacion)):
        if hijo.asignacion[indice] in lista_seleccionados:
            hijo.asignacion[indice] = lista_seleccionados_restantes.pop(0)
    return hijo

def cruce_moc(i, j, aleatorio, tam):
    punto = aleatorio.randrange(tam)
    sublista_i = i.asignacion[punto:]
    sublista_j = j.asignacion[punto:]
    b_i = individuo.Individuo([item if item not in sublista_j else -1 for item in i.asignacion ])
    b_j = individuo.Individuo([item if item not in sublista_i else -1 for item in j.asignacion ])

    for indice in range(len(b_i.asignacion)):
        if b_i.asignacion[indice] == -1:
            b_i.asignacion[indice] = sublista_j.pop(0)
    for indice in range(len(b_j.asignacion)):
        if b_j.asignacion[indice] == -1:
            b_j.asignacion[indice] = sublista_i.pop(0)

    return b_i, b_j

def seleccion_por_torneo(poblacion, tam, aleatorio, Kbest):
    nueva_poblacion=[]
    for i in range(tam):
        nueva_poblacion.append(seleccion_padre_por_torneo(poblacion, aleatorio,Kbest))
    return nueva_poblacion


def intercambio_2_opt(solucion, i, j):
    #print("Ejecutando intercambio 2-opt...")
    nueva_solucion = solucion.copy()
    nueva_solucion[i], nueva_solucion[j] = nueva_solucion[j], nueva_solucion[i]
    return nueva_solucion

def mutacion(poblacion, tam, probabilidad_mutacion,aleatorio,log):
    for i in range(len(poblacion)):
        if aleatorio.random()>probabilidad_mutacion:
            pos_i=aleatorio.randint(0,tam-1)
            pos_j=0
            while pos_j==pos_i:
                pos_j=aleatorio.randint(0,tam-1)
            poblacion[i].asignacion=intercambio_2_opt(poblacion[i].asignacion,pos_i,pos_j)
            poblacion[i].evaluado=False


    return poblacion

def torneo_de_perdedores(poblacion, aleatorio, K_worst, individuo_elite, tam, m_flujo, m_distancia):
    participantes = aleatorio.sample(poblacion, K_worst)
    for participante in participantes:
        if participante.evaluado == False:
            participante.evaluar(tam,m_flujo,m_distancia)
    perdedor = max(participantes, key=lambda ind: ind.coste)
    try:
        indice_victima = poblacion.index(perdedor)
        poblacion[indice_victima] = individuo_elite
    except ValueError:
        # Esta situación es muy rara, pero por seguridad, si no encuentra
        # a la víctima (quizás por un error de igualdad), simplemente
        # reemplazamos al peor individuo global de la nueva población.
        peor_global = max(poblacion, key=lambda ind: ind.coste)
        indice_peor = poblacion.index(peor_global)
        poblacion[indice_peor] = individuo_elite

    return poblacion

def seleccion_padre_por_torneo(poblacion, aleatorio, Kbest):
    '''
        Ejecuta un torneo de tamaño Kbest para seleccionar los mejores individuos de la población.
        :param poblacion:
        :param aleatorio:
        :param Kbest:
        :return:
        '''
    # 1. Elegir k participantes al azar (sin repetición)
    participantes = aleatorio.sample(poblacion, int(Kbest))
    # 2. Seleccionar el mejor individuo entre los participantes
    ganador = min(participantes, key=lambda ind: ind.coste)
    return ganador

def cruce(poblacion, tam, probabilidad_cruce, aleatorio, kbest, operador_cruce):
    nueva_poblacion=[]
    for i in range(0,tam,2):
        padre1 = poblacion.pop(0)
        padre2 = poblacion.pop(0)
        if aleatorio.random() < probabilidad_cruce:
            # Se cruzan los padres
            if operador_cruce == "OX2":
                hijo1 = cruce_ox2(padre1, padre2, aleatorio, probabilidad_cruce)
                hijo2 = cruce_ox2(padre2, padre1, aleatorio, probabilidad_cruce)
            elif operador_cruce == "MOC":
                hijo1, hijo2 = cruce_moc(padre1, padre2, aleatorio, len(padre1.asignacion))
            else:
                raise ValueError(f"Operador de cruce desconocido: {operador_cruce}")
        else:
            # No se cruzan, los hijos son copias de los padres
            hijo1 = padre1
            hijo2 = padre2
        nueva_poblacion.append(hijo1)
        nueva_poblacion.append(hijo2)
    return nueva_poblacion

def obtener_elite(poblacion, n_elite):
    poblacion_ordenada = sorted(poblacion, key=lambda ind: ind.coste)
    elite = []
    for i in range(int(n_elite)):
        elite.append(poblacion_ordenada[i].copiar())
    return elite

def esta_poblacion(individuo,poblacion):

    for i in poblacion:
        if(i.asignacion == individuo.asignacion and i.coste == individuo.coste):
            return True

    return False
def busqueda_tabu(tam, matriz_flujo, matriz_distancia, num_max_iteraciones, aleatorio, K, tenencia_tabu, oscilacion_estrategica, estancamiento, log):
    print("Ejecutando búsqueda tabu...")

    # Generar solución inicial con algoritmo greedy
    log.log("Ejecuccuón de Greedy Aleatorio para obtener solución inicial de Búsqueda Tabu")
    solucion = greedy_aleatorio.greedy_aleatorio(tam, matriz_flujo, matriz_distancia, aleatorio, K, log)
    coste_solucion = evaluacion.evaluacion(tam, matriz_flujo, matriz_distancia, solucion)
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

    #Actualizamos la memoria a largo plazo con la solución inicial
    actualizar_memoria_largo_plazo(memoria_largo_plazo, tam, solucion)

    # Contador de oscilación y estancamiento
    num_oscilacion = 0  # Contador de movimientos sin mejora
    num_oscilacion_estancamiento = num_max_iteraciones * estancamiento  # Umbral para detectar estancamiento

    while num_iteraciones < num_max_iteraciones:
        mejor_vecino = solucion
        mejor_coste_vecino = coste_solucion

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
                            coste_solucion = evaluacion.factorizacion(tam, matriz_flujo, matriz_distancia, solucion, i, pos_j, mejor_coste_vecino)
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
            actualizar_memoria_largo_plazo(memoria_largo_plazo, tam, mejor_vecino)

        # Comprobamos estancamiento
        if num_oscilacion >= num_oscilacion_estancamiento:
            log.log("Estancamiento detectado. Aplicando estrategia de oscilación.")
            #print("Estancamiento detectado. Reiniciando memoria a corto plazo.")
            reiniciar_memoria_corto_plazo(memoria_corto_plazo)
            num_oscilacion = 0  # Reiniciar el contador de oscilación
            if aleatorio.random() < oscilacion_estrategica:
                # Diversificación: Con la memoria a largo plazo, buscamos una solución alejada de las mejores históricas
                log.log_evento("diversificación estratégica.", f"num_iteraciones={num_iteraciones}")
                solucion = diversificacion_estrategica(tam, memoria_largo_plazo, aleatorio, K)
            else:
                # Intensificación: Con la memoria a largo plazo, buscamos una solución cercana a las mejores históricas
                log.log_evento("intensificación estratégica.", f"num_iteraciones={num_iteraciones}")
                solucion = intensificacion_estrategica(tam, memoria_largo_plazo, aleatorio, K)
            coste_solucion = ev.evaluacion(tam, matriz_flujo, matriz_distancia, solucion)
            log.log(" Nueva solución tras oscilación estratégica.", "EVENT")
            log.log( f"Solución: {solucion}, Coste: {coste_solucion}", "EVENT")
            log.log(f"Coste mejor solución hasta ahora: {coste_mejor}", "EVENT")

    return mejor_solucion

def algoritmo_memetico(tam_problema, k, tam_poblacion, tam_greedy, m_flujo, m_distancia, aleatorio, max_evaluaciones,n_elite,Kbest,K_worst,prob_mutacion,tiempo_max, operador_cruce, probabilidad_cruce,log, n_eval_tabu_max, n_iter_tabu, tenencia_tabu):
    n_evaluaciones=0
    n_eval_tabu=0
    gen = 0
    mejor_individuo=None
    tiempo_inicio=time.perf_counter()
    poblacion_actual = poblacion_inicial(tam_problema, k, tam_poblacion, tam_greedy, m_flujo, m_distancia, aleatorio, n_elite)
    while n_evaluaciones < max_evaluaciones and (time.perf_counter()-tiempo_inicio<tiempo_max):
        gen = gen + 1
        log.log(f"Generación: {gen}", "GENERACION")
        # Obtenemos la poblacion elite
        elite = obtener_elite(poblacion_actual, n_elite)
        log.log(f"Coste de la población élite", "ELITE")
        for i, ind in enumerate(elite):
            log.log(f"E_{i}: {ind.coste}", "ELITE")
        # Ejecutamos seleccion
        poblacion_actual=seleccion_por_torneo(poblacion_actual, tam_poblacion, aleatorio, Kbest)
        # Ejecutamos cruce
        poblacion_actual=cruce(poblacion_actual, tam_poblacion, probabilidad_cruce, aleatorio, Kbest, operador_cruce)
        # Ejecutamos mutacion
        poblacion_actual=mutacion(poblacion_actual, tam_problema, prob_mutacion, aleatorio, log)
        # Evaluamos la poblacion actual
        evaluaciones_gen = evaluacion.evaluacion_poblacion(tam_problema, m_flujo, m_distancia, poblacion_actual)
        n_evaluaciones += evaluaciones_gen
        n_eval_tabu += evaluaciones_gen
        # Aplicamos la búsqueda tabú a los mejores individuos de la población
        if n_eval_tabu > n_eval_tabu_max:
            log.log("Aplicando búsqueda tabú a la élite...", "TABU")
            for ind in elite:
                # Aquí se podría implementar una función de búsqueda tabú específica
                pass
            n_eval_tabu -= n_eval_tabu_max
        log.log(f"Número total de evaluaciones: {n_evaluaciones}")

        # implementacion del reemplazamiento si elite no sobrevive es decir no está en poblacion_actual se aplica torneo de perdedores
        for i in elite:
            if (esta_poblacion(i, poblacion_actual) == False):
                poblacion_actual = torneo_de_perdedores(poblacion_actual, aleatorio, K_worst, i, tam_problema, m_flujo,
                                                        m_distancia)

        mejor_individuo = min(poblacion_actual, key=lambda ind: ind.coste)
        log.log(f"El individuo con el coste mínimo tiene un coste de: {mejor_individuo.coste}")

    return mejor_individuo, n_evaluaciones

def main():
    probabilidad_cruce = 0.5
    aleatorio = random.Random(1)
 #   individuo1 = individuo.Individuo([1, 2, 3, 4, 5, 6, 7, 8])
  #  individuo2 = individuo.Individuo([2, 4, 6, 8, 7, 5, 3, 1])

#   hijo1, hijo2 = cruce_moc(individuo1, individuo2, aleatorio, 8)
#    #hijo2 = cruce_ox2(individuo2, individuo1, aleatorio, probabilidad_cruce)

 #   print(f"Hijo 1: {hijo1.asignacion}")
  #  print(f"Hijo 2: {hijo2.asignacion}")
   # print(f"Padre: {individuo1.asignacion}")



if __name__ == '__main__':
    main()



