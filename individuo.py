class Individuo:

    def __init__(self, asignacion):
        # self.asignacion (list[int]): vector de enteros que representa la solución.
        self.asignacion = asignacion

        # self.evaluado (bool): True si el individuo ya ha sido evaluado, False en caso contrario.
        self.evaluado = False

        # self.coste (int | None): Almacena el coste (fitness) del individuo.
        # Es None hasta que se calcula por primera vez.
        self.coste = None

    def evaluar(self, tam, matriz_flujo, matriz_distancia):
        """
            Calcula el coste de la asignación si no ha sido evaluado previamente.
        """
        if self.evaluado:
            return self.coste, 0
        else:
            coste_total = 0
            for i in range(tam):
                for j in range(tam):
                    coste_total += matriz_flujo[i, j] * matriz_distancia[self.asignacion[i], self.asignacion[j]]
            self.coste = coste_total
            self.evaluado = True
            return coste_total, 1

    def copiar(self):
        nuevo = Individuo(self.asignacion.copy())  # copia de la lista
        nuevo.evaluado = self.evaluado
        nuevo.coste = self.coste
        return nuevo