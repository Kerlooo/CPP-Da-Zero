# Stringhe in C++

Una **stringa** è una sequenza di caratteri: una parola, una frase, un nome. L'abbiamo già usata fin dai primi capitoli, ma senza mai guardarci dentro.

```cpp
string nome = "Alice";
```

In C++ esistono due modi di rappresentare del testo: `string`, moderno e comodo, e gli array di `char` ereditati dal C. Partiamo dal primo, che è quello che userai.

## `std::string`

`string` non è un tipo nativo del linguaggio come `int` o `double`: arriva dalla libreria standard. Per usarlo serve il suo header:

```cpp
#include <string>
```

> Nota: `#include <iostream>` spesso include `<string>` di rimbalzo, quindi il codice può compilare anche senza. È un caso fortunato che dipende dal compilatore: se usi le stringhe, includi `<string>` esplicitamente.

### Dichiarazione e Inizializzazione

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string vuota;                       // Stringa vuota, ""
    string nome = "Alice";
    string saluto{"Ciao"};              // Con le graffe
    string copia = nome;                // Copia del contenuto di nome

    return 0;
}
```

A differenza degli array, una `string` non dichiarata non contiene spazzatura: nasce vuota.

## Concatenazione

L'operatore `+` unisce due stringhe. `+=` aggiunge in coda.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nome = "Mario";
    string cognome = "Rossi";

    string completo = nome + " " + cognome;
    cout << completo << endl;           // Mario Rossi

    string frase = "Ciao";
    frase += ", ";
    frase += nome;
    cout << frase << endl;              // Ciao, Mario

    return 0;
}
```

> [!WARNING]
> Il `+` unisce testo, non somma numeri. Due stringhe che contengono cifre vengono attaccate, non addizionate:
> ```cpp
> string a = "5";
> string b = "3";
> cout << a + b << endl;          // 53, non 8
> ```
> Attenzione anche a `"5" + "3"` scritto direttamente con le virgolette: quello è un **errore di compilazione**. Due letterali tra virgolette non sono ancora oggetti `string`, e il `+` fra loro non ha senso. Perché funzioni, almeno uno dei due deve essere una `string`.

Un numero non si può concatenare direttamente a una stringa:

```cpp
int eta = 30;
string testo = "Ho " + eta + " anni";       // ERRORE
```

Con `cout` il problema non si pone, perché `<<` gestisce ogni tipo per conto suo:

```cpp
cout << "Ho " << eta << " anni" << endl;    // Corretto
```

Se ti serve davvero una stringa, converti il numero con `to_string`:

```cpp
string testo = "Ho " + to_string(eta) + " anni";    // Corretto
```

## Lunghezza

`length()` restituisce il numero di caratteri. `size()` fa esattamente la stessa cosa: sono due nomi per la stessa operazione.

```cpp
string parola = "Programmazione";

cout << parola.length() << endl;        // 14
cout << parola.size() << endl;          // 14
```

La sintassi `parola.length()` si chiama **chiamata a metodo**: una funzione che appartiene all'oggetto e si richiama con il punto.

Per sapere se una stringa è vuota, `empty()` è più chiaro di un confronto con zero:

```cpp
string vuota;

if (vuota.empty()) {
    cout << "La stringa è vuota" << endl;
}
```

## Accedere ai Singoli Caratteri

Una stringa si comporta come un array di caratteri: indici tra parentesi quadre, **partendo da zero**.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string parola = "Ciao";

    cout << parola[0] << endl;          // C
    cout << parola[3] << endl;          // o  -> ultimo carattere

    parola[0] = 'M';
    cout << parola << endl;             // Miao

    return 0;
}
```

Il singolo carattere è un `char`, quindi va tra **apici singoli** (`'M'`), non tra virgolette doppie.

L'ultimo carattere sta in posizione `length() - 1`:

```cpp
string parola = "Ciao";
cout << parola[parola.length() - 1] << endl;    // o
```

Come per gli array, l'operatore `[]` **non controlla i limiti**: `parola[100]` su una stringa di 4 caratteri non dà errore, dà comportamento imprevedibile.

> Nota: esiste anche `parola.at(100)`, che fa la stessa cosa ma controlla l'indice e segnala l'errore invece di proseguire alla cieca. È più sicuro, e leggermente più lento.

### Scorrere una Stringa

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string parola = "Ciao";

    for (int i = 0; i < parola.length(); i++) {
        cout << i << ": " << parola[i] << endl;
    }

    // Oppure, se l'indice non serve:
    for (char c : parola) {
        cout << c << " ";
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
0: C
1: i
2: a
3: o
C i a o
```

## Leggere Stringhe da Tastiera

`cin >>` si ferma al **primo spazio**. Per una parola singola va benissimo, per una frase no.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nome;

    cout << "Come ti chiami? ";
    cin >> nome;

    cout << "Ciao " << nome << endl;

    return 0;
}
```

**Esecuzione:**
```
Come ti chiami? Mario Rossi
Ciao Mario
```

Il cognome è sparito: `cin >>` ha letto fino allo spazio e ha lasciato `Rossi` in attesa nel buffer.

### `getline`

Per leggere una riga intera, spazi compresi, si usa `getline`:

```cpp
getline(cin, nome_variabile);
```

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nomeCompleto;

    cout << "Nome e cognome: ";
    getline(cin, nomeCompleto);

    cout << "Ciao " << nomeCompleto << endl;

    return 0;
}
```

**Esecuzione:**
```
Nome e cognome: Mario Rossi
Ciao Mario Rossi
```

### La Trappola di `cin >>` seguito da `getline`

Mescolare i due è la fonte di errori più comune con le stringhe:

```cpp
int eta;
string nome;

cout << "Età: ";
cin >> eta;

cout << "Nome: ";
getline(cin, nome);         // Non aspetta niente: nome resta vuoto
```

Il motivo: `cin >> eta` legge il numero ma **lascia nel buffer l'invio** che hai premuto. `getline` lo trova subito, lo interpreta come fine riga e restituisce una stringa vuota senza fermarsi.

La soluzione è svuotare il buffer prima di chiamare `getline`:

```cpp
#include <iostream>
#include <string>
#include <limits>
using namespace std;

int main() {
    int eta;
    string nome;

    cout << "Età: ";
    cin >> eta;

    cin.ignore(numeric_limits<streamsize>::max(), '\n');    // Scarta il resto della riga

    cout << "Nome: ";
    getline(cin, nome);

    cout << nome << ", " << eta << " anni" << endl;

    return 0;
}
```

`cin.ignore(...)` scarta tutto quello che resta sulla riga corrente, invio compreso. Serve `#include <limits>`.

> Nota: vedrai spesso scritto `cin.ignore();` senza argomenti, che scarta un solo carattere. Funziona nel caso semplice, ma se l'utente ha digitato qualcosa dopo il numero il buffer resta sporco. La forma lunga è quella che regge sempre.

## Metodi Utili

| Metodo                   | Cosa fa                                                | Esempio su `"Programmazione"` |
| ------------------------ | ------------------------------------------------------ | ----------------------------- |
| `length()` / `size()`    | Numero di caratteri                                     | `14`                          |
| `empty()`                | `true` se la stringa è vuota                            | `false`                       |
| `substr(inizio, quanti)` | Estrae una porzione                                     | `substr(0, 7)` → `"Program"`  |
| `find("testo")`          | Posizione della prima occorrenza                        | `find("mm")` → `7`            |
| `append("testo")`        | Aggiunge in coda (come `+=`)                            | —                             |
| `clear()`                | Svuota la stringa                                       | `""`                          |
| `insert(pos, "testo")`   | Inserisce testo in una posizione                        | —                             |
| `erase(pos, quanti)`     | Cancella dei caratteri                                  | —                             |

### `substr`

Estrae una sottostringa: primo argomento la posizione di partenza, secondo quanti caratteri prendere.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string frase = "Buongiorno a tutti";

    cout << frase.substr(0, 10) << endl;    // Buongiorno
    cout << frase.substr(13) << endl;       // tutti  -> da 13 fino alla fine

    return 0;
}
```

Omettendo il secondo argomento, `substr` prende tutto quello che resta.

### `find`

Cerca un testo e restituisce la posizione in cui inizia. Se non lo trova, restituisce il valore speciale `string::npos`.

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string frase = "Impariamo il C++";

    size_t posizione = frase.find("C++");

    if (posizione != string::npos) {
        cout << "Trovato in posizione " << posizione << endl;    // 13
    } else {
        cout << "Non trovato" << endl;
    }

    return 0;
}
```

> Nota: `find` restituisce un `size_t`, un tipo intero senza segno pensato per le dimensioni. Usarlo al posto di `int` evita i confronti anomali con `string::npos`, che è il numero senza segno più grande rappresentabile.

> [!WARNING]
> Controlla sempre il risultato di `find` contro `string::npos` prima di usarlo. Se dai per scontato che il testo ci sia e non c'è, ti ritrovi a lavorare con una posizione senza senso.

## Confrontare Stringhe

Le stringhe si confrontano con gli operatori che già conosci:

```cpp
string a = "mela";
string b = "pera";

if (a == b) { }         // Stesso contenuto?
if (a != b) { }         // Contenuto diverso?
if (a < b) { }          // true: "mela" viene prima di "pera" in ordine alfabetico
```

Il confronto `<` segue l'ordine dei codici dei caratteri, che corrisponde all'ordine alfabetico **solo per lettere dello stesso caso**. Tutte le maiuscole vengono prima di tutte le minuscole:

```cpp
string x = "Zebra";
string y = "ape";

if (x < y) {
    cout << "Zebra viene prima" << endl;    // Questo viene stampato
}
```

`'Z'` ha un codice più basso di `'a'`, quindi `"Zebra"` risulta "minore" di `"ape"`.

## Stringhe in Stile C

Prima di `std::string`, il testo si rappresentava con array di `char` terminati da un carattere speciale, `'\0'` (detto *terminatore nullo*), che segna dove finisce la stringa.

```cpp
char nome[6] = "Mario";     // 5 caratteri + 1 per il terminatore '\0'
```

L'array deve essere **più grande di un posto** rispetto ai caratteri visibili: senza terminatore, le funzioni che leggono la stringa non sanno dove fermarsi e proseguono nella memoria successiva.

Queste stringhe non hanno metodi: si manipolano con funzioni di `<cstring>` come `strlen`, `strcpy`, `strcmp`.

```cpp
#include <iostream>
#include <cstring>
using namespace std;

int main() {
    char parola[20] = "Ciao";

    cout << strlen(parola) << endl;     // 4  -> il terminatore non si conta

    return 0;
}
```

| Operazione        | `std::string`    | Stile C                 |
| ----------------- | ---------------- | ----------------------- |
| Lunghezza         | `s.length()`     | `strlen(s)`             |
| Copia             | `a = b;`         | `strcpy(a, b);`         |
| Concatenazione    | `a + b`          | `strcat(a, b);`         |
| Confronto         | `a == b`         | `strcmp(a, b) == 0`     |
| Dimensione        | Cresce da sola   | Fissa alla dichiarazione |

Nel codice che scrivi tu, usa `std::string`: gestisce la memoria da sola, cresce quando serve e non ti lascia sbagliare il conto del terminatore. Le stringhe in stile C vanno conosciute perché le incontrerai in codice più vecchio e in molte librerie di sistema.

## Esempio Completo: Analisi di una Frase

```cpp
#include <iostream>
#include <string>
using namespace std;

// Prototipi
int contaVocali(const string& testo);
int contaParole(const string& testo);
string inverti(const string& testo);

int main() {
    string frase;

    cout << "Inserisci una frase: ";
    getline(cin, frase);

    cout << "Caratteri: " << frase.length() << endl;
    cout << "Vocali:    " << contaVocali(frase) << endl;
    cout << "Parole:    " << contaParole(frase) << endl;
    cout << "Invertita: " << inverti(frase) << endl;

    return 0;
}

int contaVocali(const string& testo) {
    int totale = 0;

    for (char c : testo) {
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
            totale++;
        }
    }

    return totale;
}

int contaParole(const string& testo) {
    if (testo.empty()) {
        return 0;
    }

    int totale = 1;     // L'ultima parola non è seguita da spazio

    for (char c : testo) {
        if (c == ' ') {
            totale++;
        }
    }

    return totale;
}

string inverti(const string& testo) {
    string risultato;

    for (int i = testo.length() - 1; i >= 0; i--) {
        risultato += testo[i];
    }

    return risultato;
}
```

**Esecuzione:**
```
Inserisci una frase: Ciao a tutti
Caratteri: 12
Vocali:    6
Parole:    3
Invertita: ittut a oaiC
```

> Nota: nei prototipi compare `const string&`. La `&` evita di copiare la stringa a ogni chiamata, il `const` garantisce che la funzione non la modifichi. Copiare una stringa lunga a ogni chiamata costa, e con `&` non succede. Il meccanismo dietro la `&` lo vedremo nel capitolo sui riferimenti: per ora basta sapere che è la forma consigliata per passare una stringa che va solo letta.

---

⬅️ [Precedente: Array](11-array.md) | [📚 Indice](.github/README.md)
