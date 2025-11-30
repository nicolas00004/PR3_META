import time
import evaluacion
import greedy_aleatorio
import random
import individuo
import logs
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
def algortimo_evolutivo_generacional(tam, k,tam_poblacion,tam_greedy,m_flujo,m_distancia,aleatorio,max_iteraciones,n_elite,Kbest,K_worst,prob_mutacion,tiempo_max, operador_cruce, probabilidad_cruce,log, estadisticas):
    cont =0
    gen = 0
    tiempo_incio=time.perf_counter()
    poblacion_actual=[]
    mejor_individuo=None

    # Generamos una poblacion inicial
    poblacion_actual = poblacion_inicial(tam, k, tam_poblacion, tam_greedy, m_flujo, m_distancia, aleatorio, n_elite)
    cont=cont+evaluacion.evaluacion_poblacion(tam, m_flujo, m_distancia, poblacion_actual)
    log.log("Poblacion inicial creada")
    log.log(f"Número de iteraciones: {cont}")
    while (cont < int(max_iteraciones)) and ((time.perf_counter()-tiempo_incio)<tiempo_max):
        gen = gen + 1
        log.log(f"Generación: {gen}", "GENERACION")
        #Obtenemos la poblacion elite
        elite = obtener_elite(poblacion_actual, n_elite)
        log.log(f"Coste de la población élite", "ELITE")
        for i, ind in enumerate(elite):
            log.log(f"E_{i}: {ind.coste}", "ELITE")
        # Seleccion por torneo
        poblacion_actual = seleccion_por_torneo(poblacion_actual, tam_poblacion, aleatorio, Kbest)
        #implementacion de los cruces
        poblacion_actual = cruce(poblacion_actual,tam_poblacion, probabilidad_cruce, aleatorio, Kbest, operador_cruce)
        #implementacion de la mutacion
        poblacion_actual=mutacion(poblacion_actual, tam,prob_mutacion, aleatorio, log)
        # actualizamos los costes de la poblacion actual
        cont = cont + evaluacion.evaluacion_poblacion(tam, m_flujo, m_distancia, poblacion_actual)
        log.log(f"Número de iteraciones: {cont}")
        #implementacion del reemplazamiento si elite no sobrevive es decir no está en poblacion_actual se aplica torneo de perdedores
        for i in elite:
            if(esta_poblacion(i,poblacion_actual)== False):
                poblacion_actual= torneo_de_perdedores(poblacion_actual,aleatorio,K_worst,i, tam, m_flujo, m_distancia)

        mejor_individuo = min(poblacion_actual, key=lambda ind: ind.coste)
        log.log(f"El individuo con el coste mínimo tiene un coste de: {mejor_individuo.coste}")
        estadisticas.nuevo_punto(cont, mejor_individuo.coste)
        #print(f"El individuo con el coste mínimo tiene un coste de: {mejor_individuo.coste}")

    return mejor_individuo,cont


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



