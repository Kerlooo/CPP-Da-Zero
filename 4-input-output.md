# Input/Output in C++

L'Input/Output (I/O) è fondamentale in C++. Permette al programma di:
- **Output**: Visualizzare messaggi e dati sullo schermo (`cout`)
- **Errori**: Segnalare che qualcosa non va, su un canale separato (`cerr`)
- **Input**: Ricevere dati dall'utente tramite tastiera (`cin`)

## Output: `cout`

`cout` (character output) stampa dati sullo schermo.

### Sintassi Base

```cpp
cout << valore;
```

L'operatore `<<` è chiamato **stream insertion operator** e invia i dati verso lo stream di output.

### Esempio (senza usare `namespace std;`)

```cpp
#include <iostream>

int main() {
    std::cout << "Output!";
    std::cout << 42;
    std::cout << 3.14;
    
    return 0;
}
```

**Output:**
```
Output!423.14
```

### Esempi (usando `using namespace std;`)

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Output!";
    cout << 42;
    cout << 3.14;
    
    return 0;
}
```

### Andare a Capo: `endl`

Per andare a capo, si usa `endl` (end line):

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Prima riga" << endl;
    cout << "Seconda riga" << endl;
    cout << "Terza riga" << endl;
    
    return 0;
}
```

**Output:**
```
Prima riga
Seconda riga
Terza riga
```

### Concatenare Output

Puoi concatenare più valori usando più `<<`:

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int eta = 25;
    string nome = "Marco";
    
    cout << "Nome: " << nome << endl;
    cout << "Eta: " << eta << endl;
    cout << "Mi chiamo " << nome << " e ho " << eta << " anni" << endl;
    
    return 0;
}
```

**Output:**
```
Nome: Marco
Eta: 25
Mi chiamo Marco e ho 25 anni
```

## Output degli Errori: `cerr`

`cout` non è l'unico canale di uscita. C++ mette a disposizione anche `cerr` (*character error*), pensato per i **messaggi di errore** e le segnalazioni di problemi.

Si usa esattamente come `cout`, con lo stesso operatore `<<`:

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Messaggio normale" << endl;
    cerr << "Messaggio di errore" << endl;

    return 0;
}
```

Sullo schermo il risultato sembra identico: entrambe le righe compaiono nel terminale. La differenza non si vede, ma c'è.

### Perché Due Canali Diversi

Ogni programma ha due uscite separate:

| Canale         | Nome tecnico        | A cosa serve                              |
| -------------- | ------------------- | ----------------------------------------- |
| `cout`         | standard output     | Il risultato normale del programma        |
| `cerr`         | standard error      | Errori, avvisi, diagnostica               |

Tenerli separati permette a chi usa il programma di **dividere** i due flussi. Da terminale puoi salvare in un file solo il risultato, lasciando che gli errori restino visibili a schermo:

```bash
./programma > risultato.txt
```

Con questo comando, tutto ciò che è passato da `cout` finisce dentro `risultato.txt`, mentre quello scritto con `cerr` continua a comparire sullo schermo. Se avessi stampato gli errori con `cout`, si sarebbero mescolati ai dati veri, finendo nel file insieme a loro.

### `cerr` non Aspetta

C'è una seconda differenza, più sottile. `cout` accumula il testo in una zona di memoria temporanea (il **buffer**) e lo scrive tutto insieme quando conviene, perché è più efficiente. `cerr` invece scrive **subito**, senza accumulare nulla.

Questo conta molto quando un programma va in crash: il messaggio scritto con `cout` potrebbe essere ancora nel buffer e andare perso, mentre quello scritto con `cerr` è già uscito. Per segnalare un errore è esattamente il comportamento che vuoi.

### Quando Usare l'Uno o l'Altro

- **`cout`** — tutto ciò che è il prodotto del programma: risultati, tabelle, richieste all'utente.
- **`cerr`** — tutto ciò che segnala che qualcosa non va: input non valido, file mancante, divisione per zero.

La regola pratica: chiediti se quel testo servirebbe ancora a chi salva l'output in un file. Se la risposta è no, va su `cerr`.

> Nota: esiste anche `clog`, un terzo canale destinato ai messaggi di diagnostica (log). Scrive sullo stesso standard error di `cerr`, ma usa un buffer come `cout`. Nella pratica da principiante ti bastano `cout` e `cerr`.

## Input: `cin`

`cin` (character input) legge dati inseriti dall'utente.

### Sintassi Base

```cpp
cin >> variabile;
```

L'operatore `>>` è chiamato **stream extraction operator** e riceve i dati dallo stream di input.

### Esempi (senza usare `namespace std;`)

```cpp
#include <iostream>

int main() {
    int numero;
    
    std::cout << "Inserisci un numero: ";
    std::cin >> numero;
    std::cout << "Hai inserito: " << numero << std::endl;
    
    return 0;
}
```

**Esecuzione:**
```
Inserisci un numero: 42
Hai inserito: 42
```

### Esempi (usando `namespace std;`)

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    
    cout << "Inserisci un numero: ";
    cin >> numero;
    cout << "Hai inserito: " << numero << endl;
    
    return 0;
}
```

### Leggere Più Input

Puoi leggere più valori concatenando `>>`:

```cpp
#include <iostream>
using namespace std;

int main() {
    int base, altezza;
    cout << "Inserisci base e altezza: ";
    cin >> base >> altezza;

    cout << "Base: " << base << ", altezza: " << altezza << endl;
    
    return 0;
}
```

**Esecuzione:**
```
Inserisci base e altezza: 7 2
Base: 7, altezza: 2
```

I valori si possono separare con uno spazio oppure premendo Invio dopo ciascuno: `cin` li legge nello stesso modo.

> Nota: per lo stesso motivo, `cin >>` con una `string` legge **una sola parola**: si ferma al primo spazio. Se scrivi `Mario Rossi`, nella variabile finisce solo `Mario`. Per leggere una riga intera, spazi compresi, serve `getline`, che vedrai nel [capitolo sulle stringhe](12-stringhe.md).

### Esempio Completo: `cout`, `cin` e `cerr` Insieme

Ora che conosci anche `cin`, ecco un programma che usa tutti e tre i canali. Chiede due numeri e, se il secondo è zero, segnala l'errore su `cerr` invece di dividere.

> Nota: l'`if` serve a eseguire un pezzo di codice solo se una condizione è vera: lo vedrai nel [capitolo 6](6-if-else.md). La divisione tra interi è spiegata nel [capitolo 5](5-operatori-aritmetici.md).

```cpp
#include <iostream>
using namespace std;

int main() {
    int numeratore, denominatore;

    cout << "Inserisci numeratore e denominatore: ";
    cin >> numeratore >> denominatore;

    if (denominatore == 0) {
        cerr << "Errore: divisione per zero" << endl;
        return 1;   // valore diverso da 0 = il programma è terminato male
    }

    cout << "Risultato: " << (numeratore / denominatore) << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci numeratore e denominatore: 10 0
Errore: divisione per zero
```

Nota il `return 1` accanto al messaggio di errore: per convenzione `main` restituisce `0` quando tutto è andato bene e un valore diverso da zero quando qualcosa è fallito. Il messaggio su `cerr` spiega il problema alla persona, il valore di ritorno lo segnala al sistema operativo.

---

⬅️ [Precedente: Tipi di variabili](3-variabili.md) | [📚 Indice](.github/README.md) | [Successivo: Operatori aritmetici](5-operatori-aritmetici.md) ➡️
