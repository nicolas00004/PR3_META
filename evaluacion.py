
def factorizacion(tam, matriz_flujo, matriz_distancia, asignacion, i , j, coste_actual):
    coste_nuevo = coste_actual
    for k in range(tam):
        if k != i and k != j:
            coste_nuevo += matriz_flujo[i,k] * (matriz_distancia[asignacion[i], asignacion[k]] - matriz_distancia[asignacion[j], asignacion[k]]) *2
            coste_nuevo += matriz_flujo[j,k] * (matriz_distancia[asignacion[j], asignacion[k]] - matriz_distancia[asignacion[i], asignacion[k]]) *2
    return coste_nuevo

def evaluacion_poblacion(tam, matriz_flujo, matriz_distancia, poblacion):
    cont=0
    for individuo in poblacion:
        if (individuo.evaluado== False):
            costo_individual, evaluado = individuo.evaluar(tam, matriz_flujo, matriz_distancia)
            cont=cont+evaluado

    return cont