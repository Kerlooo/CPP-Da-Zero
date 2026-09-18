# Funzioni in C++

Una **funzione** è un blocco di codice con un nome, che esegue un compito preciso e che puoi richiamare tutte le volte che vuoi.

Finora tutto il codice che abbiamo scritto stava dentro `main`. Funziona finché il programma è piccolo, ma appena cresce diventa ingestibile: centinaia di righe di seguito, con pezzi di logica ripetuti più volte.

Senza funzioni:

```cpp
// Calcolo l'area del primo rettangolo
int area1 = 5 * 3;
cout << "Area: " << area1 << endl;

// Calcolo l'area del secondo rettangolo
int area2 = 7 * 2;
cout << "Area: " << area2 << endl;

// ...e ogni volta riscrivo le stesse due righe
```

Con una funzione, quella logica la scrivi **una volta sola** e la richiami quando serve.

## La Prima Funzione

```cpp
#include <iostream>
using namespace std;

// Definizione della funzione
void saluta() {
    cout << "Ciao!" << endl;
}

int main() {
    saluta();       // Chiamata: esegue il codice della funzione
    saluta();       // Posso richiamarla quante volte voglio
    saluta();

    return 0;
}
```

**Output:**
```
Ciao!
Ciao!
Ciao!
```

Due momenti diversi, da non confondere:

- La **definizione** descrive cosa fa la funzione. Scriverla non esegue niente.
- La **chiamata** (`saluta();`) è il momento in cui il codice viene davvero eseguito.

Quando il programma incontra una chiamata, salta dentro la funzione, esegue le sue istruzioni, poi torna esattamente al punto da cui era partito e prosegue.

## Sintassi

```cpp
tipo_restituito nome_funzione(parametri) {
    // Corpo della funzione
    return valore;
}
```

| Parte              | Cosa indica                                              |
| ------------------ | -------------------------------------------------------- |
| `tipo_restituito`  | Il tipo del valore che la funzione restituisce            |
| `nome_funzione`    | Il nome con cui la richiami                               |
| `parametri`        | I dati che la funzione riceve dall'esterno (possono mancare) |
| `return`           | L'istruzione che restituisce il risultato e chiude la funzione |

Il nome segue le stesse regole delle variabili. Per convenzione descrive un'**azione**: `calcolaArea`, `stampaMenu`, `leggiEta`.

## Il Tipo `void`

`void` significa "nessun valore". Una funzione `void` fa qualcosa — stampa a schermo, modifica qualcosa — ma non restituisce niente a chi l'ha chiamata.

```cpp
void stampaLinea() {
    cout << "------------------------" << endl;
}
```

In una funzione `void` il `return` non serve: si può omettere.

## Funzioni che Restituiscono un Valore

Quando il tipo è diverso da `void`, la funzione **deve** restituire un valore di quel tipo con `return`.

```cpp
#include <iostream>
using namespace std;

int quadrato(int numero) {
    return numero * numero;
}

int main() {
    int risultato = quadrato(5);        // risultato vale 25

    cout << risultato << endl;          // 25
    cout << quadrato(3) << endl;        // 9, usata direttamente
    cout << quadrato(2) + 10 << endl;   // 14, il valore entra nell'espressione

    return 0;
}
```

La chiamata `quadrato(5)` **diventa** il valore `25`: puoi salvarlo in una variabile, stamparlo o usarlo dentro un calcolo più grande, come faresti con un numero qualsiasi.

### `return` Chiude la Funzione

Appena il programma incontra un `return`, esce immediatamente dalla funzione. Le righe successive non vengono eseguite.

```cpp
int valoreAssoluto(int n) {
    if (n < 0) {
        return -n;      // Se n è negativo, esce qui
    }

    return n;           // Ci arriva solo se n è positivo o zero
}
```

## Parametri e Argomenti

I **parametri** sono le variabili dichiarate nella definizione. Gli **argomenti** sono i valori che passi al momento della chiamata.

```cpp
int somma(int a, int b) {     // a e b sono i parametri
    return a + b;
}

int main() {
    int x = somma(3, 7);      // 3 e 7 sono gli argomenti
    return 0;
}
```

I parametri si separano con la virgola e **ognuno vuole il suo tipo**:

```cpp
int somma(int a, int b) { }       // Corretto
int somma(int a, b) { }           // ERRORE: manca il tipo di b
```

Gli argomenti devono corrispondere ai parametri per **numero**, **ordine** e **tipo**:

```cpp
void mostraDati(string nome, int eta) {
    cout << nome << " ha " << eta << " anni" << endl;
}

int main() {
    mostraDati("Alice", 30);     // Corretto
    mostraDati(30, "Alice");     // ERRORE: ordine invertito
    mostraDati("Alice");         // ERRORE: manca un argomento

    return 0;
}
```

### Passaggio per Valore

Quando passi una variabile a una funzione, la funzione riceve una **copia** del valore. Modificarla dentro la funzione non tocca l'originale.

```cpp
#include <iostream>
using namespace std;

void raddoppia(int numero) {
    numero = numero * 2;
    cout << "Dentro la funzione: " << numero << endl;
}

int main() {
    int valore = 10;

    raddoppia(valore);
    cout << "Fuori dalla funzione: " << valore << endl;

    return 0;
}
```

**Output:**
```
Dentro la funzione: 20
Fuori dalla funzione: 10
```

`valore` resta `10`: la funzione ha lavorato su una copia. Questo comportamento si chiama **passaggio per valore** ed è quello predefinito in C++. Esiste anche il passaggio per riferimento, che permette di modificare davvero l'originale, ma lo vedremo più avanti.

## Lo Scope delle Variabili

Le variabili dichiarate dentro una funzione **esistono solo lì**. Nascono quando la funzione parte e spariscono quando finisce.

```cpp
void funzioneA() {
    int contatore = 5;      // Esiste solo dentro funzioneA
}

void funzioneB() {
    cout << contatore;      // ERRORE: qui contatore non esiste
}
```

Questo è un vantaggio, non un limite: due funzioni possono usare variabili con lo stesso nome senza disturbarsi, perché ognuna lavora nel proprio spazio.

```cpp
void primaFunzione() {
    int i = 10;         // La i di primaFunzione
}

void secondaFunzione() {
    int i = 99;         // Una i completamente diversa
}
```

## L'Ordine di Definizione Conta

Il compilatore legge il file dall'alto verso il basso. Se chiami una funzione prima di averla definita, il compilatore non sa cosa sia:

```cpp
int main() {
    saluta();           // ERRORE: saluta non è ancora stata definita
    return 0;
}

void saluta() {
    cout << "Ciao!" << endl;
}
```

La soluzione più semplice è definire le funzioni **prima** di `main`. Ma con molte funzioni che si chiamano a vicenda, l'ordine giusto diventa difficile da trovare.

### Prototipi

Un **prototipo** (o *dichiarazione*) annuncia al compilatore che una funzione esiste, senza scriverne ancora il corpo. È la prima riga della funzione seguita da un punto e virgola.

```cpp
#include <iostream>
using namespace std;

// Prototipi: dichiaro le funzioni
void saluta();
int somma(int a, int b);

int main() {
    saluta();                       // Il compilatore sa già che esiste
    cout << somma(3, 4) << endl;

    return 0;
}

// Definizioni: scrivo il corpo dopo main
void saluta() {
    cout << "Ciao!" << endl;
}

int somma(int a, int b) {
    return a + b;
}
```

Con i prototipi in cima al file, `main` resta la prima cosa che si legge e l'ordine delle definizioni non conta più.

> Nota: nel prototipo i nomi dei parametri sono facoltativi: `int somma(int, int);` è altrettanto valido. Scriverli comunque aiuta chi legge a capire cosa rappresentano.

## Parametri con Valore di Default

Un parametro può avere un valore predefinito, usato quando chi chiama la funzione non lo passa.

```cpp
#include <iostream>
using namespace std;

void stampaLinea(char simbolo = '-', int lunghezza = 20) {
    for (int i = 0; i < lunghezza; i++) {
        cout << simbolo;
    }
    cout << endl;
}

int main() {
    stampaLinea();            // -------------------- (usa entrambi i default)
    stampaLinea('*');         // ******************** (lunghezza resta 20)
    stampaLinea('=', 10);     // ========== (nessun default usato)

    return 0;
}
```

I parametri con default devono stare **in fondo** alla lista. Altrimenti il compilatore non saprebbe a quale parametro assegnare un argomento mancante:

```cpp
void esempio(int a, int b = 5);     // Corretto
void esempio(int a = 5, int b);     // ERRORE: il default non può precedere un parametro senza default
```

## Overload: Stesso Nome, Parametri Diversi

C++ permette di dare lo **stesso nome** a più funzioni, purché abbiano parametri diversi per numero o tipo. Si chiama **overload** (sovraccarico).

```cpp
#include <iostream>
using namespace std;

int somma(int a, int b) {
    return a + b;
}

double somma(double a, double b) {
    return a + b;
}

int somma(int a, int b, int c) {
    return a + b + c;
}

int main() {
    cout << somma(3, 4) << endl;          // 7    -> versione con due int
    cout << somma(1.5, 2.5) << endl;      // 4    -> versione con due double
    cout << somma(1, 2, 3) << endl;       // 6    -> versione con tre int

    return 0;
}
```

Il compilatore sceglie la versione giusta guardando gli argomenti della chiamata. Senza overload dovresti inventare nomi come `sommaInteri`, `sommaDecimali`, `sommaTre`.

> [!WARNING]
> Il tipo restituito **non** basta a distinguere due funzioni. `int valore()` e `double valore()` sono un errore di compilazione: la differenza deve stare nei parametri.

## `main` è una Funzione

`int main()` è la funzione da cui parte ogni programma C++. Il sistema operativo la chiama automaticamente all'avvio.

Il suo tipo restituito è `int`, e il `return 0;` che scrivi alla fine comunica al sistema che il programma è terminato senza errori. Un valore diverso da zero segnala che qualcosa è andato storto.

## Esempio Completo: Calcolatrice

```cpp
#include <iostream>
using namespace std;

// Prototipi
void stampaMenu();
double somma(double a, double b);
double sottrazione(double a, double b);
double moltiplicazione(double a, double b);
double divisione(double a, double b);

int main() {
    int scelta;
    double primo, secondo;

    stampaMenu();

    cout << "Scelta: ";
    cin >> scelta;

    cout << "Inserisci due numeri: ";
    cin >> primo >> secondo;

    switch (scelta) {
        case 1:
            cout << "Risultato: " << somma(primo, secondo) << endl;
            break;
        case 2:
            cout << "Risultato: " << sottrazione(primo, secondo) << endl;
            break;
        case 3:
            cout << "Risultato: " << moltiplicazione(primo, secondo) << endl;
            break;
        case 4:
            if (secondo == 0) {
                cout << "Errore: divisione per zero" << endl;
            } else {
                cout << "Risultato: " << divisione(primo, secondo) << endl;
            }
            break;
        default:
            cout << "Scelta non valida" << endl;
    }

    return 0;
}

// Definizioni
void stampaMenu() {
    cout << "1. Somma" << endl;
    cout << "2. Sottrazione" << endl;
    cout << "3. Moltiplicazione" << endl;
    cout << "4. Divisione" << endl;
}

double somma(double a, double b) {
    return a + b;
}

double sottrazione(double a, double b) {
    return a - b;
}

double moltiplicazione(double a, double b) {
    return a * b;
}

double divisione(double a, double b) {
    return a / b;
}
```

**Esecuzione:**
```
1. Somma
2. Sottrazione
3. Moltiplicazione
4. Divisione
Scelta: 3
Inserisci due numeri: 4 2.5
Risultato: 10
```

`main` ora si legge in pochi secondi: dice **cosa** succede, non **come**. Il come sta nelle singole funzioni, ognuna responsabile di una cosa sola.

## Consigli Pratici

- **Una funzione, un compito.** Se per descrivere cosa fa devi usare la parola "e", probabilmente sono due funzioni.
- **Nomi che dicono l'azione.** `calcolaMedia` si capisce, `funzione2` no.
- **Funzioni corte.** Se una funzione non entra nello schermo, di solito contiene una funzione più piccola che chiede di uscire.
- **Ripetizione = funzione mancante.** Lo stesso blocco copiato in tre punti è un segnale: va estratto in una funzione.

---

⬅️ [Precedente: Break e Continue](9-break-continue.md) | [📚 Indice](.github/README.md) | [Successivo: Array](11-array.md) ➡️
