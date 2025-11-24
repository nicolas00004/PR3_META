import estadisticas
import extraccion_Datos
import random
import AlgGen_Clase1_Grupo9
import algoritmo_memetico
import time
import logs
import os

if __name__ == "__main__":

    configuracion=extraccion_Datos.cargar_param("parametros.txt")
    semilla_original, k, archivos_Dat, num_sol, num_sol_greedy, num_ejecuciones, iteraciones, n_elite, k_best, k_worst, prob_mutacion, tiempo_max, operador_cruce, probabilidad_cruce,n_eval_tabu,n_iter_tabu = extraccion_Datos.cargar_datos(
        configuracion)

    semilla = semilla_original

    for i in range(num_ejecuciones):

        print("----------Ejecucion numero: ", i,"-----------------")

        semilla = extraccion_Datos.permutar_semilla_circular(semilla)
        for archivo in archivos_Dat:
            nombre_archivo = os.path.basename(archivo).split(".")[0]
            log = logs.Logs(f"logs/{"MEMETICO"}_cruce_{operador_cruce}_m_{num_sol}_e_{n_elite}_kbest_{k_best}_kworst_{k_worst}_{nombre_archivo}_ejecucion_{i}.txt")
            estadistica = estadisticas.Estadisticas(
                f"estadisticas/{"MEMETICO"}_cruce_{operador_cruce}_e_{n_elite}_kbest_{k_best}_{nombre_archivo}_ejecucion_{i}.csv")
            comienzo_aleatorio = time.time()
            aleatorio = random.Random(semilla)

            tam, flujo, distancias = extraccion_Datos.extraccion_Archivo(archivo)
            log.log_parametros("memetico", nombre_archivo, semilla, cruce=operador_cruce, M=num_sol, E=n_elite,
                               Kbest=k_best, Kworst=k_worst, Prob_mut=prob_mutacion, Prob_cruce=probabilidad_cruce)
            solucion,iteraciones = algoritmo_memetico.algoritmo_memetico(tam, k, num_sol,
                                                                                         num_sol_greedy,
                                                                                         flujo, distancias,
                                                                                         aleatorio,
                                                                                         iteraciones,
                                                                                         n_elite, k_best,
                                                                                         k_worst,
                                                                                         prob_mutacion,
                                                                                         tiempo_max,
                                                                                         operador_cruce,
                                                                                         probabilidad_cruce,log,n_eval_tabu,n_iter_tabu)

            duracion = time.time() - comienzo_aleatorio
            log.log_solucion_final(solucion.asignacion, solucion.coste, duracion)

            print("Solucion encontrada: ", solucion.asignacion)
            print("La mejor solucion encontrada tiene un coste de: ", solucion.coste)
            print("Iteraciones: ", iteraciones)
            duracion = time.time() - comienzo_aleatorio
            print("La duracion es:", duracion)

