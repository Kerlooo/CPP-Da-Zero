# Tipi di Variabili in C++

In C++ esistono diversi tipi di variabili:
| Tipo                 | Descrizione                           | Intervallo           |
| -------------------- | ------------------------------------- | ------------------------------ |
| `int`                | Intero normale **signed**             | ~ da -2 miliardi a +2 miliardi |
| `float`              | Numero decimale a precisione singola  | ~7 cifre decimali              |
| `double`             | Numero decimale a doppia precisione   | ~15 cifre decimali             |
| `char`               | Singolo carattere (signed o unsigned) | 1 byte                         |
| `string`             | Sringa di caratteri alfanumerici      | Variabile                      |
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
- C++ distingue tra **maiuscole e minuscole** (`eta` ≠ `Eta 
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
