# Array in C++

Un **array** è una variabile che contiene più valori dello stesso tipo, uno dopo l'altro.

Immagina di dover memorizzare i voti di 30 studenti. Con le variabili che conosciamo finora:

```cpp
int voto1, voto2, voto3, voto4, voto5;      // ...e così via fino a voto30
```

Trenta variabili da dichiarare, da riempire una per una, impossibili da scorrere con un ciclo. Un array risolve tutto con una riga sola.

## Dichiarazione

```cpp
tipo nome_array[dimensione];
```

La **dimensione** è quanti elementi l'array può contenere. Va decisa alla dichiarazione e non cambia più.

```cpp
int voti[30];           // 30 interi
double prezzi[10];      // 10 decimali
char lettere[5];        // 5 caratteri
```

> [!WARNING]
> La dimensione di un array dichiarato così deve essere un valore **noto al momento della compilazione**: un numero scritto direttamente o una costante `const`. Non può essere una variabile letta da tastiera.
> ```cpp
> const int MAX = 50;
> int valori[MAX];        // Corretto
>
> int n;
> cin >> n;
> int altri[n];           // Non è C++ standard: alcuni compilatori lo accettano, altri no
> ```

## Inizializzazione

Puoi riempire l'array alla dichiarazione, elencando i valori tra graffe:

```cpp
int voti[5] = {28, 30, 24, 27, 30};
```

Se elenchi i valori, la dimensione si può omettere: la calcola il compilatore.

```cpp
int voti[] = {28, 30, 24, 27, 30};      // Dimensione 5, dedotta dai valori
```

Se indichi meno valori della dimensione, i restanti vengono messi a **zero**:

```cpp
int numeri[5] = {1, 2};         // {1, 2, 0, 0, 0}
int azzerato[5] = {};           // {0, 0, 0, 0, 0}
```

Il contrario non è permesso: elencare più valori della dimensione dichiarata è un errore di compilazione.

> [!WARNING]
> Un array dichiarato senza inizializzazione **non** contiene zeri: contiene valori casuali, resti di quello che c'era in memoria prima.
> ```cpp
> int voti[5];              // Contenuto imprevedibile
> cout << voti[0];          // Stampa un numero qualsiasi
> ```
> Riempi sempre un array prima di leggerlo.

## Accedere agli Elementi

Ogni elemento si raggiunge con il suo **indice**, tra parentesi quadre.

```cpp
nome_array[indice]
```

**Gli indici partono da zero.** Il primo elemento è in posizione `0`, il secondo in posizione `1`, e l'ultimo di un array di `n` elementi è in posizione `n - 1`.

```cpp
int voti[5] = {28, 30, 24, 27, 30};

cout << voti[0] << endl;        // 28  -> primo elemento
cout << voti[4] << endl;        // 30  -> ultimo elemento (indice 4, non 5)
```

| Indice  | 0  | 1  | 2  | 3  | 4  |
| ------- | -- | -- | -- | -- | -- |
| Valore  | 28 | 30 | 24 | 27 | 30 |

Un elemento si comporta esattamente come una normale variabile: si legge e si modifica.

```cpp
voti[2] = 25;           // Modifica il terzo elemento
voti[0]++;              // Incrementa il primo
int primo = voti[0];    // Copia il valore in un'altra variabile
```

## Scorrere un Array con un Ciclo

È qui che gli array mostrano la loro utilità: un ciclo `for` visita tutti gli elementi in tre righe.

```cpp
#include <iostream>
using namespace std;

int main() {
    int voti[5] = {28, 30, 24, 27, 30};

    for (int i = 0; i < 5; i++) {
        cout << "Voto " << i + 1 << ": " << voti[i] << endl;
    }

    return 0;
}
```

**Output:**
```
Voto 1: 28
Voto 2: 30
Voto 3: 24
Voto 4: 27
Voto 5: 30
```

La condizione è `i < 5`, non `i <= 5`: l'ultimo indice valido è `4`. È l'errore *off by one* già incontrato con i cicli, e sugli array è particolarmente pericoloso.

### Usare una Costante per la Dimensione

Scrivere `5` in più punti significa doverli cambiare tutti insieme il giorno in cui l'array cresce. Meglio una costante:

```cpp
#include <iostream>
using namespace std;

int main() {
    const int NUMERO_VOTI = 5;
    int voti[NUMERO_VOTI] = {28, 30, 24, 27, 30};

    for (int i = 0; i < NUMERO_VOTI; i++) {
        cout << voti[i] << " ";
    }
    cout << endl;

    return 0;
}
```

Un solo punto da modificare, e nessun rischio di dimenticarne uno.

## Il Ciclo `for` Range-Based

Quando ti serve solo scorrere i valori, senza sapere in che posizione si trovano, C++11 offre una forma più corta:

```cpp
for (tipo elemento : array) {
    // Usa elemento
}
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int voti[5] = {28, 30, 24, 27, 30};

    for (int voto : voti) {
        cout << voto << " ";
    }
    cout << endl;

    return 0;
}
```

**Output:**
```
28 30 24 27 30
```

Non c'è nessun indice da gestire, quindi nessun modo di sbagliarlo. Il limite è proprio quello: se ti serve la posizione dell'elemento, o devi modificarlo, torna al `for` classico.

> Nota: in questa forma `voto` è una **copia** dell'elemento. Modificarlo non cambia l'array.

## Il Pericolo: Uscire dai Limiti

C++ **non controlla** se l'indice che usi è valido. Chiedere l'elemento `10` di un array da 5 non produce un errore: il programma legge o scrive la memoria che si trova lì, qualunque cosa sia.

```cpp
int voti[5] = {28, 30, 24, 27, 30};

cout << voti[10];       // Nessun errore di compilazione. Stampa spazzatura.
voti[10] = 99;          // Peggio: scrive in memoria che non ti appartiene
```

> [!WARNING]
> Scrivere fuori dai limiti di un array è uno degli errori più gravi in C++. Il programma può continuare come se niente fosse e poi crashare molto più avanti, in un punto che con l'array non c'entra nulla. Oppure può non crashare mai e darti risultati sbagliati.
> Il controllo degli indici è responsabilità **tua**, non del linguaggio.

Quando l'indice arriva da fuori, controllalo sempre:

```cpp
#include <iostream>
using namespace std;

int main() {
    const int DIMENSIONE = 5;
    int voti[DIMENSIONE] = {28, 30, 24, 27, 30};
    int posizione;

    cout << "Quale voto vuoi vedere (0-4)? ";
    cin >> posizione;

    if (posizione >= 0 && posizione < DIMENSIONE) {
        cout << "Voto: " << voti[posizione] << endl;
    } else {
        cout << "Posizione non valida" << endl;
    }

    return 0;
}
```

## Operazioni Comuni

### Riempire da Tastiera

```cpp
#include <iostream>
using namespace std;

int main() {
    const int DIMENSIONE = 5;
    int numeri[DIMENSIONE];

    for (int i = 0; i < DIMENSIONE; i++) {
        cout << "Inserisci il numero " << i + 1 << ": ";
        cin >> numeri[i];
    }

    return 0;
}
```

### Somma e Media

```cpp
#include <iostream>
using namespace std;

int main() {
    const int DIMENSIONE = 5;
    int voti[DIMENSIONE] = {28, 30, 24, 27, 30};
    int somma = 0;

    for (int i = 0; i < DIMENSIONE; i++) {
        somma += voti[i];
    }

    double media = static_cast<double>(somma) / DIMENSIONE;

    cout << "Somma: " << somma << endl;         // Somma: 139
    cout << "Media: " << media << endl;         // Media: 27.8

    return 0;
}
```

Il `static_cast` serve perché `somma` e `DIMENSIONE` sono entrambi interi: senza, la media verrebbe troncata a `27`.

### Trovare il Massimo

```cpp
#include <iostream>
using namespace std;

int main() {
    const int DIMENSIONE = 5;
    int voti[DIMENSIONE] = {28, 30, 24, 27, 30};

    int massimo = voti[0];      // Parto dal primo elemento

    for (int i = 1; i < DIMENSIONE; i++) {
        if (voti[i] > massimo) {
            massimo = voti[i];
        }
    }

    cout << "Voto massimo: " << massimo << endl;   // 30

    return 0;
}
```

Il massimo parte dal primo elemento, non da zero: se tutti i valori fossero negativi, uno zero iniziale resterebbe per sempre il massimo, sbagliando il risultato.

### Cercare un Valore

```cpp
#include <iostream>
using namespace std;

int main() {
    const int DIMENSIONE = 5;
    int numeri[DIMENSIONE] = {10, 25, 3, 47, 8};
    int cercato = 47;
    int posizione = -1;         // -1 significa "non trovato"

    for (int i = 0; i < DIMENSIONE; i++) {
        if (numeri[i] == cercato) {
            posizione = i;
            break;              // Trovato: inutile continuare
        }
    }

    if (posizione != -1) {
        cout << "Trovato in posizione " << posizione << endl;
    } else {
        cout << "Non trovato" << endl;
    }

    return 0;
}
```

## Array e Funzioni

Un array passato a una funzione **non viene copiato**: la funzione lavora direttamente sull'originale. Questo è diverso da tutto quello che hai visto finora sul passaggio per valore.

```cpp
#include <iostream>
using namespace std;

void raddoppiaTutti(int numeri[], int dimensione) {
    for (int i = 0; i < dimensione; i++) {
        numeri[i] *= 2;
    }
}

int main() {
    int valori[4] = {1, 2, 3, 4};

    raddoppiaTutti(valori, 4);

    for (int v : valori) {
        cout << v << " ";       // 2 4 6 8 -> l'originale è cambiato
    }
    cout << endl;

    return 0;
}
```

Nota il secondo parametro: **la dimensione va passata a parte**. Dentro la funzione l'array perde l'informazione su quanti elementi contiene, e non esiste modo di recuperarla.

> Nota: se la funzione deve solo leggere l'array senza modificarlo, dichiara il parametro `const int numeri[]`. Il compilatore bloccherà qualsiasi modifica accidentale.

## Array Bidimensionali

Un array può avere due dimensioni, come una tabella con righe e colonne.

```cpp
tipo nome[righe][colonne];
```

```cpp
int matrice[3][4];              // 3 righe, 4 colonne: 12 elementi

int tabella[2][3] = {
    {1, 2, 3},                  // Riga 0
    {4, 5, 6}                   // Riga 1
};
```

L'accesso richiede due indici: prima la riga, poi la colonna.

```cpp
cout << tabella[0][2];          // 3  -> riga 0, colonna 2
tabella[1][0] = 99;             // Modifica riga 1, colonna 0
```

Per scorrerlo tutto servono due cicli annidati: quello esterno per le righe, quello interno per le colonne.

```cpp
#include <iostream>
using namespace std;

int main() {
    const int RIGHE = 3;
    const int COLONNE = 4;

    int matrice[RIGHE][COLONNE] = {
        {1,  2,  3,  4},
        {5,  6,  7,  8},
        {9, 10, 11, 12}
    };

    for (int r = 0; r < RIGHE; r++) {
        for (int c = 0; c < COLONNE; c++) {
            cout << matrice[r][c] << "\t";
        }
        cout << endl;           // Fine riga: vado a capo
    }

    return 0;
}
```

**Output:**
```
1	2	3	4
5	6	7	8
9	10	11	12
```

Il `cout << endl;` sta nel ciclo **esterno**: viene eseguito una volta per riga, dopo aver stampato tutte le sue colonne.

## Esempio Completo: Statistiche dei Voti

```cpp
#include <iostream>
using namespace std;

const int NUMERO_VOTI = 5;

// Prototipi
void leggiVoti(int voti[], int dimensione);
double calcolaMedia(const int voti[], int dimensione);
int trovaMassimo(const int voti[], int dimensione);
int trovaMinimo(const int voti[], int dimensione);

int main() {
    int voti[NUMERO_VOTI];

    leggiVoti(voti, NUMERO_VOTI);

    cout << "Media:   " << calcolaMedia(voti, NUMERO_VOTI) << endl;
    cout << "Massimo: " << trovaMassimo(voti, NUMERO_VOTI) << endl;
    cout << "Minimo:  " << trovaMinimo(voti, NUMERO_VOTI) << endl;

    return 0;
}

void leggiVoti(int voti[], int dimensione) {
    for (int i = 0; i < dimensione; i++) {
        cout << "Voto " << i + 1 << ": ";
        cin >> voti[i];
    }
}

double calcolaMedia(const int voti[], int dimensione) {
    int somma = 0;

    for (int i = 0; i < dimensione; i++) {
        somma += voti[i];
    }

    return static_cast<double>(somma) / dimensione;
}

int trovaMassimo(const int voti[], int dimensione) {
    int massimo = voti[0];

    for (int i = 1; i < dimensione; i++) {
        if (voti[i] > massimo) {
            massimo = voti[i];
        }
    }

    return massimo;
}

int trovaMinimo(const int voti[], int dimensione) {
    int minimo = voti[0];

    for (int i = 1; i < dimensione; i++) {
        if (voti[i] < minimo) {
            minimo = voti[i];
        }
    }

    return minimo;
}
```

**Esecuzione:**
```
Voto 1: 28
Voto 2: 30
Voto 3: 24
Voto 4: 27
Voto 5: 30
Media:   27.8
Massimo: 30
Minimo:  24
```

## Limiti degli Array

Gli array classici sono veloci e semplici, ma hanno tre limiti concreti:

- **La dimensione è fissa.** Decisa alla scrittura del codice, non cambia mentre il programma gira.
- **Non conoscono la propria dimensione.** Vanno sempre accompagnati da un `int` che dice quanto sono lunghi.
- **Nessun controllo sugli indici.** Sbagliare indice non dà errore, dà comportamenti imprevedibili.

C++ offre `std::vector`, un array che cresce da solo e sa quanto è lungo. Per capire come funziona servono però concetti che non abbiamo ancora visto, quindi lo incontreremo più avanti.

---

⬅️ [Precedente: Funzioni](10-funzioni.md) | [📚 Indice](.github/README.md) | [Successivo: Stringhe](12-stringhe.md) ➡️
