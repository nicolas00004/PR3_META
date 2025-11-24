import os
import numpy as np


def permutar_semilla_circular(semilla_actual):
    """
    Realiza un desplazamiento circular a la izquierda de los dígitos de la semilla.

    Ejemplo: 1658743 -> 6587431
    """
    # 1. Convertir el entero a una cadena para manipular los dígitos
    semilla_str = str(semilla_actual)

    # 2. Extraer el primer dígito
    primer_digito = semilla_str[0]

    # 3. Obtener el resto de la cadena (desde el segundo dígito hasta el final)
    resto_digitos = semilla_str[1:]

    # 4. Concatenar: poner el resto delante del primer dígito
    nueva_semilla_str = resto_digitos + primer_digito

    # 5. Convertir la nueva cadena de vuelta a un entero y devolverla
    nueva_semilla = int(nueva_semilla_str)

    return nueva_semilla

def cargar_param(nombre_archivo):
    configuracion = {}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if '=' in linea:
                # Divide la línea en clave y valor
                clave, valor = linea.split('=', 1)
                configuracion[clave.strip()] = valor.strip()
    return configuracion


def cargar_datos(archivo):
    """
    Args:
        nombre_archivo (str): La ruta del archivo a cargar.

    Return:
        n (int): El tamaño del problema.
        flujos (np_array): Una lista de listas (matriz) con los datos de flujo.
        distancias (np_array): Una lista de listas (matriz) con los datos de distancia.
    """
    semilla = archivo['Semilla']
    k = archivo['K']
    k1=int(k)
    n_sol=archivo['tam_poblacion']
    num_sol=int(n_sol)
    sol_gre=archivo['n_Sol_Greedy']
    num_gre=float(sol_gre)
    num_ejecuciones = int(archivo['n_ejecuciones'])
    iteraciones=int(archivo['iteraciones'])
    n_elite=int(archivo['E'])
    k_best=int(archivo['kbest'])
    k_worst=int(archivo['kworst'])
    prob_mutacion=float(archivo['prob_mutacion'])
    t_max=int(archivo['t_max'])
    operador_cruce=archivo['operador_cruce']
    probabilidad_cruce=float(archivo['probabilidad_cruce'])
    ruta = archivo['DATA']
    n_eval_tabu=archivo['n_eval_tabu']
    n_eval_tabu=int(n_eval_tabu)
    n_iter_tabu=archivo['n_iter_tabu']
    n_iter_tabu=int(n_iter_tabu)
    archivos_dat = []


    for archivo in os.listdir(ruta):
        if archivo.endswith(".dat"):
            archivos_dat.append(os.path.join(ruta, archivo))

    return semilla, k1, archivos_dat,num_sol,num_gre, num_ejecuciones,iteraciones,n_elite,k_best,k_worst,prob_mutacion,t_max, operador_cruce, probabilidad_cruce,n_eval_tabu,n_iter_tabu


def extraccion_Archivo( nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            # 1. Leer el tamaño del problema (n)
            n_str = archivo.readline().strip()

            n = int(n_str)

            # 2. Leer la línea en blanco
            archivo.readline()

            # 3. Leer la matriz de flujos
            flujos = []
            for _ in range(n):
                linea = archivo.readline().strip()
                # Convertir los valores a enteros (asumiendo que los datos son numéricos)
                fila = [int(x) for x in linea.split()]
                flujos.append(fila)
            m_flujos = np.array(flujos)
            # 4. Leer la línea en blanco
            archivo.readline()

            # 5. Leer la matriz de distancias
            distancias = []
            for _ in range(n):
                linea = archivo.readline().strip()
                fila = [int(x) for x in linea.split()]
                distancias.append(fila)
            m_distancias = np.array(distancias)

        return n, m_flujos, m_distancias
    except FileNotFoundError:
        print("Error: El fichero no existe.")
    except Exception as e:
        print(f"Error al leer el fichero: {e}")
