# Coda (Queue)

La **coda** è la sorella della [pila](16-pila.md): anche lei permette di accedere solo a certi elementi, ma con la regola opposta.

## Il Concetto: FIFO

Pensa alla **fila alla posta**. Chi arriva si mette **in fondo**, e lo sportello serve chi è **davanti**. Il primo arrivato è il primo servito.

Questa regola si chiama **FIFO**: *First In, First Out*, "il primo a entrare è il primo a uscire".

```
                    fronte               fondo
                      |                    |
  esce  <---        [ 10 ]  [ 20 ]  [ 30 ]        <---  entra
```

| Struttura | Regola | Si inserisce | Si toglie   |
| --------- | ------ | ------------ | ----------- |
| Pila      | LIFO   | in cima      | dalla cima  |
| Coda      | FIFO   | in fondo     | dal fronte  |

## Le Operazioni

| Operazione | Cosa fa                                        |
| ---------- | ---------------------------------------------- |
| `push(x)`  | Mette `x` in **fondo** alla coda (*enqueue*)    |
| `pop()`    | Toglie l'elemento al **fronte** (*dequeue*)     |
| `front()`  | Legge l'elemento al fronte, senza toglierlo     |
| `empty()`  | Dice se la coda è vuota                         |
| `size()`   | Dice quanti elementi contiene                   |

**Dove si usa davvero:**
- La **coda di stampa**: i documenti vengono stampati nell'ordine in cui sono stati inviati.
- I **messaggi** e le richieste a un server, gestiti in ordine di arrivo.
- La tastiera: i tasti premuti vengono letti nell'ordine in cui li hai premuti.
- Qualsiasi simulazione di **turni**: sportelli, casse, processi del sistema operativo.

## Costruire una Coda a Mano

Come per la pila, partiamo da un array. Serve però un'idea in più.

### Il Problema dell'Array Semplice

L'approccio più ovvio: inserire in fondo come nella pila, e togliere da `dati[0]` spostando indietro tutti gli altri di un posto.

| Operazione | Array dopo       |
| ---------- | ---------------- |
| push 10, 20, 30 | `10 20 30`  |
| pop        | `20 30` (spostati tutti) |

Funziona, ma ogni `pop` deve spostare **tutti** gli elementi rimasti: con una coda di un milione di elementi, un milione di spostamenti per toglierne uno.

L'alternativa è **non spostare niente** e ricordare con un indice `fronte` dove inizia la coda. Ma così lo spazio all'inizio dell'array, liberato dai `pop`, non viene più riusato: dopo abbastanza operazioni si arriva alla fine dell'array anche con la coda quasi vuota.

### La Soluzione: l'Array Circolare

L'idea è trattare l'array come se fosse un **anello**: quando si arriva alla fine, si ricomincia dall'inizio, riusando i posti liberati.

```
    [0]  [1]  [2]  [3]  [4]
     ^                   |
     +-------------------+
   dopo l'ultima posizione si torna alla prima
```

Servono tre informazioni:

```cpp
const int CAPACITA = 5;

int dati[CAPACITA];
int fronte = 0;     // indice del primo elemento
int quanti = 0;     // quanti elementi ci sono
```

Il **fondo**, cioè il posto dove va il prossimo elemento, si calcola: è `quanti` posizioni dopo `fronte`. Per "tornare all'inizio" dopo l'ultima posizione si usa il modulo `%`, visto in [5-operatori-aritmetici.md](5-operatori-aritmetici.md):

```cpp
int fondo = (fronte + quanti) % CAPACITA;
```

Il resto della divisione per `CAPACITA` è sempre un numero tra `0` e `CAPACITA - 1`: con `CAPACITA` uguale a 5, dopo l'indice `4` viene `5 % 5 = 0`.

| Operazione | Cosa fa                                                     |
| ---------- | ----------------------------------------------------------- |
| `push(x)`  | `dati[(fronte + quanti) % CAPACITA] = x;` poi `quanti++`     |
| `pop()`    | `fronte = (fronte + 1) % CAPACITA;` poi `quanti--`           |
| `front()`  | restituisce `dati[fronte]`                                   |
| `empty()`  | `quanti == 0`                                                |
| piena?     | `quanti == CAPACITA`                                         |

Ecco una sequenza con `CAPACITA` uguale a 5. Tra parentesi quadre gli elementi che fanno parte della coda, `.` indica un posto che non fa parte della coda (il vecchio valore può esserci ancora, come nella pila, ma non conta più).

| Operazione | `[0]` | `[1]` | `[2]` | `[3]` | `[4]` | `fronte` | `quanti` |
| ---------- | ----- | ----- | ----- | ----- | ----- | -------- | -------- |
| inizio     | .     | .     | .     | .     | .     | 0        | 0        |
| push 10, 20, 30, 40 | [10] | [20] | [30] | [40] | . | 0  | 4        |
| pop        | .     | [20]  | [30]  | [40]  | .     | 1        | 3        |
| pop        | .     | .     | [30]  | [40]  | .     | 2        | 2        |
| push 50    | .     | .     | [30]  | [40]  | [50]  | 2        | 3        |
| push 60    | [60]  | .     | [30]  | [40]  | [50]  | 2        | 4        |

All'ultimo `push` il fondo vale `(2 + 3) % 5 = 0`: il `60` finisce in `dati[0]`, riusando il posto liberato dal primo `pop`. L'ordine della coda resta `30 40 50 60`, anche se in memoria il `60` sta prima del `30`.

### Il Codice

```cpp
#include <iostream>
using namespace std;

const int CAPACITA = 5;

bool codaVuota(int quanti) {
    return quanti == 0;
}

bool codaPiena(int quanti) {
    return quanti == CAPACITA;
}

void push(int dati[], int fronte, int& quanti, int valore) {
    if (codaPiena(quanti)) {
        cout << "Errore: coda piena" << endl;
        return;
    }
    int fondo = (fronte + quanti) % CAPACITA;
    dati[fondo] = valore;
    quanti++;
}

void pop(int& fronte, int& quanti) {
    if (codaVuota(quanti)) {
        cout << "Errore: coda vuota" << endl;
        return;
    }
    fronte = (fronte + 1) % CAPACITA;
    quanti--;
}

int front(const int dati[], int fronte) {
    return dati[fronte];    // chi chiama deve controllare prima che non sia vuota
}

int main() {
    int dati[CAPACITA];
    int fronte = 0;
    int quanti = 0;

    push(dati, fronte, quanti, 10);
    push(dati, fronte, quanti, 20);
    push(dati, fronte, quanti, 30);
    push(dati, fronte, quanti, 40);

    pop(fronte, quanti);        // esce 10
    pop(fronte, quanti);        // esce 20

    push(dati, fronte, quanti, 50);
    push(dati, fronte, quanti, 60);     // finisce in dati[0]

    cout << "Fronte: " << front(dati, fronte) << endl;     // 30

    // Svuota la coda stampando gli elementi
    cout << "Svuoto: ";
    while (!codaVuota(quanti)) {
        cout << front(dati, fronte) << " ";
        pop(fronte, quanti);
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
Fronte: 30
Svuoto: 30 40 50 60
```

Gli elementi escono **nello stesso ordine** in cui sono entrati: è il FIFO. Confrontalo con la pila, dove uscivano al contrario.

Nota quali parametri passano per riferimento: `push` modifica solo `quanti`, mentre `pop` modifica sia `fronte` che `quanti`.

> [!WARNING]
> Come per la pila, i controlli su coda piena (*overflow*) e coda vuota (*underflow*) sono indispensabili. Senza di essi, con la coda piena il `push` sovrascriverebbe elementi ancora in attesa; con la coda vuota il `pop` porterebbe `quanti` sotto zero.

## `std::queue`: la Coda della Libreria

```cpp
#include <queue>

queue<int> coda;
```

| Metodo         | Cosa fa                                   |
| -------------- | ----------------------------------------- |
| `coda.push(x)` | Mette `x` in fondo                         |
| `coda.pop()`   | Toglie l'elemento al fronte                |
| `coda.front()` | Restituisce l'elemento al fronte           |
| `coda.back()`  | Restituisce l'elemento in fondo            |
| `coda.empty()` | `true` se è vuota                          |
| `coda.size()`  | Numero di elementi                         |

```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> coda;

    coda.push(10);
    coda.push(20);
    coda.push(30);

    cout << "Elementi: " << coda.size() << endl;    // 3
    cout << "Fronte: " << coda.front() << endl;     // 10
    cout << "Fondo: " << coda.back() << endl;       // 30

    coda.pop();
    cout << "Fronte: " << coda.front() << endl;     // 20

    // Svuota la coda stampando gli elementi
    cout << "Svuoto: ";
    while (!coda.empty()) {
        cout << coda.front() << " ";
        coda.pop();
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
Elementi: 3
Fronte: 10
Fondo: 30
Fronte: 20
Svuoto: 20 30
```

`std::queue` non ha capienza massima, quindi niente array circolare da gestire: cresce da sola.

> [!WARNING]
> Le stesse trappole di `std::stack`:
> - `pop()` **non restituisce** l'elemento: prima `front()`, poi `pop()`.
> - `front()`, `back()` e `pop()` su una coda vuota hanno comportamento imprevedibile. Controlla con `empty()`.

> Nota: attenzione ai nomi. Nella pila l'elemento accessibile si legge con `top()`, nella coda con `front()`. Scrivere `coda.top()` è un errore di compilazione.

## Pila o Coda?

| Domanda                                        | Struttura |
| ---------------------------------------------- | --------- |
| Devo annullare le ultime azioni, in ordine inverso? | Pila  |
| Devo tornare indietro sui miei passi?          | Pila      |
| Devo servire le richieste in ordine di arrivo? | Coda      |
| Devo elaborare dati nell'ordine in cui arrivano? | Coda    |

| Pila `std::stack` | Coda `std::queue` |
| ----------------- | ----------------- |
| `#include <stack>` | `#include <queue>` |
| `push(x)`: in cima | `push(x)`: in fondo |
| `pop()`: dalla cima | `pop()`: dal fronte |
| `top()`           | `front()` e `back()` |

## Esempio Completo: Sportello con Turni

Una simulazione di uno sportello. I clienti prendono il numero e si mettono in coda; l'impiegato li chiama in ordine di arrivo.

```cpp
#include <iostream>
#include <queue>
#include <string>
using namespace std;

void mostraMenu() {
    cout << endl;
    cout << "1. Nuovo cliente" << endl;
    cout << "2. Chiama il prossimo" << endl;
    cout << "3. Clienti in attesa" << endl;
    cout << "0. Esci" << endl;
    cout << "Scelta: ";
}

int main() {
    queue<string> attesa;
    int scelta;

    do {
        mostraMenu();
        cin >> scelta;

        switch (scelta) {
            case 1: {
                string nome;
                cout << "Nome del cliente: ";
                cin >> nome;
                attesa.push(nome);
                cout << nome << " aggiunto alla coda. Persone davanti: "
                     << attesa.size() - 1 << endl;
                break;
            }
            case 2:
                if (attesa.empty()) {
                    cout << "Nessun cliente in attesa" << endl;
                } else {
                    cout << "Allo sportello: " << attesa.front() << endl;
                    attesa.pop();
                }
                break;
            case 3:
                cout << "In attesa: " << attesa.size() << endl;
                break;
            case 0:
                cout << "Chiusura sportello" << endl;
                break;
            default:
                cout << "Scelta non valida" << endl;
        }
    } while (scelta != 0);

    return 0;
}
```

**Esecuzione:**
```

1. Nuovo cliente
2. Chiama il prossimo
3. Clienti in attesa
0. Esci
Scelta: 1
Nome del cliente: Anna
Anna aggiunto alla coda. Persone davanti: 0

...
Scelta: 1
Nome del cliente: Luca
Luca aggiunto alla coda. Persone davanti: 1

...
Scelta: 2
Allo sportello: Anna

...
Scelta: 2
Allo sportello: Luca

...
Scelta: 2
Nessun cliente in attesa
```

Per brevità, nell'esecuzione il menu è mostrato solo la prima volta e sostituito da `...` nelle successive.

> Nota: le graffe dopo `case 1:` servono perché dentro quel `case` viene dichiarata una variabile (`nome`). Senza graffe il compilatore segnala un errore, perché la variabile sarebbe visibile anche negli altri `case`, dove non è stata inizializzata.

---

⬅️ [Precedente: Pila (Stack)](16-pila.md) | [📚 Indice](.github/README.md)
