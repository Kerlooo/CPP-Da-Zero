# Tipi di Variabili in C++

In C++ esistono diversi tipi di variabili:
| Tipo                 | Descrizione                           | Intervallo           |
| -------------------- | ------------------------------------- | ------------------------------ |
| `int`                | Intero normale **signed**             | ~ da -2 miliardi a +2 miliardi |
| `float`              | Numero decimale a precisione singola  | ~7 cifre decimali              |
| `double`             | Numero decimale a doppia precisione   | ~15 cifre decimali             |
| `char`               | Singolo carattere (signed o unsigned) | 1 byte                         |
| `string`             | Stringa di caratteri alfanumerici      | Variabile                      |
| `bool`               | Valore booleano                       | `true` / `false`               |

> Nota: Gli intervalli possono variare leggermente in base all'architettura, ma quelli indicati sono quelli standard su macchine moderne.

## Tipi di `int`

Le variabili `int` supportano dei modificatori come `signed`, `unsigned`, `short`, `long`. Questi valori modificano l'intervallo (la grandezza del numero inserito).
| Tipo                 | Descrizione                           | Intervallo (tipico)            |
| -------------------- | ------------------------------------- | ------------------------------ |
| `int`                | Intero normale **signed**             | ~ da -2 miliardi a +2 miliardi |
| `short`              | Intero corto **signed**               | da -32,768 a 32,767            |
| `unsigned short`     | Intero corto **unsigned**             | da 0 a 65,535                  |
| `unsigned int`       | Intero normale **unsigned**           | da 0 a ~4 miliardi             |
| `long long`          | Intero lungo **signed**               | da -9e18 a +9e18               |
| `unsigned long long` | Intero lungo **unsigned**             | da 0 a 18e18                   |

## Dichiarazione delle variabili

### Sintassi Base

La dichiarazione di una variabile segue questa struttura:

```cpp
tipo nome_variabile;
```

**Esempi:**
```cpp
int eta;
float altezza;
string nome;
bool attivo;
```

### Assegnazione di un Valore

Dopo la dichiarazione, puoi assegnare un valore usando l'operatore `=`:

```cpp
int eta;
eta = 25;

float altezza;
altezza = 1.80;

string nome;
nome = "Marco";

bool attivo;
attivo = true;
```

### Dichiarazione e Inizializzazione Contemporanea

Puoi dichiarare e assegnare un valore nella stessa riga:

```cpp
int eta = 25;
float altezza = 1.80;
string nome = "Marco";
bool attivo = true;
char lettera = 'A';
```

### Inizializzazione con le Graffe (Modern C++)

C++11 introduce un'altra sintassi usando le graffe `{}`:

```cpp
int numero{42};
float prezzo{19.99};
string messaggio{"Ciao"};
bool flag{false};
```

### Dichiarare Più Variabili dello Stesso Tipo

Puoi dichiarare più variabili insieme:

```cpp
int x = 10, y = 20, z = 30;
float a = 1.5, b = 2.5, c = 3.5;
```

### Esempio Completo

```cpp
#include <iostream>
using namespace std;

int main() {
    // Dichiarazione semplice
    int eta;
    eta = 25;
    
    // Dichiarazione e inizializzazione
    string nome = "Alice";
    float altezza = 1.75;
    bool maggiorenne = true;
    
    // Inizializzazione con graffe
    int anni_esperienza{5};
    
    return 0;
}
```

### Regole Importanti

- I nomi delle variabili iniziano con una **lettera o underscore** `_`
- Contengono solo **lettere, numeri e underscore**
- Non possono iniziare con un **numero**
- Non possono contenere **spazi** o **caratteri speciali**
- C++ distingue tra **maiuscole e minuscole** (`eta` ≠ `Eta`)
- Usa nomi **significativi** e leggibili

**Esempi di nomi validi:**
```cpp
int eta;
int _counter;
float prezzoProdotto;
string nome_utente;
```

**Esempi di nomi NON validi:**
```cpp
int 1numero;        //  Inizia con un numero
int nome utente;    //  Contiene uno spazio
float prezzo-totale; //  Contiene un trattino
```

## Costanti: `const`

A volte un valore non deve **mai** cambiare: il numero di giorni in una settimana, il valore di pi greco, l'aliquota IVA. Per questi casi C++ mette a disposizione la parola chiave `const`.

Una variabile dichiarata `const` diventa una **costante**: puoi leggerla ovunque, ma qualsiasi tentativo di modificarla viene bloccato dal compilatore.

### Sintassi

```cpp
const tipo nome_costante = valore;
```

La parola `const` va prima del tipo, e il valore va assegnato **subito**, nella stessa riga della dichiarazione.

**Esempi:**
```cpp
const int GIORNI_SETTIMANA = 7;
const double PI_GRECO = 3.14159;
const char SEPARATORE = ';';
const string NOME_PROGRAMMA = "Calcolatrice";
```

### Inizializzazione Obbligatoria

Una costante deve ricevere il suo valore nel momento in cui nasce. Non puoi dichiararla vuota e riempirla dopo:

```cpp
const int MAX = 100;   // Corretto

const int MIN;         // ERRORE: costante senza valore iniziale
MIN = 0;               // ERRORE: non si può assegnare a una costante
```

### Cosa Succede se Provi a Modificarla

Il compilatore si ferma e segnala l'errore **prima** che il programma venga eseguito. Non è un controllo che avviene mentre il programma gira: è un controllo fatto in fase di compilazione.

```cpp
#include <iostream>
using namespace std;

int main() {
    const double ALIQUOTA_IVA = 0.22;

    double prezzo = 100.0;
    double totale = prezzo + (prezzo * ALIQUOTA_IVA);   // Leggere va benissimo

    cout << "Totale con IVA: " << totale << endl;       // Totale con IVA: 122

    // ALIQUOTA_IVA = 0.10;   // Se togli il commento, il programma non compila

    return 0;
}
```

### Perché Usare `const`

- **Il compilatore ti protegge.** Un valore che non deve cambiare non può essere modificato per sbaglio da una riga scritta distrattamente.
- **Il codice si spiega da solo.** `prezzo * 0.22` costringe chi legge a chiedersi cosa sia quel `0.22`. `prezzo * ALIQUOTA_IVA` si capisce al volo.
- **Le modifiche si fanno in un punto solo.** Se l'IVA passa dal 22% al 20%, cambi una riga invece di cercare tutti i `0.22` sparsi nel programma.

I numeri scritti direttamente nel codice, come quel `0.22`, si chiamano **numeri magici**: funzionano, ma nessuno sa da dove arrivino. Sostituirli con costanti dal nome chiaro è una delle abitudini che distinguono il codice ordinato da quello confuso.

### Convenzione sui Nomi

Le costanti si scrivono per tradizione **tutte in maiuscolo**, con l'underscore a separare le parole:

```cpp
const int NUMERO_MASSIMO_TENTATIVI = 3;
const double VELOCITA_LUCE = 299792458.0;
```

Non è un obbligo del linguaggio: il programma compila anche scrivendo `const int numeroMassimoTentativi = 3;`. È una convenzione condivisa che permette di riconoscere una costante a colpo d'occhio, senza andare a cercare dove è stata dichiarata.

> Nota: esiste anche `#define`, un vecchio meccanismo ereditato dal C che permette di definire valori fissi. Funziona in modo completamente diverso (è una sostituzione di testo fatta prima della compilazione, senza controllo di tipo) ed è oggi sconsigliato per le costanti. In C++ usa `const`.

---

⬅️ [Precedente: Come si strutturano i programmi](2-struttura.md) | [📚 Indice](.github/README.md) | [Successivo: Input e Output](4-input-output.md) ➡️
