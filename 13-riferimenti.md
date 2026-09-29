# Riferimenti in C++

Un **riferimento** è un secondo nome per una variabile che esiste già. Non è una copia e non è una nuova variabile: è la stessa scatola di memoria, raggiungibile con due nomi diversi.

```cpp
int numero = 10;
int& alias = numero;    // alias e numero sono la stessa cosa

alias = 99;
cout << numero << endl;     // 99 -> modificando alias ho modificato numero
```

Hai già incontrato il simbolo `&` in `12-stringhe.md`, nei prototipi scritti `const string&`, con la promessa di spiegarlo più avanti. Questo è il capitolo.

## A Cosa Servono

Nel capitolo sulle [funzioni](10-funzioni.md) hai visto che una funzione riceve una **copia** dei valori che le passi: modificarla dentro non tocca l'originale. È il **passaggio per valore**, ed è il comportamento predefinito.

Va benissimo quasi sempre, ma lascia scoperti due casi:

1. La funzione **deve** modificare la variabile di chi la chiama.
2. Il valore da passare è grosso (per esempio una stringa lunga) e copiarlo a ogni chiamata è uno spreco.

I riferimenti risolvono entrambi.

## Sintassi

La `&` si scrive dopo il tipo, nella dichiarazione:

```cpp
tipo& nome_riferimento = variabile_esistente;
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int punteggio = 100;
    int& rif = punteggio;       // rif si riferisce a punteggio

    cout << punteggio << endl;  // 100
    cout << rif << endl;        // 100

    rif += 50;                  // modifico attraverso il riferimento

    cout << punteggio << endl;  // 150 -> cambiato anche l'originale
    cout << rif << endl;        // 150

    return 0;
}
```

Non esistono "due variabili che valgono 150": esiste **una** variabile con due nomi.

> Nota: dove metti lo spazio non conta. `int& rif`, `int &rif` e `int&rif` sono la stessa dichiarazione. In questa guida usiamo `int&`, che tiene la `&` attaccata al tipo: è un riferimento a `int`.

## Le Tre Regole

### 1. Va inizializzato subito

Un riferimento deve sapere *a cosa* si riferisce nel momento in cui nasce. Non esiste un riferimento "vuoto".

```cpp
int x = 5;

int& a = x;     // Corretto
int& b;         // ERRORE: riferimento non inizializzato
```

È la stessa regola delle costanti `const`, per un motivo simile: senza un valore di partenza, il riferimento non avrebbe senso.

### 2. Non si può cambiare bersaglio

Una volta legato a una variabile, un riferimento resta legato a quella per sempre. Assegnargli un'altra variabile **non** lo sposta: copia il valore.

```cpp
int x = 5;
int y = 99;

int& rif = x;   // rif si riferisce a x

rif = y;        // NON lega rif a y: copia 99 dentro x

cout << x << endl;      // 99  <- x è cambiata
cout << y << endl;      // 99
```

Questo è il punto che confonde di più all'inizio. Dopo `int& rif = x;`, ogni volta che scrivi `rif` stai scrivendo `x`: `rif = y` significa `x = y`.

### 3. Deve riferirsi a qualcosa che esiste

Non puoi legare un riferimento a un valore scritto direttamente nel codice, perché quel valore non è una variabile e non ha un posto stabile in memoria.

```cpp
int& rif = 42;      // ERRORE: 42 non è una variabile
```

> Nota: l'eccezione è il riferimento costante, `const int& rif = 42;`, che invece è permesso. Lo vediamo tra poco.

## Passaggio per Riferimento

È qui che i riferimenti diventano davvero utili. Mettendo la `&` nel parametro di una funzione, la funzione riceve la variabile originale invece di una copia.

### Il Confronto

```cpp
#include <iostream>
using namespace std;

void perValore(int numero) {
    numero = numero * 2;
}

void perRiferimento(int& numero) {
    numero = numero * 2;
}

int main() {
    int a = 10;
    int b = 10;

    perValore(a);
    perRiferimento(b);

    cout << "Per valore:      " << a << endl;
    cout << "Per riferimento: " << b << endl;

    return 0;
}
```

**Output:**
```
Per valore:      10
Per riferimento: 20
```

Una sola `&` di differenza nella firma, due comportamenti opposti. `perValore` ha raddoppiato una copia che è sparita appena la funzione è finita; `perRiferimento` ha raddoppiato `b`.

> [!WARNING]
> Chi legge la **chiamata** non vede nessuna differenza: `perValore(a)` e `perRiferimento(b)` si scrivono identiche. Per sapere se una funzione modificherà la tua variabile devi guardare la sua firma. È il motivo per cui una funzione che modifica un parametro dovrebbe avere un nome che lo dice chiaramente.

### Scambiare Due Variabili

Lo scambio è l'esempio classico: con il passaggio per valore non si può scrivere come funzione, perché la funzione scambierebbe solo le sue copie. Con i riferimenti sì (l'altro modo per farlo sono i puntatori, che vedrai nel prossimo capitolo).

```cpp
#include <iostream>
using namespace std;

void scambia(int& primo, int& secondo) {
    int temporaneo = primo;
    primo = secondo;
    secondo = temporaneo;
}

int main() {
    int a = 1;
    int b = 2;

    cout << "Prima:  a=" << a << " b=" << b << endl;

    scambia(a, b);

    cout << "Dopo:   a=" << a << " b=" << b << endl;

    return 0;
}
```

**Output:**
```
Prima:  a=1 b=2
Dopo:   a=2 b=1
```

Serve la variabile `temporaneo` perché la prima assegnazione distruggerebbe il valore di `primo` prima di poterlo salvare.

### Restituire Più di un Valore

Una funzione può restituire un solo valore con `return`. Se te ne servono due, i parametri per riferimento sono la via più semplice.

```cpp
#include <iostream>
using namespace std;

// Calcola perimetro e area, e li scrive nelle due variabili ricevute
void calcolaRettangolo(int base, int altezza, int& perimetro, int& area) {
    perimetro = (base + altezza) * 2;
    area = base * altezza;
}

int main() {
    int p, a;

    calcolaRettangolo(7, 3, p, a);

    cout << "Perimetro: " << p << endl;     // 20
    cout << "Area: " << a << endl;          // 21

    return 0;
}
```

Nota la divisione dei ruoli: `base` e `altezza` entrano come copie (la funzione li legge soltanto), `perimetro` e `area` sono riferimenti perché è lì che il risultato deve uscire.

## `const` e Riferimenti: Leggere senza Copiare

Il secondo motivo per usare i riferimenti non ha niente a che fare con la modifica: è l'**efficienza**.

Passare una `string` lunga per valore significa copiarne tutti i caratteri a ogni chiamata. Un riferimento evita la copia, ma da solo aprirebbe la porta a modifiche indesiderate. La soluzione è combinarlo con `const`:

```cpp
void stampa(const string& testo) {
    cout << testo << endl;
    // testo = "altro";   // ERRORE: const lo vieta
}
```

Questa firma dice due cose insieme, e le dice a chi legge **e** al compilatore:

| Pezzo    | Cosa garantisce                                  |
| -------- | ------------------------------------------------ |
| `&`      | Non viene fatta nessuna copia                     |
| `const`  | La funzione non modificherà il valore ricevuto    |

È esattamente la forma che hai già visto nell'esempio finale di [12-stringhe.md](12-stringhe.md). In [11-array.md](11-array.md) hai incontrato lo stesso uso di `const` in `const int voti[]`: lì non c'è nessuna `&`, perché gli array non vengono mai copiati, ma il `const` ha lo stesso ruolo di impedire le modifiche.

### La Regola Pratica

| Cosa deve fare la funzione col parametro | Come dichiararlo |
| ---------------------------------------- | ---------------- |
| Solo leggerlo, ed è un tipo piccolo (`int`, `char`, `bool`, `double`) | per valore: `int x` |
| Solo leggerlo, ed è un tipo grosso (`string`, contenitori) | `const string& x` |
| Modificarlo                               | `string& x`      |

Per un `int` il riferimento non conviene: un `int` è così piccolo che copiarlo costa pochissimo, non più che passarlo per riferimento, e la versione per valore si legge meglio.

> Nota: un riferimento `const` può legarsi anche a un valore scritto direttamente, cosa che un riferimento normale non può fare. `const int& r = 42;` è valido: il compilatore crea un valore temporaneo e lo tiene in vita finché serve al riferimento. È il motivo per cui `stampa("Ciao")` funziona anche se `"Ciao"` non è una variabile.

## Riferimenti nel `for` Range-Based

In [11-array.md](11-array.md) c'era una nota rimasta a metà: nel `for` range-based la variabile è una **copia**, quindi modificarla non cambia l'array. Con un riferimento, invece, sì.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numeri[5] = {1, 2, 3, 4, 5};

    for (int n : numeri) {      // n è una copia
        n = n * 10;             // non cambia niente
    }

    for (int n : numeri) {
        cout << n << " ";       // 1 2 3 4 5
    }
    cout << endl;

    for (int& n : numeri) {     // n è un riferimento all'elemento
        n = n * 10;             // modifica davvero l'array
    }

    for (int n : numeri) {
        cout << n << " ";       // 10 20 30 40 50
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
1 2 3 4 5
10 20 30 40 50
```

Anche qui vale la regola del `const`: se devi solo leggere elementi grossi, `for (const string& parola : elenco)` evita una copia per ogni giro.

## Attenzione: la `&` ha Due Significati

Lo stesso simbolo fa due cose completamente diverse a seconda di dove si trova. È la fonte di confusione numero uno del prossimo capitolo.

| Dove appare                       | Cosa significa                     | Esempio        |
| --------------------------------- | ---------------------------------- | -------------- |
| In una **dichiarazione**, dopo il tipo | "questo è un riferimento"     | `int& r = x;`  |
| In un'**espressione**, davanti a una variabile | "dammi l'indirizzo di" | `&x`           |

```cpp
int x = 5;

int& r = x;         // dichiarazione: r è un riferimento a x
cout << &x;         // espressione: stampa l'indirizzo di x in memoria
```

Il secondo uso è il punto di partenza dei [puntatori](14-puntatori.md).

## Errori Frequenti

### Dimenticare la `&` nella funzione

```cpp
void raddoppia(int numero) {        // manca la &
    numero *= 2;
}
```

Il codice compila senza un fiato e non fa niente di visibile. Se una funzione "non funziona" ma non dà errori, controlla per prima cosa se il parametro è un riferimento.

### Restituire un riferimento a una variabile locale

```cpp
int& sbagliata() {
    int locale = 42;
    return locale;      // PERICOLO: locale sparisce appena la funzione finisce
}
```

La variabile muore alla fine della funzione, e il riferimento restituito punta a memoria che non esiste più. Il compilatore di solito avvisa, il programma spesso sembra funzionare, e poi rompe altrove.

> [!WARNING]
> Non restituire mai un riferimento a qualcosa dichiarato dentro la funzione. Per restituire un risultato calcolato lì dentro, usa un normale valore di ritorno: `int corretta() { int locale = 42; return locale; }`.

## Esempio Completo: Statistiche con Più Risultati

```cpp
#include <iostream>
#include <string>
using namespace std;

// Prototipi
void analizza(const int voti[], int dimensione, int& minimo, int& massimo, double& media);
void stampaRiquadro(const string& titolo);

int main() {
    const int DIMENSIONE = 6;
    int voti[DIMENSIONE] = {28, 30, 24, 27, 30, 21};

    int minimo, massimo;
    double media;

    analizza(voti, DIMENSIONE, minimo, massimo, media);

    stampaRiquadro("Statistiche");

    cout << "Minimo:  " << minimo << endl;
    cout << "Massimo: " << massimo << endl;
    cout << "Media:   " << media << endl;

    return 0;
}

// L'array e la dimensione entrano in sola lettura,
// i tre risultati escono attraverso i riferimenti
void analizza(const int voti[], int dimensione, int& minimo, int& massimo, double& media) {
    minimo = voti[0];
    massimo = voti[0];
    int somma = 0;

    for (int i = 0; i < dimensione; i++) {
        if (voti[i] < minimo) {
            minimo = voti[i];
        }
        if (voti[i] > massimo) {
            massimo = voti[i];
        }
        somma += voti[i];
    }

    media = static_cast<double>(somma) / dimensione;
}

// const string& : nessuna copia, nessuna modifica possibile
void stampaRiquadro(const string& titolo) {
    cout << "--- " << titolo << " ---" << endl;
}
```

**Esecuzione:**
```
--- Statistiche ---
Minimo:  21
Massimo: 30
Media:   26.6667
```

Una sola chiamata restituisce tre risultati, e la firma della funzione dice già tutto: `const int voti[]` si legge soltanto, `int&` e `double&` sono le uscite.

---

⬅️ [Precedente: Stringhe](12-stringhe.md) | [📚 Indice](.github/README.md) | [Successivo: Puntatori](14-puntatori.md) ➡️
