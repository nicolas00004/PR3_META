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
    semilla_original, k, archivos_Dat, algoritmos, num_sol, num_sol_greedy, num_ejecuciones, iteraciones, n_elite, k_best, k_worst, prob_mutacion, tiempo_max, operador_cruce, probabilidad_cruce = extraccion_Datos.cargar_datos(
        configuracion)

    for algoritmo in algoritmos:

        match algoritmo:

            case "EVOLUTIVO_GENERACIONAL":

                print("---------------Algoritmo EVOLUTIVO_GENERACIONAL---------------")
                semilla = semilla_original

                for i in range(num_ejecuciones):

                    print("----------Ejecucion numero: ", i,"-----------------")

                    semilla = extraccion_Datos.permutar_semilla_circular(semilla)
                    for archivo in archivos_Dat:
                        nombre_archivo = os.path.basename(archivo).split(".")[0]
                        log = logs.Logs(f"logs/{algoritmo}_cruce_{operador_cruce}_m_{num_sol}_e_{n_elite}_kbest_{k_best}_kworst_{k_worst}_{nombre_archivo}_ejecucion_{i}.txt")
                        estadistica = estadisticas.Estadisticas(
                            f"estadisticas/{algoritmo}_cruce_{operador_cruce}_e_{n_elite}_kbest_{k_best}_{nombre_archivo}_ejecucion_{i}.csv")
                        comienzo_aleatorio = time.time()
                        aleatorio = random.Random(semilla)

                        tam, flujo, distancias = extraccion_Datos.extraccion_Archivo(archivo)
                        log.log_parametros(algoritmo, nombre_archivo, semilla, cruce=operador_cruce, M=num_sol, E=n_elite,
                                           Kbest=k_best, Kworst=k_worst, Prob_mut=prob_mutacion, Prob_cruce=probabilidad_cruce)
                        solucion,iteraciones = AlgGen_Clase1_Grupo9.algortimo_evolutivo_generacional(tam, k, num_sol,
                                                                                                     num_sol_greedy,
                                                                                                     flujo, distancias,
                                                                                                     aleatorio,
                                                                                                     iteraciones,
                                                                                                     n_elite, k_best,
                                                                                                     k_worst,
                                                                                                     prob_mutacion,
                                                                                                     tiempo_max,
                                                                                                     operador_cruce,
                                                                                                     probabilidad_cruce,log, estadistica)

                        duracion = time.time() - comienzo_aleatorio
                        log.log_solucion_final(solucion.asignacion, solucion.coste, duracion)

                        print("Solucion encontrada: ", solucion.asignacion)
                        print("La mejor solucion encontrada tiene un coste de: ", solucion.coste)
                        print("Iteraciones: ", iteraciones)


                        print("La duracion es:", duracion)

            case "EVOLUTIVO_ESTACIONARIO":

                print("---------------Algoritmo EVOLUTIVO_ESTACIONARIO---------------")
                semilla = semilla_original

                for i in range(num_ejecuciones):

                    print("----------Ejecucion numero: ", i, "-----------------")

                    semilla = extraccion_Datos.permutar_semilla_circular(semilla)
                    for archivo in archivos_Dat:
                        nombre_archivo = os.path.basename(archivo).split(".")[0]
                        log = logs.Logs(f"logs/{algoritmo}_cruce_{operador_cruce}_m_{num_sol}_e_{n_elite}_kbest_{k_best}_kworst_{k_worst}_{nombre_archivo}_ejecucion_{i}.txt")

                        estadistica = estadisticas.Estadisticas(f"estadisticas/{algoritmo}_cruce_{operador_cruce}_e_{n_elite}_kbest_{k_best}_{nombre_archivo}_ejecucion_{i}.csv")

                        comienzo_aleatorio = time.time()
                        aleatorio = random.Random(semilla)

                        tam, flujo, distancias = extraccion_Datos.extraccion_Archivo(archivo)

                        log.log_parametros(algoritmo, nombre_archivo, semilla, cruce=operador_cruce, M=num_sol,
                                           E=n_elite,
                                           Kbest=k_best, Kworst=k_worst, Prob_mut=prob_mutacion,
                                           Prob_cruce=probabilidad_cruce)

                        solucion, iteraciones = AlgEst_Clase1_Grupo9.algortimo_evolutivo_estacionario(tam,
                                                                                                                  k,
                                                                                                                  num_sol,
                                                                                                                  num_sol_greedy,
                                                                                                                  flujo,
                                                                                                                  distancias,
                                                                                                                  aleatorio,
                                                                                                                  iteraciones,
                                                                                                                  k_best,
                                                                                                                  k_worst,
                                                                                                                  prob_mutacion,
                                                                                                                  tiempo_max,
                                                                                                                  operador_cruce,
                                                                                                                  probabilidad_cruce,
                                                                                                                  log)
                        print("Solucion encontrada: ", solucion.asignacion)
                        print("La mejor solucion encontrada tiene un coste de: ", solucion.coste)
                        print("Iteraciones: ", iteraciones)

                        duracion = time.time() - comienzo_aleatorio
                        print("La duracion es:", duracion)
                        log.log_solucion_final(solucion.asignacion, solucion.coste, duracion)
