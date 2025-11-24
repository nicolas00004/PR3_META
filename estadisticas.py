class Estadisticas:
    def __init__(self, archivo):
        self.archivo = archivo
        # Crea el archivo de log si no existe
        with open(self.archivo, "w", encoding="utf-8") as f:
            f.write("")

    def write(self, valor):
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(valor + "\n")
    def nuevo_punto(self, x, y):
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(f"{x};{y}\n")