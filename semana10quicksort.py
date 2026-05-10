"""
Semana 10 — Quick Sort y Veredicto StreamMX
Estructura de Datos Básica · UAN · LSC
Dr. Eligardo Cruz Sánchez
Equipo: [nombres del equipo]
Fecha: [fecha de la sesión]
"""

import time
import random
import copy


# ──────────────────────────────────────────────────────────────────────
#  EVIDENCIAS DE COMPRENSIÓN (llenar ANTES de codificar)
# ──────────────────────────────────────────────────────────────────────

# COMPRENDE-1: ¿Cuál es el invariante del pivote en Lomuto?
# Que el pivote siempre sera el ultimo elemento del arreglo


# COMPRENDE-2: ¿Cuándo y por qué Quick Sort degenera a O(n²)?
# cuando el arreglo ya esta ordenado o cuando los elementos son iguales
# ya que aunque aun que este acomodado el arreglo se terminan haciendo 
# muchas llamadas recursivas

# COMPRENDE-3: ¿Por qué Quick Sort es inestable y Merge Sort estable?
# por que quick sort solo compara valores y no le importan las posiciones

# ESTRATEGIA: Describe brevemente el plan del equipo para el benchmark
# usar el algoritmo de ordenamiento quick sort en vez del merge para 
#manejar mejor los recursos


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 1 — QUICK SORT (partición Lomuto)
# ──────────────────────────────────────────────────────────────────────

def particionar_lomuto(A, izq, der):
    """
    Particiona A[izq..der] usando Lomuto.
    El pivote es A[der] (último elemento).
    Retorna el índice final del pivote.
    """
    # DECISIÓN: describe aquí por qué el pivote es el último elemento
    # Por que estamos usando lomuto
    
    pivote = A[der]
    i = izq - 1

    for j in range(izq, der):
        # TODO: si A[j] <= pivote, incrementar i e intercambiar A[i] con A[j]
        if A[j] <= pivote:
            i+=1
            A[i], A[j] =A[j], A[i]
        pass

    # TODO: colocar el pivote en su posición definitiva (intercambiar A[i+1] con A[der])
    A[i+1], A[der] = A[der], A[i+1]
    # TODO: retornar el índice del pivote
    return i+1

    pass


def quick_sort(A, izq=None, der=None):
    """
    Quick Sort recursivo sobre A[izq..der].
    Llama a particionar_lomuto para obtener el índice del pivote.
    """
    if izq is None:
        izq = 0
    if der is None:
        der = len(A) - 1

    if izq < der:
        # TODO: obtener el índice del pivote usando particionar_lomuto
        p= particionar_lomuto (A, izq, der)
        # TODO: llamar recursivamente sobre A[izq..p-1] y A[p+1..der]
        quick_sort(A, izq, p -1 )
        quick_sort(A,p + 1, der)
        pass 


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 2 — EXPERIMENTO DE ESTABILIDAD
# ──────────────────────────────────────────────────────────────────────

# Datos simulados StreamMX: tuplas (puntaje, titulo, fecha_subida)
datos_streamx = [
    (7.5, "El Laberinto", "lunes"),
    (8.2, "Interestelar", "lunes"),
    (7.5, "La Señal", "martes"),
    (9.1, "Origen", "lunes"),
    (7.5, "Gravedad", "miércoles"),
    (8.2, "Tenet", "martes"),
    (7.5, "Dune", "jueves"),
]

# -------------------------
# MERGE SORT 
# -------------------------
def merge_sort(lista, clave=lambda x: x):
    if len(lista) <= 1:
        return lista[:]

    medio = len(lista) // 2
    izq = merge_sort(lista[:medio], clave)
    der = merge_sort(lista[medio:], clave)
    return mezclar(izq, der, clave)

def mezclar(izq, der, clave):
    res = []
    i = j = 0


    while i < len(izq) and j < len(der):
        if clave(izq[i]) <= clave(der[j]):
            res.append(izq[i])
            i += 1
        else:
            res.append(der[j])
            j += 1

    res.extend(izq[i:])
    res.extend(der[j:])
    return res


# -------------------------
# QUICK SORT 
# -------------------------
def particionar_lomuto(A, izq, der, clave):
    pivote = clave(A[der])
    i = izq - 1

    for j in range(izq, der):
        if clave(A[j]) <= pivote:
            i += 1
            A[i], A[j] = A[j], A[i]

    A[i + 1], A[der] = A[der], A[i + 1]
    return i + 1

def quick_sort(A, izq=0, der=None, clave=lambda x: x):
    if der is None:
        der = len(A) - 1

    if izq < der:
        p = particionar_lomuto(A, izq, der, clave)
        quick_sort(A, izq, p - 1, clave)
        quick_sort(A, p + 1, der, clave)

        

# -------------------------
# SALIDA: ordenar por puntaje
# -------------------------

ordenado_merge = merge_sort(datos_streamx, clave=lambda t: t[0])

datos_quick = datos_streamx[:]          # copia para no modificar el original
quick_sort(datos_quick, clave=lambda t: t[0])

print("Original:")
for x in datos_streamx:
    print(x)

print("\nMerge sort (estable) por puntaje:")
for x in ordenado_merge:
    print(x)

print("\nQuick sort (Lomuto) por puntaje (puede reordenar empates):")
for x in datos_quick:
    print(x)

def verificar_estabilidad(datos_originales, datos_ordenados, campo_clave=0):
    """
    Verifica si el ordenamiento preservó el orden relativo de elementos
    con el mismo valor en campo_clave.
    Retorna (True, "") si es estable, (False, detalle) si no.

    FUNCIÓN PROVISTA — no modificar. El equipo la usa, no la implementa.
    """
    from collections import defaultdict

    # Índices de cada elemento en el arreglo original (por valor de clave)
    orden_original = defaultdict(list)
    for idx, elemento in enumerate(datos_originales):
        clave = elemento[campo_clave] if isinstance(elemento, (list, tuple)) else elemento
        orden_original[clave].append(idx)

    # Recorrer el arreglo ordenado y verificar que los índices originales
    # de elementos con la misma clave aparecen en orden creciente
    posicion_en_original = defaultdict(int)  # puntero por clave
    for elemento in datos_ordenados:
        clave = elemento[campo_clave] if isinstance(elemento, (list, tuple)) else elemento
        grupo = orden_original[clave]
        ptr = posicion_en_original[clave]
        if ptr >= len(grupo):
            return False, f"Clave {clave}: más ocurrencias en ordenado que en original"
        posicion_en_original[clave] += 1

    # Verificar que el orden relativo dentro de cada grupo es creciente
    posicion_en_original = defaultdict(int)
    ultimo_idx = defaultdict(lambda: -1)
    for elemento in datos_ordenados:
        clave = elemento[campo_clave] if isinstance(elemento, (list, tuple)) else elemento
        ptr = posicion_en_original[clave]
        idx_original = orden_original[clave][ptr]
        if idx_original <= ultimo_idx[clave]:
            detalle = (f"Inestabilidad detectada en clave '{clave}': "
                       f"elemento con índice original {idx_original} aparece "
                       f"después de elemento con índice {ultimo_idx[clave]}")
            return False, detalle
        ultimo_idx[clave] = idx_original
        posicion_en_original[clave] += 1

    return True, "Ordenamiento estable: orden relativo preservado en todos los grupos"


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 3 — BENCHMARK COMPARATIVO (MS de S9 vs QS de S10)
# ──────────────────────────────────────────────────────────────────────

def generar_distribucion(n, tipo):
    """
    Genera un arreglo de n enteros según la distribución indicada.
    tipo: 'aleatorio' | 'ordenado' | 'inverso' | 'duplicados'
    """
    if tipo == 'aleatorio':
        return [random.randint(1, n) for _ in range(n)]
    elif tipo == 'ordenado':
        return list(range(n))
    elif tipo == 'inverso':
        return list(range(n, 0, -1))
    elif tipo == 'duplicados':
        # Generador provisto — no modificar.
        # Simula millones de empates de puntaje en StreamMX:
        # el 80% del arreglo es el número 7 (valor arbitrario fijo),
        # el 20% restante son enteros aleatorios en [1, n].
        # Se mezcla para evitar que la zona de duplicados quede agrupada.
        base  = [7] * int(n * 0.8)
        ruido = [random.randint(1, n) for _ in range(n - len(base))]
        arreglo = base + ruido
        random.shuffle(arreglo)
        return arreglo
    else:
        raise ValueError(f"Distribución desconocida: {tipo}")


def medir_tiempo(funcion, arreglo):
    """
    Ejecuta funcion sobre una copia de arreglo y retorna el tiempo en segundos.
    """
    copia = copy.deepcopy(arreglo)
    inicio = time.perf_counter()
    funcion(copia)
    fin = time.perf_counter()
    return fin - inicio


# TODO: copiar merge_sort de la entrega de Semana 9
# Importar Merge Sort de S9 (pegar la implementación aquí si es necesario)
def merge_sort(A):
    """
    [Pegar aquí la implementación completa de Merge Sort de S9]
    """
    
def merge_sort(arr):
    
    if len(arr) <= 1:
        return arr[:]  # copia para no depender del original

    medio = len(arr) // 2
    izquierda = merge_sort(arr[:medio])
    derecha = merge_sort(arr[medio:])

    return mezclar(izquierda, derecha)


def mezclar(izquierda, derecha):
    
    resultado = []
    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar lo que falte (solo una de estas dos tendrá elementos)
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado



    
def ejecutar_benchmark():
    """
    Ejecuta el benchmark completo y muestra una tabla comparativa.

    NOTA PEDAGÓGICA — límite de recursión:
    Python limita la pila de llamadas a ~1000 frames por defecto.
    Con ese límite, n=1000 ordenado crashea INSTANTÁNEAMENTE,
    lo que impide distinguir 'programa lento por O(n²)' de
    'programa muerto por O(n) de pila (Stack Overflow)'.

    Para separar empíricamente Complejidad Temporal de Complejidad
    Espacial, aumentamos el límite temporalmente:
      - n=10,000 arreglo ordenado → programa congelado varios segundos  → O(n²) en TIEMPO
      - n=100,000 arreglo ordenado → RecursionError / crash              → O(n)  en ESPACIO (pila)

    Ese contraste es el hallazgo central del experimento.
    """
    import sys
    sys.setrecursionlimit(110_000)   # permite sentir O(n²) antes de colapsar por pila

    tamanos = [1_000, 10_000, 100_000]
    distribuciones = ['aleatorio', 'ordenado', 'inverso', 'duplicados']

    print("=" * 85)
    print(f"{'n':>10} | {'Distribución':>12} | {'Merge Sort (s)':>18} | {'Quick Sort (s)':>18}")
    print("=" * 85)

    for n in tamanos:
        for dist in distribuciones:
            A = generar_distribucion(n, dist)

            t_ms = medir_tiempo(merge_sort, A)

            # Quick Sort puede crashear con RecursionError en peor caso
            try:
                t_qs = medir_tiempo(quick_sort, A)
                resultado_qs = f"{t_qs:>18.4f}"
            except RecursionError:
                resultado_qs = f"{'CRASH (Stack Overflow)':>18}"

            print(f"{n:>10} | {dist:>12} | {t_ms:>18.4f} | {resultado_qs}")
        print("-" * 85)

    # REFLEXIONA-1: ¿En qué distribución Quick Sort fue MÁS lento o crasheó?
    # Donde fue mas lento definitivamente fue en los datos ordenados, aunque 
    # probablemente con una mayor cantidad de n elementos crashearia
    

    # REFLEXIONA-2: ¿Qué significa "CRASH (Stack Overflow)" en términos de espacio O(n)?
    # [Pista: ¿cuántos frames de recursión crea Lomuto con n=1000 arreglo ordenado?]
    #Significa que el programa hizo demasiadas llamadas recursivas haciendo que la 
    #pila de llamadas se llene y supere su limite, lo que haria que crasheara


    # REFLEXIONA-3: Con estos datos, ¿qué recomendarías a la Ing. Sofía para cada distribución?
    # que solamente utilice quicksort con datos aleatorios (y mas si datos grandes)


if __name__ == "__main__":
    # Sección 1: Verificar que Quick Sort ordena correctamente
    prueba = [9, 3, 7, 1, 5, 8, 2, 4, 6]
    quick_sort(prueba)
    print("Prueba básica:", prueba)
    assert prueba == sorted([9, 3, 7, 1, 5, 8, 2, 4, 6]), "Quick Sort falla en prueba básica"

    # Sección 2: Experimento de estabilidad
    # La función verificar_estabilidad() ya está implementada — úsala:
    # TODO: crear una copia ordenada de datos_streamx con merge_sort (por campo 0 = puntaje)
    # TODO: crear otra copia ordenada con quick_sort
    # TODO: llamar verificar_estabilidad(datos_streamx, copia_ms) y mostrar resultado
    # TODO: llamar verificar_estabilidad(datos_streamx, copia_qs) y mostrar resultado
    # TODO: imprimir las películas con puntaje 7.5 en ambos resultados y comparar el orden

    # Sección 3: Benchmark
    ejecutar_benchmark()
    #quick sort es mas rapido cuando se trata de datos aleatorios, pero cuando
    #hablamos de datos ordenados, inversos o duplicados merge termina siendo mejor

    # ──────────────────────────────────────────────────────────────────────
    #  VALIDA: VEREDICTO STREAMMX — EQUIPO [NOMBRE]
    #
    #  DISTRIBUCIÓN A — Rankings casi ordenados (pocos cambios del día anterior):
    #  Algoritmo recomendado: [Merge Sort / Quick Sort + estrategia de pivote]
    #  Razón tiempo:       t_MS=[0.2239]s vs t_QS=[5.1064]s con n=100000
    #  Razón espacio:      [merge sort requiere memoria adiciona mientras que QS es in-place pero es mas inestable]
    #  Razón estabilidad:  [Si es que el orden cronologico debe preservarse MS es mejor]
    #  Razón duplicados:   [No esta garantizado el empate en posiciones]
    #
    #  DISTRIBUCIÓN B — Datos frescos aleatorios (flujo del día):
    #  Algoritmo recomendado: [quick sort]
    #  Razón tiempo:       [quick sort tiene buen rendimiento con datos aleatorios]
    #  Razón espacio:      [quick sort trabaja in-place]
    #  Razón estabilidad:  [a pesar de que usualmente qs no es estable, escala muy bien con datos aleatorios]
    #
    #  DISTRIBUCIÓN C — Millones de empates en puntaje (caso crítico):
    #  Algoritmo recomendado: [merge sort]
    #  Razón tiempo:       [con tantos datos y empates es mejor mg por que mantiene n log n ]
    #  Razón espacio:      [si bien mg requiere memoria adicional, considero que de todas formas es la mejor opcion]
    #  Razón duplicados:   [si se usa lomuto puro se harian comparaciones e intercambios innecesarios, lo que bajaria el rendimiento]
    #
    #  CONCLUSIÓN GENERAL:
    #  [1-2 oraciones con la recomendación técnica completa para la Ing. Sofía]
    # considero que es mejor seguir usando mg, ya que si bien en otro caso qs seria mas eficaz,
    #al tener millones de duplicados usar qs haria que baje el rendimiento teniendo una complejidad (en el peor de los casos)
    #de  O(n²)
    # ──────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────
#  FASE 1: COMPRENDE
# ──────────────────────────────────────────────────────────────────────
# IA-REFLEXION-C: [máximo 3 líneas: qué descubrió el equipo mediante el diálogo socrático]
# Que quick sort suele ser muy inestable pero es mas rapido y consume menos RAM
# que el merge sort y suele venir bien cuando tienes un arreglo desordenado
# y cuando quieres cuidar la memoria
# ──────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────
#  FASE 2: APLICA
# ──────────────────────────────────────────────────────────────────────

# IA-REFLEXION-A: [máximo 3 líneas sobre qué aclaró la IA
# y qué implementó el equipo sin ayuda]
# i y j no son como parte del pivote, sino que  pero son las iteraciones que
# dejan el pivote en su lugar al final

# ──────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────
#  FASE 3: REFLEXIONA
# ──────────────────────────────────────────────────────────────────────
# IA-REFLEXION-R: [máximo 3 líneas: ¿qué ítem les costó más trabajo y qué
#  necesitan repasar antes de la defensa real?]

# lo que me costo mas trabajo fue tratar de defender mis argumentos
# ya que termine siendo algo ambiguo a la hora de explicarme, solo tengo que
#tener mas en claro lo que voy a decir
# ──────────────────────────────────────────────────────────────────────

#──────────────────────────────────────────────────────────────────────
#  FASE 4: VALIDA
# ─────────────────────────────────────────────────────────────────────
#  IA-REFLEXION-V: [máximo 3 líneas: ¿encontraron errores con los casos
#  adversariales? ¿Cuál fue el más revelador?]

#el error destacable que tuve fue el de llegar al maximo de recursiones en python,
#lo que me marcaba un error en la terminal 

# ──────────────────────────────────────────────────────────────────────


#──────────────────────────────────────────────────────────────────────
#  FASE 5: PROFUNDIZA
# ─────────────────────────────────────────────────────────────────────
# IA-REFLEXION-P: [máximo 3 líneas: ¿qué pregunta de S11 le queda pendiente
#  al equipo después de este diálogo?]

#¿como es que se muestran estas búsquedas en un sitio cotidiano como una pagina web?


# ─────────────────────────────────────────────────────────────────────