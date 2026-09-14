# Ciclo `while` e `do-while` in C++

Un **ciclo** (o *loop*) è un'istruzione che ripete un blocco di codice finché una condizione resta vera. Serve a evitare di riscrivere cento volte la stessa riga.

Senza ciclo:

```cpp
cout << 1 << endl;
cout << 2 << endl;
cout << 3 << endl;
// ...e così via fino a 100
```

Con un ciclo, le stesse 100 righe diventano 3.

## Ciclo `while`

Il `while` ripete un blocco **finché la condizione è vera**. La condizione viene controllata **prima** di ogni ripetizione.

### Sintassi

```cpp
while (condizione) {
    // Codice ripetuto finché condizione è true
}
```

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int i = 1;              // 1. Inizializzazione

    while (i <= 5) {        // 2. Condizione
        cout << i << endl;
        i++;                // 3. Aggiornamento
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

### Come Funziona

Ogni ripetizione del ciclo si chiama **iterazione**. Il programma esegue sempre questi passi:

1. Controlla la condizione.
2. Se è `true` → esegue il blocco, poi **torna al punto 1**.
3. Se è `false` → salta il blocco e prosegue con il codice sotto.

| Iterazione | `i` all'inizio | `i <= 5` | Stampa | `i` alla fine |
| ---------- | -------------- | -------- | ------ | ------------- |
| 1          | 1              | `true`   | `1`    | 2             |
| 2          | 2              | `true`   | `2`    | 3             |
| 3          | 3              | `true`   | `3`    | 4             |
| 4          | 4              | `true`   | `4`    | 5             |
| 5          | 5              | `true`   | `5`    | 6             |
| 6          | 6              | `false`  | —      | il ciclo finisce |

> Nota: se la condizione è **già falsa** alla prima verifica, il blocco non viene eseguito nemmeno una volta.

### I Tre Ingredienti di un Ciclo

Perché un ciclo funzioni e finisca, servono sempre tre cose:

| Ingrediente      | Nell'esempio | A cosa serve                        |
| ---------------- | ------------ | ----------------------------------- |
| Inizializzazione | `int i = 1;` | Dare un valore di partenza          |
| Condizione       | `i <= 5`     | Decidere quando fermarsi            |
| Aggiornamento    | `i++;`       | Avvicinarsi alla fine a ogni giro   |

Se ne manca uno, il ciclo non si ferma più.

### Il Ciclo Infinito

```cpp
int i = 1;

while (i <= 5) {
    cout << i << endl;
    // manca i++ : i resta 1 per sempre, la condizione è sempre true
}
```

> [!WARNING]
> Questo codice stampa `1` all'infinito e il programma non termina mai. Se ti succede, fermalo con **Ctrl + C** nel terminale. La causa è quasi sempre l'aggiornamento dimenticato o sbagliato.

Un altro errore frequente è il punto e virgola subito dopo la parentesi:

```cpp
while (i <= 5);     //  il ; chiude il while: il corpo è vuoto
{
    cout << i << endl;
    i++;
}
```

Qui il `while` ripete "niente" all'infinito, e il blocco tra graffe non viene mai considerato parte del ciclo.

## Ciclo `do-while`

Il `do-while` è uguale al `while`, ma controlla la condizione **alla fine**. Il blocco viene quindi eseguito **almeno una volta**, sempre.

### Sintassi

```cpp
do {
    // Codice eseguito almeno una volta
} while (condizione);
```

> [!WARNING]
> Il `do-while` vuole il **punto e virgola** dopo la parentesi finale: `} while (condizione);`

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int i = 1;

    do {
        cout << i << endl;
        i++;
    } while (i <= 5);

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

### `while` contro `do-while`

La differenza si vede solo quando la condizione è **falsa fin dall'inizio**.

```cpp
#include <iostream>
using namespace std;

int main() {
    int i = 10;

    while (i < 5) {
        cout << "while: " << i << endl;     // mai eseguito
        i++;
    }

    int j = 10;

    do {
        cout << "do-while: " << j << endl;  // eseguito una volta
        j++;
    } while (j < 5);

    return 0;
}
```

**Output:**
```
do-while: 10
```

| Ciclo      | Quando controlla la condizione | Esecuzioni minime |
| ---------- | ------------------------------ | ----------------- |
| `while`    | Prima del blocco               | 0                 |
| `do-while` | Dopo il blocco                 | 1                 |

## Quando Usare Quale

Il `do-while` è perfetto quando devi fare qualcosa **prima** di poter valutare la condizione: il caso tipico è chiedere un dato all'utente e ricontrollarlo finché non è valido.

### Esempio: Validazione dell'Input

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta;

    do {
        cout << "Inserisci la tua eta (1-120): ";
        cin >> eta;

        if (eta < 1 || eta > 120) {
            cout << "Valore non valido, riprova." << endl;
        }
    } while (eta < 1 || eta > 120);

    cout << "Hai " << eta << " anni." << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci la tua eta (1-120): 200
Valore non valido, riprova.
Inserisci la tua eta (1-120): -5
Valore non valido, riprova.
Inserisci la tua eta (1-120): 30
Hai 30 anni.
```

Con un `while` normale dovresti chiedere l'età **due volte** nel codice: una prima del ciclo (per avere qualcosa da controllare) e una dentro. Il `do-while` evita la ripetizione.

### Esempio: Ciclo con Sentinella

Una **sentinella** è un valore speciale che segnala la fine. Qui il ciclo somma numeri finché l'utente non inserisce `0`.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    int somma = 0;

    cout << "Inserisci dei numeri (0 per terminare)" << endl;

    cin >> numero;

    while (numero != 0) {
        somma += numero;    // accumula il totale
        cin >> numero;      // legge il prossimo: senza questo, ciclo infinito
    }

    cout << "Somma totale: " << somma << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci dei numeri (0 per terminare)
10
5
3
0
Somma totale: 18
```

> Nota: la variabile `somma` si chiama **accumulatore**. Va sempre inizializzata **prima** del ciclo (a `0` per le somme, a `1` per i prodotti), altrimenti parte da un valore casuale.

## Esempio Completo: Tabellina

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    int contatore = 1;

    cout << "Di quale numero vuoi la tabellina? ";
    cin >> numero;

    while (contatore <= 10) {
        cout << numero << " x " << contatore << " = " << numero * contatore << endl;
        contatore++;
    }

    return 0;
}
```

**Esecuzione:**
```
Di quale numero vuoi la tabellina? 7
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

---

⬅️ [Precedente: Switch](7-switch.md) | [📚 Indice](.github/README.md) | [Successivo: Ciclo for](9-ciclo-for.md) ➡️
