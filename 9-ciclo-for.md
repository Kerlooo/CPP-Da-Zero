# Ciclo `for` in C++

Il `for` fa esattamente le stesse cose di un `while`, ma raccoglie i **tre ingredienti del ciclo** (inizializzazione, condizione, aggiornamento) su una sola riga. È il ciclo da usare quando sai **quante volte** vuoi ripetere.

## Sintassi

```cpp
for (inizializzazione; condizione; aggiornamento) {
    // Codice ripetuto
}
```

**Le tre parti, separate da punto e virgola:**
- `inizializzazione` → eseguita **una volta sola**, all'inizio
- `condizione` → controllata **prima** di ogni iterazione; se è `false` il ciclo finisce
- `aggiornamento` → eseguito **alla fine** di ogni iterazione

## Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 5; i++) {
        cout << i << endl;
    }

    return 0;
}
```

**Output:**
```
1
2
3
4
5
```

## Lo Stesso Ciclo, Scritto nei Due Modi

```cpp
// Con while: le tre parti sono sparse in tre punti diversi
int i = 1;
while (i <= 5) {
    cout << i << endl;
    i++;
}

// Con for: le tre parti sono tutte sulla stessa riga
for (int i = 1; i <= 5; i++) {
    cout << i << endl;
}
```

Il risultato è identico. Il `for` è preferibile perché è impossibile dimenticare l'aggiornamento: è lì in vista, dentro le parentesi.

## Ordine di Esecuzione

Il `for` non esegue le tre parti da sinistra a destra a ogni giro. L'ordine reale è:

1. `inizializzazione` → **solo la prima volta**
2. `condizione` → se `false`, il ciclo finisce subito
3. **corpo** del ciclo
4. `aggiornamento`
5. torna al punto 2

| Iterazione | `i` all'inizio | `i <= 3` | Stampa | Dopo `i++` |
| ---------- | -------------- | -------- | ------ | ---------- |
| 1          | 1              | `true`   | `1`    | 2          |
| 2          | 2              | `true`   | `2`    | 3          |
| 3          | 3              | `true`   | `3`    | 4          |
| 4          | 4              | `false`  | —      | il ciclo finisce |

> Nota: l'`aggiornamento` avviene **dopo** il corpo, non prima. Per questo la prima iterazione usa il valore iniziale intatto.

## Contare all'Indietro

Basta invertire condizione e aggiornamento:

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 5; i >= 1; i--) {
        cout << i << endl;
    }

    cout << "Partiti!" << endl;

    return 0;
}
```

**Output:**
```
5
4
3
2
1
Partiti!
```

## Cambiare il Passo

L'aggiornamento non deve per forza essere `i++`. Può essere qualsiasi operazione.

```cpp
#include <iostream>
using namespace std;

int main() {
    // Solo i numeri pari da 0 a 10
    for (int i = 0; i <= 10; i += 2) {
        cout << i << " ";
    }
    cout << endl;

    // Potenze di 2 fino a 64
    for (int i = 1; i <= 64; i *= 2) {
        cout << i << " ";
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
0 2 4 6 8 10
1 2 4 8 16 32 64
```

## Partire da Zero

Nei cicli `for` la convenzione è partire da `0` e usare `<` invece di `<=`. Serve a ripetere esattamente `n` volte:

```cpp
// 5 iterazioni: i vale 0, 1, 2, 3, 4
for (int i = 0; i < 5; i++) {
    cout << "Iterazione numero " << i << endl;
}
```

| Scrittura                  | Valori di `i`       | Numero di giri |
| -------------------------- | ------------------- | -------------- |
| `for (int i = 0; i < 5; i++)`  | 0, 1, 2, 3, 4   | 5              |
| `for (int i = 1; i <= 5; i++)` | 1, 2, 3, 4, 5   | 5              |
| `for (int i = 0; i <= 5; i++)` | 0, 1, 2, 3, 4, 5| 6 (attenzione!) |

> Nota: questa convenzione diventerà obbligatoria con gli **array**, dove le posizioni si contano sempre a partire da `0`.

## Lo Scope della Variabile

Una variabile dichiarata **dentro** le parentesi del `for` esiste solo dentro il ciclo. Fuori, il compilatore dà errore.

```cpp
for (int i = 0; i < 5; i++) {
    cout << i << endl;      // OK
}

cout << i << endl;          //  errore: 'i' non esiste più qui
```

Se ti serve il valore anche dopo, dichiara la variabile prima del ciclo:

```cpp
int i;

for (i = 0; i < 5; i++) {   // nota: manca 'int', la variabile esiste già
    cout << i << endl;
}

cout << "Alla fine i vale: " << i << endl;      // 5
```

## Cicli Annidati

Un ciclo può contenerne un altro. Il ciclo **interno** completa tutti i suoi giri per **ogni singolo giro** di quello esterno.

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 3; i++) {          // ciclo esterno: 3 giri
        for (int j = 1; j <= 2; j++) {      // ciclo interno: 2 giri ciascuno
            cout << "i=" << i << " j=" << j << endl;
        }
    }

    return 0;
}
```

**Output:**
```
i=1 j=1
i=1 j=2
i=2 j=1
i=2 j=2
i=3 j=1
i=3 j=2
```

Totale: 3 × 2 = **6 iterazioni**.

> Nota: usa nomi diversi per i contatori (`i`, `j`, `k`). Riusare `i` in entrambi i cicli rompe il conteggio di quello esterno.

### Esempio: Tutte le Tabelline

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int tabellina = 1; tabellina <= 3; tabellina++) {
        cout << "--- Tabellina del " << tabellina << " ---" << endl;

        for (int moltiplicatore = 1; moltiplicatore <= 10; moltiplicatore++) {
            cout << tabellina << " x " << moltiplicatore
                 << " = " << tabellina * moltiplicatore << endl;
        }

        cout << endl;
    }

    return 0;
}
```

### Esempio: Triangolo di Asterischi

```cpp
#include <iostream>
using namespace std;

int main() {
    int altezza = 5;

    for (int riga = 1; riga <= altezza; riga++) {
        // Il ciclo interno dipende da 'riga': stampa tanti asterischi quanto vale
        for (int stella = 1; stella <= riga; stella++) {
            cout << "*";
        }
        cout << endl;       // a capo a fine riga
    }

    return 0;
}
```

**Output:**
```
*
**
***
****
*****
```

## Errori Frequenti

### Il Punto e Virgola di Troppo

```cpp
for (int i = 0; i < 5; i++);    //  il ; chiude il for: il corpo è vuoto
{
    cout << "Ciao" << endl;     // eseguito UNA volta sola, fuori dal ciclo
}
```

**Output:** `Ciao` (una volta invece di cinque). Il compilatore non segnala niente.

### L'Errore "Off by One"

Sbagliare di uno il conteggio è l'errore più comune con i cicli:

```cpp
for (int i = 1; i < 5; i++)     // 4 giri: 1, 2, 3, 4  (il 5 manca!)
for (int i = 1; i <= 5; i++)    // 5 giri: 1, 2, 3, 4, 5
```

> Nota: nel dubbio, prova a scrivere a mano la tabella delle iterazioni come quella più in alto. Fa capire subito quanti giri fa davvero il ciclo.

## Quale Ciclo Scegliere

| Situazione                                        | Ciclo consigliato |
| ------------------------------------------------- | ----------------- |
| Sai quante ripetizioni servono (10 volte, 1..100) | `for`             |
| Ripeti finché una condizione resta vera, senza sapere per quanto | `while` |
| Il corpo deve essere eseguito almeno una volta (validazione input) | `do-while` |
| Scorrere tutti gli elementi di un array           | `for`             |

## Esempio Completo: Somma e Media

```cpp
#include <iostream>
using namespace std;

int main() {
    int quantita;
    int somma = 0;      // accumulatore: sempre inizializzato prima del ciclo

    cout << "Quanti numeri vuoi inserire? ";
    cin >> quantita;

    for (int i = 1; i <= quantita; i++) {
        int numero;
        cout << "Numero " << i << ": ";
        cin >> numero;
        somma += numero;
    }

    // Cast a double: senza, la media tra interi perderebbe i decimali
    double media = (double)somma / quantita;

    cout << "Somma: " << somma << endl;
    cout << "Media: " << media << endl;

    return 0;
}
```

**Esecuzione:**
```
Quanti numeri vuoi inserire? 3
Numero 1: 10
Numero 2: 7
Numero 3: 4
Somma: 21
Media: 7
```

---

⬅️ [Precedente: Ciclo while](8-ciclo-while.md) | [📚 Indice](.github/README.md) | [Successivo: Break e Continue](9-break-continue.md) ➡️
