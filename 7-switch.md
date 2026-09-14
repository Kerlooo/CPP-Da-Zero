# Switch in C++

Lo `switch` è un'alternativa più ordinata alla catena `if / else if / else` quando devi confrontare **una sola variabile** con **tanti valori fissi**.

## Sintassi

```cpp
switch (espressione) {
    case valore1:
        // Codice eseguito se espressione == valore1
        break;
    case valore2:
        // Codice eseguito se espressione == valore2
        break;
    default:
        // Codice eseguito se nessun case corrisponde
}
```

**Componenti:**
- `switch (espressione)` → il valore da confrontare, valutato **una volta sola**
- `case valore:` → un valore possibile da confrontare
- `break;` → esce dallo `switch`, salta tutto il resto
- `default:` → il caso "tutti gli altri", come l'`else` finale

## Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int giorno = 3;

    switch (giorno) {
        case 1:
            cout << "Lunedi" << endl;
            break;
        case 2:
            cout << "Martedi" << endl;
            break;
        case 3:
            cout << "Mercoledi" << endl;
            break;
        case 4:
            cout << "Giovedi" << endl;
            break;
        case 5:
            cout << "Venerdi" << endl;
            break;
        default:
            cout << "Weekend o giorno non valido" << endl;
    }

    return 0;
}
```

**Output:**
```
Mercoledi
```

## L'Importanza del `break`

Senza `break`, l'esecuzione **non si ferma** al `case` che ha corrisposto: continua verso il basso eseguendo anche i `case` successivi. Questo comportamento si chiama **fallthrough**.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 2;

    switch (numero) {
        case 1:
            cout << "Uno" << endl;
        case 2:
            cout << "Due" << endl;      // qui entra...
        case 3:
            cout << "Tre" << endl;      // ...e prosegue!
        default:
            cout << "Default" << endl;  // ...fino alla fine
    }

    return 0;
}
```

**Output:**
```
Due
Tre
Default
```

> [!WARNING]
> Dimenticare il `break` è l'errore più comune con lo `switch`. Il compilatore **non segnala nessun errore**: il programma compila e fa una cosa diversa da quella che volevi.

## Fallthrough Voluto: Più Valori, Stesso Codice

Il fallthrough non è sempre un errore. Lasciando dei `case` **vuoti** uno sopra l'altro, puoi far eseguire lo stesso blocco di codice a più valori.

```cpp
#include <iostream>
using namespace std;

int main() {
    char voto = 'B';

    switch (voto) {
        case 'A':
        case 'B':
        case 'C':
            cout << "Promosso!" << endl;
            break;
        case 'D':
        case 'F':
            cout << "Bocciato." << endl;
            break;
        default:
            cout << "Voto non valido." << endl;
    }

    return 0;
}
```

**Output:**
```
Promosso!
```

## Il `default`

Il `default` è **facoltativo**: se lo ometti e nessun `case` corrisponde, lo `switch` semplicemente non esegue niente.

Può stare in qualsiasi posizione, ma per convenzione si scrive **per ultimo**. Se lo metti in mezzo, ricordati il `break`, altrimenti il fallthrough continuerà sui `case` sotto di lui.

```cpp
#include <iostream>
using namespace std;

int main() {
    int opzione = 9;

    switch (opzione) {
        case 1:
            cout << "Hai scelto: Nuova partita" << endl;
            break;
        case 2:
            cout << "Hai scelto: Carica partita" << endl;
            break;
        default:
            cout << "Opzione non riconosciuta" << endl;
    }

    return 0;
}
```

**Output:**
```
Opzione non riconosciuta
```

## Cosa Può Andare in uno `switch`

Lo `switch` non funziona con qualsiasi tipo: accetta solo valori che il computer tratta come **numeri interi**.

| Tipo                | Funziona? | Perché |
| ------------------- | --------- | ------ |
| `int`, `short`, `long` | Sì     | Sono interi |
| `char`              | Sì        | Internamente è un numero (il codice del carattere) |
| `bool`              | Sì        | Vale 0 o 1 (ma con due soli casi conviene l'`if`) |
| `enum`              | Sì        | È una lista di costanti intere |
| `float`, `double`   | No        | Errore di compilazione |
| `string`            | No        | Errore di compilazione |

Ci sono altre due regole da rispettare:

- I valori dei `case` devono essere **costanti note in fase di compilazione** (`case 3:` va bene, `case x:` con `x` variabile no).
- Ogni valore può comparire in **un solo** `case`: due `case 3:` nello stesso `switch` sono un errore.

```cpp
// NON compila: lo switch non accetta le stringhe
string comando = "start";
switch (comando) {      //  errore
    case "start":       //  errore
        break;
}
```

> Nota: per confrontare stringhe o intervalli di valori (`voto >= 90`), devi usare `if / else if`.

## `switch` o `if / else if`?

| Situazione                                   | Cosa usare      |
| -------------------------------------------- | --------------- |
| Una variabile confrontata con valori esatti   | `switch`        |
| Intervalli di valori (`voto >= 90`)           | `if / else if`  |
| Condizioni con `&&`, `\|\|`, `!`              | `if / else if`  |
| Confronto tra `string`, `float` o `double`    | `if / else if`  |
| Menu a scelta numerica, giorni, mesi, comandi | `switch`        |

Lo stesso menu scritto nei due modi:

```cpp
// Con if / else if
if (scelta == 1) {
    cout << "Nuova partita" << endl;
}
else if (scelta == 2) {
    cout << "Carica partita" << endl;
}
else if (scelta == 3) {
    cout << "Esci" << endl;
}
else {
    cout << "Scelta non valida" << endl;
}

// Con switch: stessa logica, ma si legge meglio
switch (scelta) {
    case 1:
        cout << "Nuova partita" << endl;
        break;
    case 2:
        cout << "Carica partita" << endl;
        break;
    case 3:
        cout << "Esci" << endl;
        break;
    default:
        cout << "Scelta non valida" << endl;
}
```

## Esempio Completo: Calcolatrice

```cpp
#include <iostream>
using namespace std;

int main() {
    double a, b;
    char operatore;

    cout << "Inserisci il primo numero: ";
    cin >> a;
    cout << "Inserisci l'operatore (+ - * /): ";
    cin >> operatore;
    cout << "Inserisci il secondo numero: ";
    cin >> b;

    switch (operatore) {
        case '+':
            cout << "Risultato: " << a + b << endl;
            break;
        case '-':
            cout << "Risultato: " << a - b << endl;
            break;
        case '*':
            cout << "Risultato: " << a * b << endl;
            break;
        case '/':
            // Controlliamo il divisore prima di dividere
            if (b == 0) {
                cout << "Errore: divisione per zero" << endl;
            }
            else {
                cout << "Risultato: " << a / b << endl;
            }
            break;
        default:
            cout << "Operatore non riconosciuto" << endl;
    }

    return 0;
}
```

**Esecuzione:**
```
Inserisci il primo numero: 10
Inserisci l'operatore (+ - * /): /
Inserisci il secondo numero: 4
Risultato: 2.5
```

> Nota: i `case` confrontano un `char`, quindi i valori vanno scritti tra **apici singoli** (`'+'`), non tra virgolette doppie (`"+"`), che indicano una stringa.

---

⬅️ [Precedente: Operatore ternario](6-operatore-ternario.md) | [📚 Indice](.github/README.md) | [Successivo: Ciclo while](8-ciclo-while.md) ➡️
