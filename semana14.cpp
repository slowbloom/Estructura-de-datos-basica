#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <algorithm>
#include <stdexcept>
#include <chrono>
#include <functional>
#include <random>
#include <iomanip>
#include <sstream>

using namespace std;
using namespace std::chrono;

// ============================
// StreamMX (Modelo simplificado)
// ============================

struct Pelicula {
    string id;
    string titulo;
    double puntaje;
};

// Nodo BST
struct NodoBST {
    double clave;
    vector<Pelicula> peliculas;
    NodoBST* izq;
    NodoBST* der;

    NodoBST(double c, const Pelicula& p)
        : clave(c), peliculas{p}, izq(nullptr), der(nullptr) {}
};

struct OperacionUndo {
    string idInsertado;
};

class SistemaMX {
public:
    unordered_map<string, Pelicula> catalogo;
    NodoBST* bst_raiz;
    vector<vector<Pelicula>> pilaResultados;
    vector<OperacionUndo> pilaUndo;

    SistemaMX() : bst_raiz(nullptr) {}

    ~SistemaMX() {
        liberarBST(bst_raiz);
    }

    // ============================
    // Inserción consistente
    // ============================
    bool agregar_contenido(const string& id,
                           const string& titulo,
                           double puntaje) {

        if (catalogo.find(id) != catalogo.end()) {
            throw invalid_argument("ID duplicado: " + id);
        }

        if (puntaje < 0.0 || puntaje > 10.0) {
            throw out_of_range("Puntaje fuera de rango");
        }

        Pelicula p{id, titulo, puntaje};

        // Hash
        catalogo.insert({id, p});

        // BST
        bst_raiz = bst_insertar(bst_raiz, p);

        // Undo
        pilaUndo.push_back({id});

        return true;
    }

    // ============================
    // Router / fachada
    // ============================
    vector<Pelicula> procesar_solicitud(const string& tipo,
                                        const string& paramStr = "",
                                        double minv = 0.0,
                                        double maxv = 0.0) {

        // LOOKUP
        if (tipo == "lookup") {
            vector<Pelicula> out;

            auto it = catalogo.find(paramStr);

            if (it != catalogo.end()) {
                out.push_back(it->second);
            }

            return out;
        }

        // RANGO
        if (tipo == "rango") {

            if (minv > maxv) {
                throw invalid_argument("Rango invalido");
            }

            vector<Pelicula> resultados;

            bst_rango(bst_raiz, minv, maxv, resultados);

            pilaResultados.push_back(resultados);

            return resultados;
        }

        // TOP10
        if (tipo == "top10") {

            if (pilaResultados.empty()) {
                throw runtime_error("Ejecuta rango primero");
            }

            vector<Pelicula> base = pilaResultados.back();

            sort(base.begin(), base.end(),
                 [](const Pelicula& a, const Pelicula& b) {

                if (a.puntaje != b.puntaje) {
                    return a.puntaje > b.puntaje;
                }

                return a.id < b.id;
            });

            if (base.size() > 10) {
                base.resize(10);
            }

            return base;
        }

        // UNDO
        if (tipo == "undo") {
            deshacer_ultima_insercion();
            return {};
        }

        throw invalid_argument("Tipo desconocido");
    }

private:

    // ============================
    // BST insertar
    // ============================
    NodoBST* bst_insertar(NodoBST* nodo, const Pelicula& p) {

        if (!nodo) {
            return new NodoBST(p.puntaje, p);
        }

        if (p.puntaje < nodo->clave) {
            nodo->izq = bst_insertar(nodo->izq, p);
        }
        else if (p.puntaje > nodo->clave) {
            nodo->der = bst_insertar(nodo->der, p);
        }
        else {
            nodo->peliculas.push_back(p);
        }

        return nodo;
    }

    // ============================
    // BST rango
    // ============================
    void bst_rango(NodoBST* nodo,
                   double minv,
                   double maxv,
                   vector<Pelicula>& out) {

        if (!nodo) return;

        if (minv < nodo->clave) {
            bst_rango(nodo->izq, minv, maxv, out);
        }

        if (minv <= nodo->clave && nodo->clave <= maxv) {
            out.insert(out.end(),
                       nodo->peliculas.begin(),
                       nodo->peliculas.end());
        }

        if (nodo->clave < maxv) {
            bst_rango(nodo->der, minv, maxv, out);
        }
    }

    // ============================
    // Liberar BST
    // ============================
    void liberarBST(NodoBST* nodo) {

        if (!nodo) return;

        liberarBST(nodo->izq);
        liberarBST(nodo->der);

        delete nodo;
    }

    // ============================
    // Undo
    // ============================
    void deshacer_ultima_insercion() {

        if (pilaUndo.empty()) {
            throw runtime_error("Nada que deshacer");
        }

        string id = pilaUndo.back().idInsertado;
        pilaUndo.pop_back();

        auto it = catalogo.find(id);

        if (it == catalogo.end()) {
            throw runtime_error("Inconsistencia");
        }

        Pelicula p = it->second;

        catalogo.erase(it);

        bst_raiz = bst_borrar(bst_raiz, p.puntaje, id);
    }

    // ============================
    // BST borrar
    // ============================
    NodoBST* bst_borrar(NodoBST* nodo,
                        double clave,
                        const string& id) {

        if (!nodo) return nullptr;

        if (clave < nodo->clave) {
            nodo->izq = bst_borrar(nodo->izq, clave, id);
            return nodo;
        }

        if (clave > nodo->clave) {
            nodo->der = bst_borrar(nodo->der, clave, id);
            return nodo;
        }

        auto& v = nodo->peliculas;

        v.erase(remove_if(v.begin(), v.end(),
                          [&](const Pelicula& p) {
            return p.id == id;
        }), v.end());

        if (!v.empty()) {
            return nodo;
        }

        // Caso hoja
        if (!nodo->izq && !nodo->der) {
            delete nodo;
            return nullptr;
        }

        // Un hijo
        if (!nodo->izq) {
            NodoBST* tmp = nodo->der;
            delete nodo;
            return tmp;
        }

        if (!nodo->der) {
            NodoBST* tmp = nodo->izq;
            delete nodo;
            return tmp;
        }

        // Dos hijos
        NodoBST* succParent = nodo;
        NodoBST* succ = nodo->der;

        while (succ->izq) {
            succParent = succ;
            succ = succ->izq;
        }

        nodo->clave = succ->clave;
        nodo->peliculas = succ->peliculas;

        if (succParent->izq == succ) {
            succParent->izq =
                bst_borrar(succ, succ->clave, "");
        }
        else {
            succParent->der =
                bst_borrar(succ, succ->clave, "");
        }

        return nodo;
    }
};

// =====================================================
// Benchmark
// =====================================================

struct BenchResult {
    double median_us;
    double p95_us;
    double min_us;
};

BenchResult medir_p95(function<void()> fn,
                      int warmup = 30,
                      int reps = 300) {

    for (int i = 0; i < warmup; i++) {
        fn();
    }

    vector<double> muestras;
    muestras.reserve(reps);

    for (int i = 0; i < reps; i++) {

        auto t0 = steady_clock::now();

        fn();

        auto dt =
            duration_cast<nanoseconds>(
                steady_clock::now() - t0
            ).count() / 1000.0;

        muestras.push_back(dt);
    }

    sort(muestras.begin(), muestras.end());

    double median;

    if (reps % 2 == 0) {
        median =
            (muestras[reps/2 - 1] + muestras[reps/2]) / 2.0;
    }
    else {
        median = muestras[reps/2];
    }

    int p95_idx = (int)(0.95 * reps);

    if (p95_idx >= reps) {
        p95_idx = reps - 1;
    }

    return {
        median,
        muestras[p95_idx],
        muestras[0]
    };
}

struct BenchmarkRow {
    string op;
    int n;
    BenchResult r;
};

static string fmt_us(double us) {

    ostringstream oss;

    oss << fixed << setprecision(4) << us;

    return oss.str();
}

// =====================================================
// Benchmark del sistema
// =====================================================

vector<BenchmarkRow> benchmark_sistema(int n,
                                       SistemaMX& sistema) {

    mt19937 rng(12345);

    uniform_real_distribution<double>
        distPts(1.0, 10.0);

    vector<string> ids;
    ids.reserve(n);

    // Poblar
    for (int i = 0; i < n; i++) {

        string id = "C" + to_string(i);

        double pts = distPts(rng);

        sistema.agregar_contenido(
            id,
            "Titulo_" + to_string(i),
            pts
        );

        ids.push_back(id);
    }

    uniform_int_distribution<int>
        distIdx(0, n - 1);

    string id_muestra = ids[distIdx(rng)];

    // Activar snapshot para top10
    (void) sistema.procesar_solicitud(
        "rango",
        "",
        7.0,
        9.0
    );

    vector<BenchmarkRow> rows;

    // LOOKUP
    rows.push_back({
        "lookup",
        n,
        medir_p95([&]() {
            (void) sistema.procesar_solicitud(
                "lookup",
                id_muestra
            );
        })
    });

    // RANGO
    rows.push_back({
        "rango",
        n,
        medir_p95([&]() {
            (void) sistema.procesar_solicitud(
                "rango",
                "",
                7.0,
                9.0
            );
        })
    });

    // TOP10
    rows.push_back({
        "top10",
        n,
        medir_p95([&]() {
            (void) sistema.procesar_solicitud(
                "top10"
            );
        })
    });

    return rows;
}

// =====================================================
// Imprimir tabla
// =====================================================

static void imprimir_tabla(
    const vector<BenchmarkRow>& rows) {

    cout << left << setw(12) << "Operacion"
         << right << setw(10) << "n"
         << right << setw(16) << "Mediana(us)"
         << right << setw(14) << "P95(us)"
         << right << setw(14) << "Min(us)"
         << "\n";

    cout << string(66, '-') << "\n";

    for (const auto& row : rows) {

        cout << left << setw(12) << row.op
             << right << setw(10) << row.n
             << right << setw(16)
             << fmt_us(row.r.median_us)
             << right << setw(14)
             << fmt_us(row.r.p95_us)
             << right << setw(14)
             << fmt_us(row.r.min_us)
             << "\n";
    }
}

// =====================================================
// MAIN UNIFICADO
// =====================================================

int main() {

    cout << "====================================\n";
    cout << " DEMO BASICA SISTEMAMX\n";
    cout << "====================================\n";

    SistemaMX s;

    // Inicialización
    cout << "catalogo size: "
         << s.catalogo.size() << "\n";

    cout << "bst vacio: "
         << (s.bst_raiz == nullptr) << "\n";

    cout << "pilaResultados vacia: "
         << s.pilaResultados.size() << "\n";

    cout << "pilaUndo vacia: "
         << s.pilaUndo.size() << "\n";

    // Inserciones
    s.agregar_contenido("MX001", "El Laberinto", 8.5);
    s.agregar_contenido("MX002", "Noche Polar", 7.2);
    s.agregar_contenido("MX003", "Codigo Cero", 9.1);
    s.agregar_contenido("MX004", "Delta", 6.0);

    // Lookup
    auto r1 = s.procesar_solicitud(
        "lookup",
        "MX001"
    );

    cout << "\nlookup MX001 -> "
         << (r1.empty() ? "NO" : r1[0].titulo)
         << "\n";

    // Rango
    auto r2 = s.procesar_solicitud(
        "rango",
        "",
        7.0,
        9.0
    );

    cout << "rango [7,9] -> "
         << r2.size()
         << " resultados\n";

    // Top10
    auto top = s.procesar_solicitud("top10");

    cout << "top10 -> "
         << top.size()
         << "\n";

    // Undo
    s.procesar_solicitud("undo");

    auto r3 = s.procesar_solicitud(
        "lookup",
        "MX004"
    );

    cout << "despues de undo -> "
         << (r3.empty() ? "NO EXISTE" : "EXISTE")
         << "\n";

    cout << "\nDemo basica OK\n";

    // ====================================
    // BENCHMARKS
    // ====================================

    cout << "\n====================================\n";
    cout << " BENCHMARK n = 1,000\n";
    cout << "====================================\n";

    {
        SistemaMX s1;

        auto r1 = benchmark_sistema(1000, s1);

        imprimir_tabla(r1);
    }

    cout << "\n====================================\n";
    cout << " BENCHMARK n = 10,000\n";
    cout << "====================================\n";

    {
        SistemaMX s2;

        auto r2 = benchmark_sistema(10000, s2);

        imprimir_tabla(r2);
    }

    return 0;
}