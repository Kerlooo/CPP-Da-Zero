# `break` e `continue` in C++

`break` e `continue` servono a modificare il normale svolgimento di un ciclo: il primo lo interrompe, il secondo salta un giro.

| Istruzione  | Cosa fa                                                        |
| ----------- | -------------------------------------------------------------- |
| `break`     | Esce **subito** dal ciclo, che non riprende più                 |
| `continue`  | Salta il **resto dell'iterazione** e passa al giro successivo    |

Funzionano con tutti i cicli: `for`, `while` e `do-while`.

## `break`

Hai già incontrato `break` nello [switch](7-switch.md), dove impedisce il fallthrough. Nei cicli fa una cosa diversa ma simile: abbandona il blocco immediatamente.

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i == 5) {
            break;              // esce dal ciclo: i valori da 5 a 10 non vengono stampati
        }
        cout << i << endl;
    }

    cout << "Ciclo terminato" << endl;

    return 0;
}
```

**Output:**
```
1
2
3
4
Ciclo terminato
```

> Nota: `break` esce **solo dal ciclo**, non dal programma. Il codice scritto dopo il ciclo viene eseguito normalmente. Per terminare l'intero programma dal `main` si usa `return 0;`.

### Quando Serve: Fermarsi Appena Trovato

L'uso tipico è cercare qualcosa: appena lo trovi, continuare a cercare è inutile.

```cpp
#include <iostream>
using namespace std;

int main() {
    int cercato = 7;
    bool trovato = false;

    for (int i = 1; i <= 100; i++) {
        if (i == cercato) {
            trovato = true;
            break;              // inutile controllare gli altri 93 numeri
        }
    }

    if (trovato) {
        cout << "Numero trovato!" << endl;
    }
    else {
        cout << "Numero non presente." << endl;
    }

    return 0;
}
```

**Output:**
```
Numero trovato!
```

### `break` per Uscire da un Ciclo Infinito

Un ciclo con condizione sempre vera (`while (true)`) è legittimo, **a patto** che dentro ci sia un `break` che lo chiude.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;

    while (true) {                      // condizione sempre vera
        cout << "Inserisci un numero (0 per uscire): ";
        cin >> numero;

        if (numero == 0) {
            break;                      // unica via d'uscita
        }

        cout << "Il doppio e': " << numero * 2 << endl;
    }

    cout << "Programma terminato." << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci un numero (0 per uscire): 5
Il doppio e': 10
Inserisci un numero (0 per uscire): 12
Il doppio e': 24
Inserisci un numero (0 per uscire): 0
Programma terminato.
```

> [!WARNING]
> Se scrivi `while (true)` senza un `break` raggiungibile, il programma non termina mai. Controlla sempre che esista almeno una strada che porta al `break`.

## `continue`

`continue` non interrompe il ciclo: salta soltanto le istruzioni rimaste in **quella** iterazione e passa alla successiva.

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i % 2 != 0) {
            continue;           // se i è dispari, salta la stampa
        }
        cout << i << endl;
    }

    return 0;
}
```

**Output:**
```
2
4
6
8
10
```

### Quando Serve: Scartare i Casi da Ignorare

```cpp
#include <iostream>
using namespace std;

int main() {
    int quantita = 5;
    int somma = 0;

    cout << "Inserisci " << quantita << " numeri (gli zeri verranno ignorati)" << endl;

    for (int i = 1; i <= quantita; i++) {
        int numero;
        cout << "Numero " << i << ": ";
        cin >> numero;

        if (numero == 0) {
            cout << "Zero ignorato." << endl;
            continue;           // salta la somma, ma il ciclo prosegue
        }

        somma += numero;
    }

    cout << "Somma dei valori non nulli: " << somma << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci 5 numeri (gli zeri verranno ignorati)
Numero 1: 10
Numero 2: 0
Zero ignorato.
Numero 3: 5
Numero 4: 0
Zero ignorato.
Numero 5: 3
Somma dei valori non nulli: 18
```

## `break` e `continue` a Confronto

Lo stesso ciclo, cambiando solo l'istruzione:

```cpp
// Con break
for (int i = 1; i <= 5; i++) {
    if (i == 3) break;
    cout << i << " ";
}
// Output: 1 2          -> il ciclo muore al 3

// Con continue
for (int i = 1; i <= 5; i++) {
    if (i == 3) continue;
    cout << i << " ";
}
// Output: 1 2 4 5      -> salta solo il 3
```

| Valore di `i` | Con `break`        | Con `continue`   |
| ------------- | ------------------ | ---------------- |
| 1             | stampa `1`         | stampa `1`       |
| 2             | stampa `2`         | stampa `2`       |
| 3             | **esce dal ciclo** | **salta il giro**|
| 4             | —                  | stampa `4`       |
| 5             | —                  | stampa `5`       |

## `continue` nel `while`: Attenzione

In un `for`, l'aggiornamento (`i++`) sta nelle parentesi e viene eseguito **comunque**, anche dopo un `continue`. In un `while`, invece, l'aggiornamento è dentro il corpo: se il `continue` lo scavalca, nasce un ciclo infinito.

```cpp
int i = 0;

while (i < 10) {
    if (i == 5) {
        continue;       //  i resta 5 per sempre: i++ non viene mai raggiunto
    }
    cout << i << endl;
    i++;
}
```

Versione corretta: aggiorna il contatore **anche prima** del `continue`.

```cpp
int i = 0;

while (i < 10) {
    if (i == 5) {
        i++;            // aggiornato prima di saltare: il ciclo va avanti
        continue;
    }
    cout << i << endl;
    i++;
}
```

Stampa i numeri da 0 a 9 saltando il 5, proprio come voleva il codice originale.

> [!WARNING]
> Questo è il motivo per cui, quando serve `continue`, il `for` è più sicuro del `while`.

## Cicli Annidati

`break` e `continue` agiscono **solo sul ciclo che li contiene direttamente**, cioè quello più interno. Il ciclo esterno prosegue indisturbato.

```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= 5; j++) {
            if (j == 3) {
                break;          // esce solo dal ciclo su j
            }
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

Il ciclo su `j` viene interrotto tre volte, una per ogni giro di `i`.

### Uscire da Entrambi i Cicli

C++ non ha un `break` che esce da due cicli in un colpo solo. La soluzione più leggibile è una variabile di controllo (una **flag**) letta anche dal ciclo esterno.

```cpp
#include <iostream>
using namespace std;

int main() {
    bool fermati = false;

    for (int i = 1; i <= 3 && !fermati; i++) {
        for (int j = 1; j <= 3; j++) {
            if (i * j > 4) {
                fermati = true;     // segnala anche al ciclo esterno
                break;              // esce da quello interno
            }
            cout << i << " x " << j << " = " << i * j << endl;
        }
    }

    return 0;
}
```

**Output:**
```
1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
2 x 1 = 2
2 x 2 = 4
```

> Nota: `break` e `continue` vanno usati con misura. Un ciclo pieno di uscite sparse diventa difficile da seguire: spesso una condizione scritta meglio è più chiara di tre `continue`.

---

⬅️ [Precedente: Ciclo for](9-ciclo-for.md) | [📚 Indice](.github/README.md) | [Successivo: Funzioni](10-funzioni.md) ➡️
