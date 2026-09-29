# Pila (Stack)

Finora abbiamo visto **contenitori**: array e vector conservano dati e ti lasciano accedere a qualsiasi posizione. Una **struttura dati** come la pila aggiunge una regola: **non puoi** accedere dove vuoi, solo in un punto preciso.

Sembra una limitazione, ed è proprio questo il punto: la regola rende il programma più semplice da ragionare e più difficile da usare nel modo sbagliato.

## Il Concetto: LIFO

Pensa a una **pila di piatti**. Un piatto nuovo si appoggia **sopra**, e quando ne serve uno lo prendi **dall'alto**. Il piatto in fondo è il primo che hai messo ed è l'ultimo che prenderai.

Questa regola si chiama **LIFO**: *Last In, First Out*, "l'ultimo a entrare è il primo a uscire".

```
push(10)    push(20)    push(30)    pop()       pop()

                        | 30 |  <- cima
            | 20 |      | 20 |      | 20 |
| 10 |      | 10 |      | 10 |      | 10 |      | 10 |
+----+      +----+      +----+      +----+      +----+
```

## Le Operazioni

Una pila si usa **solo** attraverso queste operazioni:

| Operazione | Cosa fa                                     |
| ---------- | ------------------------------------------- |
| `push(x)`  | Mette `x` in cima                            |
| `pop()`    | Toglie l'elemento in cima                    |
| `top()`    | Legge l'elemento in cima, senza toglierlo    |
| `empty()`  | Dice se la pila è vuota                      |
| `size()`   | Dice quanti elementi contiene                |

Non esiste "leggi il terzo elemento dal basso". Se ti serve, la pila è la struttura sbagliata.

**Dove si usa davvero:**
- Il tasto **Annulla** (Ctrl+Z) di un editor: l'ultima modifica fatta è la prima annullata.
- Il tasto **Indietro** del browser.
- Il controllo delle **parentesi** in un'espressione (lo vediamo nell'esempio finale).
- Le **chiamate di funzione**: quando `main` chiama `f` che chiama `g`, il programma torna prima da `g`, poi da `f`, poi a `main`. Questa zona di memoria si chiama proprio *stack*.

## Costruire una Pila a Mano

Prima di usare la versione pronta della libreria, costruiamone una con quello che conosciamo: un **array** per i dati e un **intero** che ricorda quanti elementi ci sono.

```cpp
const int CAPACITA = 5;

int dati[CAPACITA];     // dove stanno gli elementi
int quanti = 0;         // quanti elementi ci sono (all'inizio nessuno)
```

L'idea chiave: gli elementi occupano le posizioni da `0` a `quanti - 1`, quindi la **cima** è sempre `dati[quanti - 1]`.

| Operazione | Cosa fa sull'array                              |
| ---------- | ----------------------------------------------- |
| `push(x)`  | `dati[quanti] = x;` poi `quanti++`               |
| `pop()`    | `quanti--` (l'elemento resta in memoria, ma non conta più) |
| `top()`    | restituisce `dati[quanti - 1]`                   |
| `empty()`  | `quanti == 0`                                    |
| piena?     | `quanti == CAPACITA`                             |

Ecco la sequenza `push(10)`, `push(20)`, `push(30)`, `pop()`:

| Dopo        | `dati[0]` | `dati[1]` | `dati[2]` | `quanti` | Cima |
| ----------- | --------- | --------- | --------- | -------- | ---- |
| inizio      | ?         | ?         | ?         | 0        | -    |
| `push(10)`  | 10        | ?         | ?         | 1        | 10   |
| `push(20)`  | 10        | 20        | ?         | 2        | 20   |
| `push(30)`  | 10        | 20        | 30        | 3        | 30   |
| `pop()`     | 10        | 20        | 30        | 2        | 20   |

Dopo il `pop()` il `30` è ancora fisicamente nell'array, ma `quanti` vale `2`, quindi per la pila non esiste più. Il prossimo `push` lo sovrascriverà.

### Il Codice

Ogni operazione diventa una funzione. L'array e il contatore vengono passati a ogni funzione; `quanti` passa **per riferimento** quando la funzione deve modificarlo.

```cpp
#include <iostream>
using namespace std;

const int CAPACITA = 5;

bool pilaVuota(int quanti) {
    return quanti == 0;
}

bool pilaPiena(int quanti) {
    return quanti == CAPACITA;
}

void push(int dati[], int& quanti, int valore) {
    if (pilaPiena(quanti)) {
        cout << "Errore: pila piena" << endl;
        return;
    }
    dati[quanti] = valore;
    quanti++;
}

void pop(int& quanti) {
    if (pilaVuota(quanti)) {
        cout << "Errore: pila vuota" << endl;
        return;
    }
    quanti--;
}

int top(const int dati[], int quanti) {
    return dati[quanti - 1];    // chi chiama deve controllare prima che non sia vuota
}

int main() {
    int dati[CAPACITA];
    int quanti = 0;

    push(dati, quanti, 10);
    push(dati, quanti, 20);
    push(dati, quanti, 30);

    cout << "Cima: " << top(dati, quanti) << endl;          // 30

    pop(quanti);
    cout << "Cima: " << top(dati, quanti) << endl;          // 20

    // Svuota la pila stampando gli elementi
    cout << "Svuoto: ";
    while (!pilaVuota(quanti)) {
        cout << top(dati, quanti) << " ";
        pop(quanti);
    }
    cout << endl;

    pop(quanti);    // pila già vuota: errore gestito

    return 0;
}
```

**Output:**
```
Cima: 30
Cima: 20
Svuoto: 20 10
Errore: pila vuota
```

Nota l'ordine della riga `Svuoto`: gli elementi escono al contrario di come sono entrati. È il LIFO in azione.

### I Due Errori da Gestire

| Errore        | Quando                          | Nome tecnico  |
| ------------- | ------------------------------- | ------------- |
| Pila piena    | `push` con `quanti == CAPACITA` | *overflow*    |
| Pila vuota    | `pop` o `top` con `quanti == 0` | *underflow*   |

> [!WARNING]
> Senza il controllo in `push`, una pila piena scriverebbe `dati[5]` in un array da 5: esattamente l'uscita dai limiti vista in [11-array.md](11-array.md). Senza il controllo in `pop`, `quanti` diventerebbe negativo e il `top` successivo leggerebbe `dati[-2]`.

### Versione con `vector`

Con un vector la pila **non si riempie mai** e il contatore non serve: il vector sa già quanti elementi ha. Le operazioni corrispondono una a una a metodi che conosci:

| Pila     | Vector          |
| -------- | --------------- |
| `push(x)` | `v.push_back(x)` |
| `pop()`  | `v.pop_back()`  |
| `top()`  | `v.back()`      |
| `empty()` | `v.empty()`    |
| `size()` | `v.size()`      |

Un vector usato solo con questi metodi **è** una pila. Il problema è che nessuno ti impedisce di scrivere `v[0]` e rompere la regola. La versione della libreria risolve proprio questo.

## `std::stack`: la Pila della Libreria

La libreria standard offre una pila pronta, che espone **solo** le operazioni della pila.

```cpp
#include <stack>

stack<int> pila;
```

| Metodo         | Cosa fa                                   |
| -------------- | ----------------------------------------- |
| `pila.push(x)` | Mette `x` in cima                          |
| `pila.pop()`   | Toglie l'elemento in cima                  |
| `pila.top()`   | Restituisce l'elemento in cima             |
| `pila.empty()` | `true` se è vuota                          |
| `pila.size()`  | Numero di elementi                         |

```cpp
#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> pila;

    pila.push(10);
    pila.push(20);
    pila.push(30);

    cout << "Elementi: " << pila.size() << endl;    // 3
    cout << "Cima: " << pila.top() << endl;         // 30

    pila.pop();
    cout << "Cima: " << pila.top() << endl;         // 20

    // Svuota la pila stampando gli elementi
    cout << "Svuoto: ";
    while (!pila.empty()) {
        cout << pila.top() << " ";
        pila.pop();
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
Elementi: 3
Cima: 30
Cima: 20
Svuoto: 20 10
```

Il programma è lo stesso di quello scritto a mano, ma senza array, contatore e controlli di capienza: `std::stack` cresce da solo.

> [!WARNING]
> Due trappole di `std::stack`:
> - `pop()` **non restituisce** l'elemento tolto. Per leggerlo e toglierlo servono due righe: prima `top()`, poi `pop()`.
> - `top()` e `pop()` su una pila vuota **non** segnalano nessun errore: il comportamento è imprevedibile. Il controllo con `empty()` resta compito tuo.

> Nota: `std::stack` non si può scorrere con un `for` e non ha `[]`. È voluto: una pila mostra solo la cima. Per vedere tutti gli elementi bisogna toglierli uno a uno, come nel ciclo `while` qui sopra.

## Esempio Completo: Parentesi Bilanciate

Un classico: data un'espressione, controllare che ogni parentesi aperta venga chiusa **dal tipo giusto** e **nell'ordine giusto**.

| Espressione      | Bilanciata? | Perché                               |
| ---------------- | ----------- | ------------------------------------ |
| `(a + b) * c`    | Sì          |                                      |
| `{[a + (b)] * c}` | Sì         |                                      |
| `(a + b]`        | No          | `(` chiusa da `]`                     |
| `(a + b`         | No          | `(` mai chiusa                        |
| `a + b)`         | No          | `)` senza nessuna aperta              |

**L'idea:** si legge l'espressione un carattere alla volta.
- Parentesi **aperta** → va nella pila.
- Parentesi **chiusa** → deve corrispondere alla cima della pila, che viene tolta. Se la pila è vuota o la cima non corrisponde, l'espressione è sbagliata.
- Alla fine la pila deve essere **vuota**: altrimenti qualche parentesi non è mai stata chiusa.

La pila funziona perché l'ultima parentesi aperta è la prima che deve essere chiusa: è LIFO.

```cpp
#include <iostream>
#include <stack>
#include <string>
using namespace std;

// Restituisce la parentesi aperta che corrisponde a una chiusa
char apertaCorrispondente(char chiusa) {
    if (chiusa == ')') return '(';
    if (chiusa == ']') return '[';
    return '{';
}

bool bilanciata(const string& espressione) {
    stack<char> aperte;

    for (char c : espressione) {
        if (c == '(' || c == '[' || c == '{') {
            aperte.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (aperte.empty()) {
                return false;       // chiusa senza nessuna aperta
            }
            if (aperte.top() != apertaCorrispondente(c)) {
                return false;       // tipo sbagliato
            }
            aperte.pop();
        }
        // tutti gli altri caratteri vengono ignorati
    }

    return aperte.empty();          // qualcosa è rimasto aperto?
}

int main() {
    string espressione;

    cout << "Espressione: ";
    getline(cin, espressione);

    if (bilanciata(espressione)) {
        cout << "Parentesi bilanciate" << endl;
    } else {
        cout << "Parentesi NON bilanciate" << endl;
    }

    return 0;
}
```

**Esecuzione:**
```
Espressione: {[a + (b)] * c}
Parentesi bilanciate
```

```
Espressione: (a + b]
Parentesi NON bilanciate
```

Ecco cosa succede alla pila con `{[a + (b)] * c}`, considerando solo le parentesi:

| Carattere | Azione                    | Pila dopo (cima a destra) |
| --------- | ------------------------- | ------------------------- |
| `{`       | push                      | `{`                       |
| `[`       | push                      | `{ [`                     |
| `(`       | push                      | `{ [ (`                   |
| `)`       | cima `(` corrisponde, pop | `{ [`                     |
| `]`       | cima `[` corrisponde, pop | `{`                       |
| `}`       | cima `{` corrisponde, pop | *vuota*                   |

Pila vuota alla fine: l'espressione è bilanciata.

---

⬅️ [Precedente: Vector](15-vector.md) | [📚 Indice](.github/README.md) | [Successivo: Coda (Queue)](16-coda.md) ➡️
