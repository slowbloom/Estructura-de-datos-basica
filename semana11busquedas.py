"""
Semana 11 — Búsqueda Lineal, Binaria y HITO 2
Estructura de Datos Básica · UAN · LSC
Dr. Eligardo Cruz Sánchez
Equipo: [nombres del equipo]
Fecha: [fecha de la sesión]
"""

import time
import random
import copy
import sys


# ──────────────────────────────────────────────────────────────────────
#  EVIDENCIAS DE COMPRENSIÓN (llenar ANTES de codificar)
# ──────────────────────────────────────────────────────────────────────

# COMPRENDE-1: Enuncia el invariante de búsqueda binaria con tus palabras.
#              ¿Qué garantiza en cada iteración del bucle while?
# nunca se pierde de vista el elemento buscado, sino que se va acotando mas y mas el arreglo pero sin perder el elemento de vista

# COMPRENDE-2: ¿Cuántas comparaciones hace búsqueda binaria en el peor caso
#              para n = 1 000 000? Muestra el cálculo: ⌊log₂(n)⌋ + 1
# sustituyendo n por 1000000 tenemos al final una division que es 6/0.30103 lo que nos da 19.93 por
# lo que podemos decir que se hacen 20 comparaciones

# COMPRENDE-3: ¿Por qué búsqueda binaria requiere arreglo ordenado?
#              Da un contraejemplo concreto donde falla si no está ordenado.
# se necesita que este ordenado el arreglo por que se basa en comparar el elemento del medio con el valor buscado. si no esta ordenado el arreglo podria no tomar en cuenta elementos clave

# ESTRATEGIA: Describe brevemente el plan del equipo para el HITO 2
#             (qué algoritmo de ordenamiento eligieron del Veredicto y por qué)
# implementar una busqueda binaria para que en el peor de los casos se generen 23 comparaciones sobre 5 millones de registros

# ──────────────────────────────────────────────────────────────────────
#  IMPORTAR CÓDIGO DE S9 Y S10
#  (pegar aquí las implementaciones que ya pasaron sus pruebas)
# ──────────────────────────────────────────────────────────────────────

def merge_sort(A):
    """[Pegar aquí la implementación de Merge Sort de S9]"""
    pass  # TODO: copiar de entrega S9
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



def quick_sort(A, izq=None, der=None):
    """[Pegar aquí la implementación de Quick Sort de S10]"""
    pass  # TODO: copiar de entrega S10
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


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 1 — BÚSQUEDA LINEAL
# ──────────────────────────────────────────────────────────────────────

def busqueda_lineal(A, objetivo):
    # TODO: implementar búsqueda lineal
   
      for i, elemento in enumerate(A):
        if elemento == objetivo:
            return i


      return -1
   
   
      """
    Recorre A de izquierda a derecha buscando objetivo.
    Retorna el índice de la primera ocurrencia, o -1 si no existe.
    No requiere que A esté ordenado.
    Complejidad: O(n) tiempo, O(1) espacio.
    """
    # DECISIÓN: ¿Por qué iterar con enumerate en lugar de range?
    # enumerate nos da el indice y el valor en cara iteracion que hace las cosas mas entendibles en vez de range

      pass


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 2 — BÚSQUEDA BINARIA (iterativa)
# ──────────────────────────────────────────────────────────────────────

def busqueda_binaria(A, objetivo):
    """
    Búsqueda binaria iterativa sobre A ordenado ascendentemente.
    Retorna el índice de una ocurrencia de objetivo, o -1 si no existe.
    PRECONDICIÓN: A debe estar ordenado.
    Complejidad: O(log n) tiempo, O(1) espacio.
    """
    # DECISIÓN: ¿Por qué usar mid = (izq + der) // 2 y no (izq + der) / 2?
    # por que el // es la division entera, lo que devuelve una posicion valida y no una decimal

    # MID-CANONICO: En C/Java la forma segura es izq + (der - izq) // 2
    #               porque izq + der puede desbordar un int de 32 bits
    #               (bug en el JDK de Java durante 20 años, 1986–2006).
    #               Python nos protege con enteros de precisión arbitraria,
    #               pero la forma canónica es un hábito profesional correcto.

    izq = 0
    der = len(A) - 1

    while izq <= der:
        # TODO: calcular mid (división entera)
        mid = izq + (der - izq) // 2 
        
        # TODO: si A[mid] == objetivo → retornar mid
        if A[mid] == objetivo:
            return mid
        
        # TODO: si A[mid] < objetivo  → mover izq = mid + 1
        elif A[mid] < objetivo:
            izq = mid +1
        # TODO: si A[mid] > objetivo  → mover der = mid - 1
        else: der = mid-1
        pass

    return -1  # No encontrado


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 3 — BENCHMARK COMPARATIVO
# ──────────────────────────────────────────────────────────────────────

def generar_arreglo_ordenado(n):
    """Genera un arreglo de n enteros ordenados (simulando catálogo ya ordenado)."""
    return list(range(n))


def medir_busqueda(funcion_busqueda, A, objetivo):
    """
    Ejecuta funcion_busqueda(A, objetivo) y retorna (tiempo_segundos, resultado).
    No copia el arreglo — búsqueda no modifica A.
    """
    inicio = time.perf_counter()
    resultado = funcion_busqueda(A, objetivo)
    fin = time.perf_counter()
    return fin - inicio, resultado


def ejecutar_benchmark_busqueda():
    """
    Benchmark: búsqueda lineal vs binaria sobre arreglos ordenados.
    Tres escenarios por tamaño: objetivo al inicio, al final, no existe.
    """
    tamanos = [1_000, 10_000, 100_000, 1_000_000]
    escenarios = [
        ('inicio',     lambda n: 0),           # mejor caso lineal, cualquiera binaria
        ('final',      lambda n: n - 1),        # peor caso lineal
        ('no_existe',  lambda n: n + 999),      # peor caso ambas
    ]

    print("=" * 90)
    print(f"{'n':>10} | {'Escenario':>10} | {'Lineal (s)':>13} | {'Binaria (s)':>13} | {'Factor':>8}")
    print("=" * 90)

    for n in tamanos:
        A = generar_arreglo_ordenado(n)
        for nombre_esc, get_objetivo in escenarios:
            objetivo = get_objetivo(n)
            t_lin, res_lin = medir_busqueda(busqueda_lineal, A, objetivo)
            t_bin, res_bin = medir_busqueda(busqueda_binaria, A, objetivo)

            # Verificar que ambas retornan el mismo resultado
            assert res_lin == res_bin, (
                f"DISCREPANCIA: lineal={res_lin}, binaria={res_bin} "
                f"para n={n}, objetivo={objetivo}"
            )

            factor = t_lin / t_bin if t_bin > 0 else float('inf')
            print(f"{n:>10} | {nombre_esc:>10} | {t_lin:>13.6f} | {t_bin:>13.6f} | {factor:>7.1f}x")
        print("-" * 90)

    # REFLEXIONA-1: ¿En qué escenario la diferencia de velocidad es mayor?
    # cuando el arreglo es demasiado grande se nota la diferencia

    # REFLEXIONA-2: ¿El "factor" de velocidad corresponde al ratio O(n)/O(log n)?
    #               Calculen el valor teórico para n=1_000_000: n / log2(n) ≈ ?
    # el valor es 50187 lo que significa que  la binaria es ese numero mas rapido que la busqueda lineal para el millon de numeros

    # REFLEXIONA-3: ¿Qué pasa si buscan el objetivo al INICIO con búsqueda lineal
    #               vs búsqueda binaria? ¿Cuál es más rápida y por qué?
    # gana la busqueda lineal por que va comparando elemento por elemento con el valor buscado y el valor buscado al estar al inicio nada mas haria una comparacion


def ejecutar_benchmark_duplicados():
    """
    Benchmark de conflicto cognitivo — Área crítica de StreamMX:
    Distribución C tiene millones de registros con el mismo puntaje.
    Mide el tiempo de buscar_por_puntaje con expansión lineal vs el rango
    que alcanzaría buscar_rango (Reto 6) sobre un arreglo con duplicados masivos.
    Objetivo: observar empíricamente la degradación a O(n) en el caso crítico.
    """
    import math

    print("\n" + "=" * 75)
    print("BENCHMARK DUPLICADOS MASIVOS — Distribución C de StreamMX")
    print("buscar_por_puntaje (expansión lineal) sobre distintas proporciones")
    print("=" * 75)
    print(f"{'n':>10} | {'% duplicados':>13} | {'buscar_por_puntaje (s)':>22} | {'Observación'}")
    print("-" * 75)

    casos = [
        (10_000,   10),    # 1 000 duplicados del mismo valor
        (10_000,   50),    # 5 000 duplicados — la mitad del arreglo
        (100_000,  50),    # 50 000 duplicados
        (100_000,  90),    # 90 000 duplicados — caso casi degenerado
    ]

    for n, pct in casos:
        num_dup = int(n * pct / 100)
        # Arreglo con num_dup copias del valor 500 y el resto distintos
        A = sorted([500] * num_dup + list(range(501, 501 + (n - num_dup))))
        t_inicio = __import__('time').perf_counter()
        resultados = buscar_por_puntaje(A, 500)
        t_fin = __import__('time').perf_counter()
        t = t_fin - t_inicio
        obs = "⚠️ LENTO" if t > 0.005 else "OK"
        print(f"{n:>10} | {pct:>12}% | {t:>22.6f} | {obs}")

    print("-" * 75)
    print()
    # REFLEXIONA-DUPLICADOS: ¿Cómo cambia el tiempo conforme aumenta el % de duplicados?
    #cuando aumenta el porcentaje de duplicados, el tiempo de la funcion buscar por puntaje tambien aumenta bastante

    # ¿Qué relación tiene esto con la degradación de O(log n) a O(n)?
    #que cuando hay muchos duplicados, para encontrar todos los elementos con ese valor la expansion puede requerir revisar una gran parte del arreglo, lo qye haria que el iempo se degrade a O(n)

    # ¿Por qué el Reto 6 (buscar_rango) resuelve este problema?
    # por ue utiliza dos busquedas binarias para encontrar las posiciones de inicio y fin donde ocurren los duplicados


# ──────────────────────────────────────────────────────────────────────
#  SECCIÓN 4 — PIPELINE HITO 2
# ──────────────────────────────────────────────────────────────────────

# Datos StreamMX simplificados: (puntaje_compuesto, titulo, id_pelicula)
catalogo_streamx = [
    (8.2, "Interestelar",    "MX-001"),
    (7.5, "El Laberinto",    "MX-002"),
    (9.1, "Origen",          "MX-003"),
    (6.8, "Dune Parte 1",    "MX-004"),
    (8.7, "Oppenheimer",     "MX-005"),
    (7.5, "La Señal",        "MX-006"),
    (9.4, "Everything E.E.", "MX-007"),
    (6.2, "Los Elegidos",    "MX-008"),
    (8.0, "The Batman",      "MX-009"),
    (7.5, "Gravedad",        "MX-010"),
    (9.0, "Parasite",        "MX-011"),
    (7.1, "Midsommar",       "MX-012"),
]


def ordenar_catalogo(catalogo, algoritmo='veredicto'):
    """
    Ordena el catálogo StreamMX por puntaje_compuesto (campo 0).
    algoritmo: 'merge_sort' | 'quick_sort' | 'veredicto'
    'veredicto' usa el algoritmo recomendado por el equipo en S10.
    """
    copia = copy.deepcopy(catalogo)

    # DECISIÓN: ¿Qué algoritmo eligió el equipo en el Veredicto StreamMX de S10?
    # Justificar aquí por qué este algoritmo es apropiado para esta distribución.
    # merge es mas apropiado por que es mas estable con un arreglo grande

    if algoritmo == 'merge_sort':
        # TODO: ordenar copia con merge_sort por campo 0 (puntaje)
        copia=merge_sort(copia)
        pass
    elif algoritmo == 'quick_sort':
        # TODO: ordenar copia con quick_sort por campo 0 (puntaje)
        copia = quick_sort(copia)
        pass
    elif algoritmo == 'veredicto':
        # TODO: usar el algoritmo recomendado en el Veredicto StreamMX del equipo
        copia = merge_sort(copia)
        pass

    return copia


def obtener_puntaje(item):
    # item puede ser (puntaje, titulo, id) o un número (puntaje)
    return item[0] if isinstance(item, (tuple, list)) else item

def buscar_por_puntaje(catalogo_ordenado, puntaje_objetivo):
    """
    Busca películas en el catálogo ordenado con el puntaje exacto.
    Usa búsqueda binaria para encontrar una ocurrencia, luego expande
    hacia ambos lados para encontrar todas (manejo de duplicados básico).
    Retorna lista de tuplas que coinciden, o lista vacía si no existe.
    """
    # TODO: usar busqueda_binaria para encontrar índice de una ocurrencia
    idx = busqueda_binaria(catalogo_ordenado,puntaje_objetivo)
    # TODO: si retorna -1, retornar []
    if idx == -1:
        return []
    # TODO: desde ese índice, expandir izquierda y derecha mientras el puntaje coincida
    inicio = idx
    while inicio - 1 >= 0 and catalogo_ordenado[inicio - 1][0] ==puntaje_objetivo:
       inicio -= 1

    fin =  idx
    while fin + 1 < len(catalogo_ordenado) and catalogo_ordenado[fin+1][0] == puntaje_objetivo:
     fin += 1
    # TODO: retornar todas las tuplas encontradas
    return catalogo_ordenado[inicio:fin+1]
    
    
    pass


def pipeline_hito2(catalogo, puntaje_buscar, algoritmo='veredicto'):
    """
    Pipeline completo HITO 2:
    1. Ordenar catálogo con el algoritmo del Veredicto StreamMX.
    2. Buscar películas con el puntaje dado usando búsqueda binaria.
    3. Retornar resultados y métricas de tiempo.
    """
    # Paso 1: Ordenar
    inicio_orden = time.perf_counter()
    catalogo_ordenado = ordenar_catalogo(catalogo, algoritmo)
    fin_orden = time.perf_counter()
    t_orden = fin_orden - inicio_orden

    # Paso 2: Buscar
    inicio_busqueda = time.perf_counter()
    resultados = buscar_por_puntaje(catalogo_ordenado, puntaje_buscar)
    fin_busqueda = time.perf_counter()
    t_busqueda = fin_busqueda - inicio_busqueda

    return {
        'catalogo_ordenado': catalogo_ordenado,
        'resultados': resultados,
        't_orden_s': t_orden,
        't_busqueda_s': t_busqueda,
        't_total_s': t_orden + t_busqueda,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS BÁSICAS — Sección 1 y 2")
    print("=" * 60)

    # Prueba búsqueda lineal
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    assert busqueda_lineal(A, 5) == 4, "Lineal: error en búsqueda exitosa"
    assert busqueda_lineal(A, 7) == -1, "Lineal: error en búsqueda fallida"
    print("Búsqueda lineal: OK")

    # Prueba búsqueda binaria
    B = sorted(A)  # [1, 1, 2, 3, 4, 5, 6, 9]
    idx = busqueda_binaria(B, 5)
    assert idx != -1 and B[idx] == 5, "Binaria: error en búsqueda exitosa"
    assert busqueda_binaria(B, 7) == -1, "Binaria: error en búsqueda fallida"
    print("Búsqueda binaria: OK")

    print("\n" + "=" * 60)
    print("BENCHMARK — Sección 3")
    print("=" * 60)
    ejecutar_benchmark_busqueda()

    print("\n" + "=" * 60)
    print("BENCHMARK DUPLICADOS — Sección 3b")
    print("=" * 60)
    ejecutar_benchmark_duplicados()

    print("\n" + "=" * 60)
    print("PIPELINE HITO 2 — Sección 4")
    print("=" * 60)
    resultado = pipeline_hito2(catalogo_streamx, puntaje_buscar=7.5)
    print(f"Catálogo ordenado (primeros 5): {resultado['catalogo_ordenado'][:5]}")
    print(f"Películas con puntaje 7.5: {resultado['resultados']}")
    print(f"Tiempo ordenar:  {resultado['t_orden_s']:.6f} s")
    print(f"Tiempo buscar:   {resultado['t_busqueda_s']:.6f} s")
    print(f"Tiempo total:    {resultado['t_total_s']:.6f} s")

    # VALIDA: ¿El pipeline retorna correctamente las 3 películas con puntaje 7.5?
    # no