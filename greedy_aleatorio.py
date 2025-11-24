
def greedy_aleatorio(tam, matriz_flujo, matriz_distancia, aleatorio, K):
    # Creación de un vector de pares unidad - flujo total
    flujo_total = []
    for i in range(tam):
        flujo_total.append((i, sum(matriz_flujo[i])))
    flujo_total.sort(key=lambda x: x[1], reverse=True)


    # Creación de un vector de pares localización - distancia total
    distancia_total = []
    for j in range(tam):
        distancia_total.append((j, sum(matriz_distancia[j])))
    distancia_total.sort(key=lambda x: x[1])
    asignacion = [-1] * tam
    for i in range(tam):
        if len(flujo_total) >= K:
            pos_unidad = aleatorio.randint(0, K-1)
            pos_localizacion = aleatorio.randint(0, K-1)
        else:
            pos_unidad = aleatorio.randint(0, len(flujo_total)-1)
            pos_localizacion = aleatorio.randint(0, len(flujo_total)-1)
        unidad = flujo_total[pos_unidad][0]
        del flujo_total[pos_unidad]
        localizacion = distancia_total[pos_localizacion][0]
        del distancia_total[pos_localizacion]
        asignacion[unidad] = localizacion


    # print("Asignación final (unidad -> localización):")
    # for unidad in range(tam):
    #     print(f"Unidad {unidad+1} -> Localización {asignacion[unidad]+1}")

    return asignacion