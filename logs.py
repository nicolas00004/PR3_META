from datetime import datetime

class Logs:
    def __init__(self, archivo):
        self.archivo = archivo
        # Crea el archivo de log si no existe
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.write(f"--- Log iniciado el {self._obtener_tiempo()} ---\n")

    def _obtener_tiempo(self):
        # Devuelve la fecha y hora actual en formato legible
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, mensaje, nivel="INFO"):
        # Guarda un mensaje en el archivo de log con un nivel de severidad
        linea = f"[{self._obtener_tiempo()}] [{nivel}] {mensaje}\n"
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(linea)

    def log_parametros(self, nombre_algoritmo, fichero, semilla, **kwargs):
        """Guarda los parámetros iniciales del experimento."""
        self.log(f"Comenzando ejecución del fichero: {fichero} con el algoritmo: {nombre_algoritmo}", "SETUP")
        self.log(f"  Parámetros del algoritmo", "SETUP")
        self.log(f"  Semilla: {semilla}", "SETUP")
        for k, v in kwargs.items():
            self.log(f"  {k}: {v}", "SETUP")
        self.log("--", "SETUP")

    def log_solucion_inicial(self, solucion, coste):
        """Registra la solución final."""
        self.log("Solución incicial:", "RESULT")
        self.log(f"  {solucion}", "RESULT")
        self.log(f"Coste inicial: {coste}", "RESULT")



    def log_solucion_final(self, solucion, coste, tiempo_total):
        """Registra la solución final."""
        self.log("Solución final:", "RESULT")
        self.log(f"  {solucion}", "RESULT")
        self.log(f"Coste final: {coste}", "RESULT")
        self.log(f"Tiempo total: {tiempo_total:.3f} s", "RESULT")
        self.log("=== FIN DE EJECUCIÓN ===", "RESULT")

    def log_movimiento(self, iteracion, pos_i, pos_j, solucion, coste, es_mejora):
        """
        Registra un movimiento realizado durante la búsqueda tabú.

        Args:
            iteracion: Número de iteración actual
            pos_i: Primera posición del intercambio (-1 si es movimiento al mejor vecino)
            pos_j: Segunda posición del intercambio (-1 si es movimiento al mejor vecino)
            solucion: Solución actual después del movimiento
            coste: Coste de la solución actual
            es_mejora: True si el movimiento mejora la mejor solución global
        """
        if pos_i == -1 and pos_j == -1:
            # Movimiento especial: se acepta el mejor vecino cuando DLB está completo
            mensaje = f"Iteración {iteracion}: Movimiento al mejor vecino (DLB completo)"
        else:
            # Movimiento normal: intercambio 2-opt
            mensaje = f"Iteración {iteracion}: Intercambio pos [{pos_i} ↔ {pos_j}]"

        # Indicar si es una mejora de la mejor solución global
        if es_mejora:
            mensaje += " ✓ NUEVA MEJOR SOLUCIÓN"

        self.log(mensaje, "TABU")
        self.log(f"  Solución: {solucion}", "TABU")
        self.log(f"  Coste: {coste}", "TABU")