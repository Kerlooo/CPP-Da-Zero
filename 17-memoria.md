# Stack, heap e memoria

In [14-puntatori.md](14-puntatori.md) hai visto che ogni variabile ha un **indirizzo**, cioè un posto preciso nella memoria. Ma non tutte le variabili finiscono nello stesso posto. Una variabile locale, una variabile globale e un `int` chiesto con `new` vivono in **zone diverse** della memoria, con regole diverse su quando nascono e quando muoiono.

Capire queste zone serve a tre cose molto concrete:

- sapere **quanto vive** una variabile, e quindi quando è ancora lecito usarla;
- capire **da dove vengono** gli errori più temuti: memory leak, puntatori penzolanti, stack overflow;
- rispondere alla classica domanda d'esame: "dove sta questa variabile, nello stack o nello heap?".

## Le Zone di Memoria di un Programma

Quando avvii un programma, il sistema operativo gli assegna un pezzo di memoria e lo divide in quattro zone, ognuna con un compito preciso.

```
indirizzi alti
+------------------------------+
|           STACK              |  variabili locali e parametri
|             |                |  cresce verso il basso
|             v                |
|                              |
|        (spazio libero)       |
|                              |
|             ^                |
|             |                |  cresce verso l'alto
|           HEAP               |  memoria chiesta con new
+------------------------------+
|  DATI STATICI (data / bss)   |  variabili globali e static
+------------------------------+
|       CODICE (text)          |  le istruzioni del programma
+------------------------------+
indirizzi bassi
```

| Zona | Cosa contiene | Chi la gestisce | Quanto dura |
| ---- | ------------- | --------------- | ----------- |
| **Codice** (*text*) | Le istruzioni del programma compilato | Il sistema operativo, che la carica all'avvio | Tutto il programma |
| **Dati statici** (*data* / *bss*) | Variabili globali e variabili `static` | Il compilatore, che ne decide la dimensione in anticipo | Tutto il programma |
| **Stack** | Variabili locali e parametri delle funzioni | Automatica: il programma la riempie e la svuota da solo | Finché la funzione (o il blocco) è in esecuzione |
| **Heap** | Memoria chiesta con `new` | **Tu**: la chiedi con `new` e la restituisci con `delete` | Da `new` fino a `delete` |

Due parole sui nomi:

- **text** è il nome tecnico della zona del codice. Di solito è in sola lettura: il programma non può modificare le proprie istruzioni.
- **data** e **bss** sono due parti della zona dei dati statici. In *data* vanno le variabili globali che hanno un valore iniziale (`int x = 5;`), in *bss* quelle senza valore o a zero (`int y;`), che all'avvio vengono riempite di zeri.

> Nota: lo schema qui sopra è la disposizione classica dei sistemi più comuni (Linux, Windows, macOS su processori Intel/AMD e ARM). Lo standard del C++ non parla di "stack" e "heap" come zone fisiche: parla di **durata** delle variabili (automatica, statica, dinamica). Le zone sono il modo in cui i compilatori e i sistemi operativi realizzano in pratica quelle regole. Dove stanno esattamente, e in che direzione crescono, dipende dal sistema.

Nel resto del capitolo le vediamo una per una, partendo da quella che usi da sempre senza saperlo: lo stack.

## Lo Stack

Lo **stack** (in italiano "pila") è la zona dove finiscono le **variabili locali**, cioè quelle dichiarate dentro una funzione, e i **parametri** delle funzioni.

Il nome non è un caso. In [16-pila.md](16-pila.md) hai visto che una pila segue la regola **LIFO**: l'ultimo elemento entrato è il primo a uscire. Le chiamate di funzione seguono esattamente questa regola: se `main` chiama `f` e `f` chiama `g`, la prima a finire è `g`, poi `f`, poi `main`.

### Lo Stack Frame

Ogni volta che una funzione viene chiamata, il programma mette in cima allo stack un blocco di memoria tutto suo, chiamato **stack frame** (o *record di attivazione*). Dentro ci sono:

- i **parametri** della funzione;
- le sue **variabili locali**;
- l'**indirizzo di ritorno**: il punto del codice da cui riprendere quando la funzione finisce.

Quando la funzione termina, il suo frame viene tolto dalla cima: è un `pop`. Tutte le sue variabili locali smettono di esistere in quel momento.

```cpp
#include <iostream>
using namespace std;

int quadrato(int x) {
    int risultato = x * x;          // locale di quadrato
    return risultato;
}

int sommaQuadrati(int a, int b) {
    int qa = quadrato(a);           // prima chiamata a quadrato
    int qb = quadrato(b);           // seconda chiamata a quadrato
    return qa + qb;
}

int main() {
    int totale = sommaQuadrati(3, 4);
    cout << "Totale: " << totale << endl;
    return 0;
}
```

**Output:**
```
Totale: 25
```

Ecco come appare lo stack nel momento in cui il programma sta eseguendo `quadrato(3)`:

```
            +---------------------------+
  cima ->   | quadrato                  |
            |   x = 3                   |
            |   risultato = 9           |
            +---------------------------+
            | sommaQuadrati             |
            |   a = 3, b = 4            |
            |   qa = ?, qb = ?          |   (non ancora calcolate)
            +---------------------------+
            | main                      |
            |   totale = ?              |
            +---------------------------+
```

E questa è la sequenza completa, con lo stack descritto dal basso verso la cima:

| Momento | Stack (dal basso alla cima) |
| ------- | --------------------------- |
| Parte `main` | `main` |
| `main` chiama `sommaQuadrati(3, 4)` | `main`, `sommaQuadrati` |
| `sommaQuadrati` chiama `quadrato(3)` | `main`, `sommaQuadrati`, `quadrato` |
| `quadrato(3)` restituisce 9 | `main`, `sommaQuadrati` |
| `sommaQuadrati` chiama `quadrato(4)` | `main`, `sommaQuadrati`, `quadrato` |
| `quadrato(4)` restituisce 16 | `main`, `sommaQuadrati` |
| `sommaQuadrati` restituisce 25 | `main` |
| `main` finisce | *vuoto* |

Nota che `quadrato` viene chiamata due volte, e ogni volta ha un frame **nuovo**: la `x` e il `risultato` della seconda chiamata non hanno niente a che fare con quelli della prima. È per questo che, come hai visto in [10-funzioni.md](10-funzioni.md), le variabili locali "esistono solo lì".

> Nota: i frame riusano la stessa memoria. Quando un frame viene tolto, i byte restano dove sono, con i vecchi valori dentro, e il frame successivo ci finisce sopra. Ecco da dove viene la "spazzatura" in una variabile locale non inizializzata: sono gli avanzi di qualche frame precedente.

> Nota: sui processori comuni lo stack cresce verso gli indirizzi **più bassi**: il frame in cima ha un indirizzo minore di quello sotto. Nei disegni lo mettiamo in alto perché è più intuitivo. Inoltre, con le ottimizzazioni attive, il compilatore può tenere alcune variabili nei **registri** del processore (piccolissime memorie interne alla CPU) invece che nello stack.

### Durata Automatica

Le variabili dello stack hanno **durata automatica**: nascono quando l'esecuzione arriva alla loro dichiarazione e muoiono quando esce dal blocco `{ }` in cui sono dichiarate. Non devi fare niente: ci pensa il programma.

È comodissimo, ed è anche il motivo per cui lo stack è **velocissimo**: creare un frame significa solo spostare un segnaposto che indica la cima, niente di più.

### Lo Stack è Piccolo: lo Stack Overflow

Lo stack ha una dimensione **fissa e limitata**, decisa all'avvio del programma. Se lo riempi, il programma va in **stack overflow** (traboccamento dello stack) e si ferma bruscamente.

I due modi classici per arrivarci:

**1. Ricorsione infinita.** Una funzione **ricorsiva** è una funzione che chiama se stessa. Ogni chiamata aggiunge un frame; se le chiamate non si fermano mai, i frame si accumulano finché lo stack finisce.

```cpp
// DA NON FARE: frammento di esempio
void infinita(int n) {
    infinita(n + 1);        // si richiama sempre, nessuna condizione per fermarsi
}
```

In un caso così evidente il compilatore se ne accorge: le versioni recenti di `g++` con `-Wall` stampano `warning: infinite recursion detected`. Nei casi meno evidenti (una condizione di uscita che esiste ma non si avvera mai) nessuno ti avvisa. Se esegui comunque il programma, su Linux vedi:

```
Segmentation fault (core dumped)
```

**2. Array locale enorme.** Un array dichiarato dentro una funzione sta nello stack, tutto intero.

```cpp
// DA NON FARE: frammento di esempio
int main() {
    int enorme[10000000];   // 10 milioni di int = circa 40 MB nello stack
    enorme[0] = 1;
    // ...
}
```

40 MB sono molto più di quanto lo stack possa contenere: il programma si ferma appena parte. La soluzione è mettere i dati nello heap, con `new[]` o, meglio, con un `vector` (li vediamo più avanti in questo capitolo).

> Nota: la dimensione dello stack dipende dal sistema e non è fissata dallo standard. Valori tipici: circa **8 MB** su Linux e macOS, **1 MB** su Windows. Un array locale da 1 milione di `int` (4 MB) funziona su Linux ma manda in stack overflow lo stesso programma su Windows. Anche il messaggio cambia: su Windows il programma spesso si chiude senza scrivere niente.

### Mai Restituire l'Indirizzo di una Variabile Locale

Ecco la conseguenza più importante della durata automatica. Guarda questa funzione:

```cpp
// DA NON FARE: frammento di esempio
int* creaNumero() {
    int x = 42;         // x vive nel frame di creaNumero
    return &x;          // restituisco l'indirizzo di x...
}                       // ...ma qui il frame sparisce, e x con lui
```

Quando `creaNumero` finisce, il suo frame viene tolto dallo stack. Il puntatore restituito indica una zona dove **prima** c'era `x` e dove, alla prossima chiamata di funzione, ci sarà qualcos'altro. È un **dangling pointer**, un puntatore penzolante, lo stesso problema visto in [14-puntatori.md](14-puntatori.md) dopo un `delete`.

Usarlo è **comportamento indefinito**: lo standard non garantisce niente. Può sembrare funzionare, può stampare numeri a caso, può far crashare il programma.

Per fortuna `g++` se ne accorge e ti avvisa:

```
warning: address of local variable 'x' returned [-Wreturn-local-addr]
```

Lo stesso vale per i **riferimenti** (visti in [13-riferimenti.md](13-riferimenti.md)):

```cpp
// DA NON FARE: frammento di esempio
int& creaRiferimento() {
    int x = 42;
    return x;           // warning: reference to local variable 'x' returned
}
```

**Come si fa bene?** Dipende da cosa ti serve:

| Soluzione | Esempio | Quando usarla |
| --------- | ------- | ------------- |
| Restituire **per valore** | `int creaNumero() { int x = 42; return x; }` | Quasi sempre: il valore viene copiato fuori prima che il frame sparisca |
| Restituire un `vector` o una `string` | `vector<int> crea() { ... return v; }` | Quando servono molti dati |
| Chiedere memoria nello heap con `new` | `int* p = new int(42); return p;` | Quando ti serve proprio un puntatore (lo vediamo tra poco) |

> [!WARNING]
> Prendi sul serio questo warning. Un programma che restituisce l'indirizzo di una locale può funzionare per caso cento volte e sbagliare la centunesima.

## Variabili Globali e `static`

Non tutto deve sparire alla fine di una funzione. Alcune variabili devono vivere **per tutta la durata del programma**: queste finiscono nella zona dei **dati statici**.

### Variabili Globali

Una variabile **globale** è dichiarata fuori da tutte le funzioni. L'hai già incontrata in [11-array.md](11-array.md) con la costante `NUMERO_VOTI`. È visibile da tutte le funzioni scritte sotto di lei, nasce prima che parta `main` e muore quando il programma finisce.

```cpp
#include <iostream>
using namespace std;

int contatore;          // globale senza valore: parte da 0, garantito

void incrementa() {
    contatore++;        // tutte le funzioni vedono la stessa variabile
}

int main() {
    incrementa();
    incrementa();
    incrementa();

    cout << "Contatore: " << contatore << endl;

    return 0;
}
```

**Output:**
```
Contatore: 3
```

Nota la differenza con le locali: una variabile globale **senza valore iniziale vale sempre 0**. Lo garantisce lo standard: è la zona *bss* che viene riempita di zeri all'avvio. Una variabile locale senza valore, invece, contiene spazzatura.

> [!WARNING]
> Le costanti globali (`const int NUMERO_VOTI = 5;`) vanno benissimo. Le variabili globali **modificabili**, invece, vanno usate il meno possibile: se qualunque funzione può cambiarle, quando il valore è sbagliato è difficilissimo capire chi l'ha cambiato. Passare i dati come parametri è quasi sempre meglio.

### Variabili Locali `static`

A volte vuoi una variabile che si ricorda il suo valore tra una chiamata e l'altra, ma che sia visibile **solo** dentro la funzione. È quello che fa la parola chiave `static` davanti a una variabile locale.

- È visibile solo dentro la funzione, come una locale normale.
- Vive nella zona dei dati statici, come una globale: **non** sta nel frame, quindi non sparisce quando la funzione finisce.
- Viene inizializzata **una volta sola**, la prima volta che l'esecuzione passa dalla sua dichiarazione.

```cpp
#include <iostream>
using namespace std;

void contaNormale() {
    int chiamate = 0;           // rinasce a ogni chiamata, nel nuovo frame
    chiamate++;
    cout << "Normale: " << chiamate << endl;
}

void contaStatic() {
    static int chiamate = 0;    // inizializzata solo la prima volta
    chiamate++;                 // poi conserva il valore tra le chiamate
    cout << "Static:  " << chiamate << endl;
}

int main() {
    for (int i = 0; i < 3; i++) {
        contaNormale();
        contaStatic();
    }

    return 0;
}
```

**Output:**
```
Normale: 1
Static:  1
Normale: 1
Static:  2
Normale: 1
Static:  3
```

La versione normale riparte ogni volta da 0, perché la variabile vive nel frame e il frame viene distrutto. La versione `static` continua a contare, perché vive fuori dallo stack.

> Nota: la riga `static int chiamate = 0;` **non** rimette a zero la variabile a ogni chiamata, anche se a prima vista sembra. È uno degli errori di lettura più comuni all'esame.

## Lo Heap: la Memoria Dinamica

Lo **heap** è la zona della **memoria dinamica**: quella che chiedi con `new` e restituisci con `delete`. Le basi le hai viste in [14-puntatori.md](14-puntatori.md#memoria-dinamica-new-e-delete): qui guardiamo cosa succede in memoria.

> Nota: "heap" in inglese vuol dire "mucchio". Non ha niente a che fare con la struttura dati chiamata anch'essa *heap*, che non trattiamo: è solo un nome uguale.

### Il Puntatore Sta nello Stack, il Dato nello Heap

Questa è l'idea chiave. Guarda questa funzione:

```cpp
void esempio() {
    int* p = new int(5);
    // ...
}
```

Qui ci sono **due** cose in memoria, in due zone diverse:

```
          STACK                              HEAP
     +----------------+                +-----------+
  p  | 0x55a1c2e3f2b0 |  ----------->  |     5     |
     +----------------+                +-----------+
     variabile locale:                 senza nome:
     sparisce a fine funzione          resta finché non fai delete
```

- `p` è una variabile locale come tutte le altre: sta nel frame di `esempio` e sparisce quando la funzione finisce.
- L'`int` che vale `5` sta nello heap, **non ha nome** e resta lì finché qualcuno non chiama `delete`.

Se la funzione finisce senza `delete`, `p` sparisce ma il blocco nello heap no. Nessuno conosce più il suo indirizzo, quindi nessuno potrà mai restituirlo. Ecco cos'è davvero un **memory leak**: memoria dello heap rimasta occupata ma diventata irraggiungibile.

### `new` con Inizializzazione

Con `new` puoi dare subito un valore a quello che crei:

| Scrittura | Cosa crea nello heap |
| --------- | -------------------- |
| `new int` | Un `int` **non inizializzato** (spazzatura) |
| `new int()` oppure `new int{}` | Un `int` che vale `0` |
| `new int(5)` oppure `new int{5}` | Un `int` che vale `5` |
| `new int[n]` | `n` interi **non inizializzati** |
| `new int[n]{}` | `n` interi tutti a `0` |
| `new int[3]{4, 8, 15}` | 3 interi: `4`, `8`, `15` |

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 5;

    int* singolo = new int(42);         // un int che vale 42
    int* zeri = new int[n]{};           // 5 int, tutti a 0

    cout << "Singolo: " << *singolo << endl;

    cout << "Array: ";
    for (int i = 0; i < n; i++) {
        cout << zeri[i] << " ";
    }
    cout << endl;

    delete singolo;                     // new    -> delete
    delete[] zeri;                      // new[]  -> delete[]

    return 0;
}
```

**Output:**
```
Singolo: 42
Array: 0 0 0 0 0
```

> [!WARNING]
> Attenzione alla differenza tra tonde e quadre:
> ```cpp
> int* a = new int(5);    // UN int che vale 5
> int* b = new int[5];    // CINQUE int non inizializzati
> ```
> Scambiarle è un errore classico, e il compilatore non può accorgersene: entrambe danno un `int*`.

### Un Altro Modo di Perdere Memoria

Il leak non succede solo quando una funzione finisce. Basta **sovrascrivere** l'unico puntatore che conosce un blocco:

```cpp
int* p = new int(1);    // blocco A nello heap
p = new int(2);         // p ora punta al blocco B: l'indirizzo di A è perso
delete p;               // libera B, ma A resta occupato per sempre
```

```
prima:   p ----> [ 1 ]  A

dopo:    p ----> [ 2 ]  B
                 [ 1 ]  A   <- nessuno lo conosce più: leak
```

La regola: prima di riassegnare un puntatore che possiede memoria dello heap, fai `delete`.

### Puntatori Penzolanti e Doppio `delete`

Dopo un `delete`, il blocco torna disponibile, ma il puntatore **contiene ancora il vecchio indirizzo**. `delete` non lo cambia.

```cpp
// DA NON FARE: frammento di esempio
int* p = new int(42);
int* q = p;             // q e p puntano allo stesso blocco

delete p;               // il blocco viene restituito

cout << *q << endl;     // ERRORE: q penzola, il blocco non è più tuo
delete q;               // ERRORE: doppio delete dello stesso blocco
```

Il **doppio delete** (*double delete* o *double free*) è restituire due volte lo stesso blocco. È comportamento indefinito: spesso il programma si ferma con un messaggio come `free(): double free detected`, ma può anche corrompere lo heap e crashare molto più avanti.

Nota che qui il problema c'è anche se metti `p = nullptr` dopo il `delete`: `q` contiene ancora il vecchio indirizzo. Quando più puntatori indicano lo stesso blocco, devi decidere **uno solo** che ha il compito di liberarlo.

### `delete` su `nullptr` è Sicuro

Lo standard garantisce che `delete` su un puntatore nullo **non fa niente**. Per questo l'abitudine vista in [14-puntatori.md](14-puntatori.md) di mettere il puntatore a `nullptr` dopo il `delete` protegge anche dal doppio delete, quando il puntatore è uno solo:

```cpp
int* p = new int(42);

delete p;
p = nullptr;

delete p;       // nessun effetto: p è nullptr
```

Allo stesso modo non serve scrivere `if (p != nullptr) delete p;`: il controllo lo fa già `delete`.

### Funzioni che Restituiscono Memoria Dinamica

Ecco la versione **corretta** della funzione che restituiva l'indirizzo di una locale: la memoria viene chiesta nello heap, quindi sopravvive alla fine della funzione.

```cpp
#include <iostream>
using namespace std;

// Crea un array di n elementi: 10, 20, 30, ...
// ATTENZIONE: chi chiama deve liberarlo con delete[]
int* creaArray(int n) {
    int* a = new int[n];        // a è locale, il blocco sta nello heap

    for (int i = 0; i < n; i++) {
        a[i] = (i + 1) * 10;
    }

    return a;                   // a sparisce, ma il suo valore (l'indirizzo) viene copiato fuori
}

int main() {
    int n = 4;
    int* numeri = creaArray(n); // ora è main che possiede il blocco

    for (int i = 0; i < n; i++) {
        cout << numeri[i] << " ";
    }
    cout << endl;

    delete[] numeri;            // il delete lo fa main
    numeri = nullptr;

    return 0;
}
```

**Output:**
```
10 20 30 40
```

Funziona, ma pone una domanda che il codice da solo non risponde: **chi deve fare il `delete[]`?** La funzione ha chiesto la memoria, ma non può liberarla, altrimenti restituirebbe un puntatore penzolante. Quindi il compito passa a chi chiama, e l'unico modo per saperlo è leggere il commento. Se chi chiama se ne dimentica, è un leak.

Questo si chiama problema della **proprietà** (*ownership*) della memoria: chi la possiede, la deve liberare. Con `new` e `delete` scritti a mano, la proprietà esiste solo nella testa del programmatore. Ricordalo: è il motivo per cui, più avanti, vedrai che `vector` è quasi sempre la scelta migliore.

### Matrici Dinamiche

Un esercizio classico d'esame: creare una matrice con righe e colonne decise mentre il programma gira, **senza** `vector`.

Serve un tipo nuovo: `int**`, un **puntatore a puntatore**. Si legge come al solito: è un puntatore che contiene l'indirizzo di un `int*`.

L'idea è costruire la matrice in due passi:

1. un array di `righe` puntatori, uno per riga (`new int*[righe]`);
2. per ogni riga, un array di `colonne` interi (`new int[colonne]`).

```
  STACK                 HEAP
+--------+          +--------+       +---+---+---+---+
| matrice| -------> | riga 0 | ----> | 0 | 0 | 0 | 0 |
+--------+          +--------+       +---+---+---+---+
                    | riga 1 | ----> | 0 | 0 | 0 | 0 |
                    +--------+       +---+---+---+---+
                    | riga 2 | ----> | 0 | 0 | 0 | 0 |
                    +--------+       +---+---+---+---+
                    array di int*     un array di int per riga
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int righe = 3;
    int colonne = 4;

    // 1. Array di puntatori: uno per ogni riga
    int** matrice = new int*[righe];

    // 2. Ogni riga è un array di int, tutti a 0
    for (int r = 0; r < righe; r++) {
        matrice[r] = new int[colonne]{};
    }

    // Si usa come una matrice normale
    for (int r = 0; r < righe; r++) {
        for (int c = 0; c < colonne; c++) {
            matrice[r][c] = r * colonne + c + 1;
        }
    }

    for (int r = 0; r < righe; r++) {
        for (int c = 0; c < colonne; c++) {
            cout << matrice[r][c] << "\t";
        }
        cout << endl;
    }

    // Liberazione: in ordine INVERSO rispetto alla creazione
    for (int r = 0; r < righe; r++) {
        delete[] matrice[r];        // prima ogni riga
    }
    delete[] matrice;               // poi l'array di puntatori
    matrice = nullptr;

    return 0;
}
```

**Output:**
```
1	2	3	4
5	6	7	8
9	10	11	12
```

`matrice[r][c]` funziona in due salti: `matrice[r]` prende il puntatore della riga `r`, e `[c]` prende l'elemento `c` di quella riga.

> [!WARNING]
> L'ordine del `delete` conta. Se fai prima `delete[] matrice`, perdi i puntatori alle righe e non puoi più liberarle: tutte le righe diventano un leak (e leggere `matrice[r]` dopo il `delete` è già un errore). Regola: **ogni `new` ha il suo `delete`**, e si libera dall'interno verso l'esterno.

> Nota: le righe di una matrice così **non** sono contigue in memoria, a differenza di un array bidimensionale `int m[3][4]` visto in [11-array.md](11-array.md), dove i 12 elementi stanno tutti uno dopo l'altro. Ogni riga è un blocco separato, in un punto qualsiasi dello heap.

### Se `new` Fallisce

Lo heap è grande, ma non infinito. Se chiedi più memoria di quella disponibile, `new` **non** restituisce `nullptr`: lancia un'**eccezione** chiamata `std::bad_alloc`. L'eccezione l'hai già incontrata con `at()` in [15-vector.md](15-vector.md): se nessuno la gestisce, il programma si ferma con un messaggio come:

```
terminate called after throwing an instance of 'std::bad_alloc'
```

> Nota: in molti libri e vecchi programmi trovi, dopo ogni `new`, un controllo `if (p == nullptr)`. Con il `new` normale del C++ standard quel controllo è inutile: se `new` torna, il puntatore è valido. Il controllo ha senso solo con la forma speciale `new (nothrow)`, che non trattiamo.

## Stack o Heap?

| Caratteristica | Stack | Heap |
| -------------- | ----- | ---- |
| Cosa ci va | Variabili locali, parametri | Memoria chiesta con `new` |
| Chi alloca e libera | Automatico | Tu, con `new` e `delete` |
| Quanto dura | Fino alla fine del blocco `{ }` | Da `new` a `delete` |
| Dimensione | Piccola (pochi MB) | Grande (gran parte della RAM disponibile) |
| Velocità | Molto veloce | Più lento: bisogna cercare un blocco libero |
| Dimensione dei dati | Deve essere nota alla compilazione | Può essere decisa mentre il programma gira |
| Errori tipici | Stack overflow, indirizzo di una locale restituito | Memory leak, dangling pointer, doppio delete |

**Quando usare cosa:**

- **Stack**, cioè variabili locali normali: è la scelta predefinita. Usalo per tutto ciò che è piccolo e serve solo dentro una funzione.
- **Heap**: quando i dati sono **tanti**, quando la loro quantità si scopre **solo a runtime** (mentre il programma gira), o quando devono **sopravvivere** alla funzione che li crea. E nel codice moderno, quasi sempre attraverso un `vector`.

## Vedere le Zone con gli Indirizzi

Puoi controllare tu stesso che le variabili stanno in zone diverse: basta stampare i loro indirizzi con `&`, come in [14-puntatori.md](14-puntatori.md).

```cpp
#include <iostream>
using namespace std;

int globale = 1;                        // dati statici

int main() {
    static int statica = 2;             // dati statici anche lei
    int locale = 3;                     // stack
    int* dinamico = new int(4);         // dinamico nello stack, l'int nello heap

    cout << "Globale:            " << &globale << endl;
    cout << "Static locale:      " << &statica << endl;
    cout << "Locale:             " << &locale << endl;
    cout << "Puntatore:          " << &dinamico << endl;
    cout << "Dato nello heap:    " << dinamico << endl;

    delete dinamico;
    dinamico = nullptr;

    return 0;
}
```

**Output** (un esempio su Linux a 64 bit):
```
Globale:            0x5603d8a3b010
Static locale:      0x5603d8a3b014
Locale:             0x7ffd4c2e9a44
Puntatore:          0x7ffd4c2e9a48
Dato nello heap:    0x5603d9f2a2b0
```

Leggi i numeri a gruppi:

- `globale` e `statica` sono **vicinissime** (`...010` e `...014`): stessa zona, quella dei dati statici, anche se una è dichiarata fuori da `main` e l'altra dentro.
- `locale` e `dinamico` (il puntatore) iniziano con `0x7ffd...`: sono nello **stack**, molto lontano dal resto.
- Il valore di `dinamico`, cioè l'indirizzo del dato, inizia con `0x5603d9...`: è nello **heap**, poco sopra i dati statici, come nello schema all'inizio del capitolo.

Nota la differenza tra le ultime due righe: `&dinamico` è **dove sta il puntatore** (stack), `dinamico` è **dove punta** (heap).

> Nota: gli indirizzi cambiano **a ogni esecuzione**. È voluto: i sistemi operativi moderni usano l'**ASLR** (*Address Space Layout Randomization*), che sposta le zone in posizioni casuali per rendere più difficili alcuni attacchi informatici. Su Windows o macOS i numeri, e anche il formato, saranno diversi. Quello che resta vero è la relazione: variabili della stessa zona hanno indirizzi vicini, zone diverse hanno indirizzi lontani.

### Gli Array Sono Contigui

Gli elementi di un array stanno **uno dopo l'altro** in memoria, senza buchi. L'indirizzo di ogni elemento è quello del precedente più `sizeof` del tipo (la dimensione in byte, vista in [3-variabili.md](3-variabili.md)).

```cpp
#include <iostream>
using namespace std;

int main() {
    int numeri[4] = {10, 20, 30, 40};

    cout << "sizeof(int): " << sizeof(int) << endl;

    for (int i = 0; i < 4; i++) {
        cout << "&numeri[" << i << "] = " << &numeri[i] << endl;
    }

    return 0;
}
```

**Output** (un esempio):
```
sizeof(int): 4
&numeri[0] = 0x7ffc8a1b2c30
&numeri[1] = 0x7ffc8a1b2c34
&numeri[2] = 0x7ffc8a1b2c38
&numeri[3] = 0x7ffc8a1b2c3c
```

Gli indirizzi crescono di 4 alla volta (in esadecimale, dopo `...38` viene `...3c`). È proprio quello che sfrutta l'aritmetica dei puntatori: `numeri + 1` salta all'indirizzo successivo di `sizeof(int)` byte.

> Nota: lo standard garantisce che gli elementi di un array siano contigui. Non garantisce invece che `int` occupi 4 byte: è il valore di quasi tutti i sistemi di oggi, ma va verificato con `sizeof`.

> [!WARNING]
> Con gli array di `char` c'è una trappola. `cout` tratta un `char*` come **testo** da stampare, non come indirizzo:
> ```cpp
> char parola[] = "ciao";
> cout << parola << endl;                       // stampa: ciao
> cout << &parola[0] << endl;                   // stampa ancora: ciao
> cout << static_cast<void*>(parola) << endl;   // stampa l'indirizzo
> ```
> Per vedere l'indirizzo bisogna convertirlo in `void*`, un "puntatore generico" che non dice a che tipo punta: `cout` allora non ha motivo di trattarlo come testo e stampa il numero.

## `vector` e `string`: lo Heap Senza Pensieri

Ora puoi capire davvero cosa fa un `vector`. Un oggetto `vector` è composto da due parti:

- un **piccolo oggetto** fisso, che sta dove lo dichiari (nello stack, se è una variabile locale). Contiene, in sostanza, un puntatore e i numeri che servono a sapere quanti elementi ci sono;
- gli **elementi veri e propri**, che stanno in un blocco dello **heap**, chiesto con `new` dal vector stesso.

```
       STACK                              HEAP
  +---------------------+          +----+----+----+
v | puntatore ----------+--------> | 10 | 20 | 30 |
  | numero di elementi  |          +----+----+----+
  | spazio disponibile  |
  +---------------------+
```

Si vede con `sizeof`: l'oggetto ha sempre la stessa dimensione, che contenga 3 elementi o un milione.

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> piccolo = {10, 20, 30};
    vector<int> grande(1000000);            // un milione di int: circa 4 MB

    cout << "sizeof(piccolo): " << sizeof(piccolo) << endl;
    cout << "sizeof(grande):  " << sizeof(grande) << endl;

    cout << "Oggetto (stack): " << &piccolo << endl;
    cout << "Dati (heap):     " << &piccolo[0] << endl;

    return 0;
}                                           // qui i vector liberano da soli il loro heap
```

**Output** (un esempio su Linux a 64 bit):
```
sizeof(piccolo): 24
sizeof(grande):  24
Oggetto (stack): 0x7ffe3b1c9a10
Dati (heap):     0x55c0e41a32b0
```

Ricordi l'array locale da 4 MB che su Windows mandava in stack overflow? Il `vector` da un milione di elementi non ha questo problema: nello stack ci sono solo 24 byte, i 4 MB stanno nello heap.

> Nota: il valore 24 è quello tipico di `g++` e Visual Studio a 64 bit, ma lo standard non lo fissa: su un altro sistema può essere diverso. Quello che non cambia è che non dipende dal numero di elementi.

La parte migliore è l'ultima riga del programma: quando un `vector` smette di esistere (alla `}` del suo blocco), **libera da solo** la sua memoria nello heap. Niente `delete`, niente leak, nessun dubbio su chi debba liberare: il proprietario è il vector.

Questa tecnica ha un nome che sentirai spesso: **RAII** (*Resource Acquisition Is Initialization*). L'idea, senza troppa teoria: si lega una risorsa (qui la memoria dello heap) a un oggetto che sta nello stack. Quando l'oggetto muore, e nello stack muore sempre in automatico, la risorsa viene restituita.

Anche `string` funziona così: l'oggetto sta nello stack, i caratteri nello heap.

> Nota: le stringhe molto corte fanno eccezione. Quasi tutte le librerie tengono i testi brevi (con `g++` fino a 15 caratteri) direttamente **dentro** l'oggetto, senza usare lo heap: è un'ottimizzazione chiamata *small string optimization*. Per te non cambia niente, ma spiega perché stampando gli indirizzi a volte i caratteri risultano nello stack.

Ecco perché nel C++ moderno `new` e `delete` scritti a mano sono rari:

- per gli **array** dinamici si usa `vector` (anche per le matrici: `vector<vector<int>>`, visto in [15-vector.md](15-vector.md));
- per il **testo** si usa `string`;
- per un **singolo oggetto** nello heap esistono gli **smart pointer** (`unique_ptr`, `shared_ptr`), che applicano la stessa idea RAII a un puntatore. Questa guida non li tratta.

`new` e `delete` restano comunque da conoscere: sono il meccanismo che sta sotto a tutto questo, e all'esame vengono chiesti.

## Errori Frequenti

| Errore | Esempio | Cosa succede | Come evitarlo |
| ------ | ------- | ------------ | ------------- |
| Memory leak | `new` senza `delete`, oppure `p = new int;` su un `p` che possedeva già memoria | Memoria dello heap occupata e irraggiungibile | Ogni `new` ha il suo `delete`; meglio ancora, usa `vector` |
| Dangling pointer | `*p` dopo `delete p;` | Comportamento indefinito: valori a caso o crash | `p = nullptr;` subito dopo `delete` |
| Doppio delete | `delete p; delete p;` oppure `delete` su due copie dello stesso puntatore | Comportamento indefinito, spesso crash | Un solo proprietario per blocco; `nullptr` dopo `delete` |
| `delete` invece di `delete[]` | `int* a = new int[10]; delete a;` | Comportamento indefinito | `new` con `delete`, `new[]` con `delete[]` |
| `delete` su memoria non da `new` | `int x; delete &x;` | Comportamento indefinito, di solito crash | `delete` solo su indirizzi restituiti da `new` |
| Stack overflow | Ricorsione infinita, array locale enorme | Il programma si ferma di colpo | Condizione di uscita nella ricorsione; dati grandi nello heap o in un `vector` |
| Restituire l'indirizzo di una locale | `int* f() { int x; return &x; }` | Dangling pointer: `g++` dà un warning | Restituisci per valore, oppure un `vector` |
| `new int(5)` confuso con `new int[5]` | `int* a = new int(5); a[3] = 1;` | Si scrive fuori dall'unico `int` allocato | Tonde = valore, quadre = quanti elementi |
| Liberare una matrice nell'ordine sbagliato | `delete[] matrice;` prima delle righe | Le righe diventano leak | Prima le righe, poi l'array di puntatori |

## Esempio Completo: Voti di una Classe

Un programma che chiede quanti studenti e quanti esami ci sono, legge i voti in una **matrice dinamica** e stampa la media di ogni studente. Creazione e liberazione della matrice stanno in due funzioni separate, così la regola "chi crea, libera" è scritta nel codice.

```cpp
#include <iostream>
using namespace std;

// Prototipi
int** creaMatrice(int righe, int colonne);
void liberaMatrice(int** matrice, int righe);
double mediaRiga(const int* riga, int colonne);

int main() {
    int studenti;
    int esami;

    cout << "Quanti studenti? ";
    cin >> studenti;
    cout << "Quanti esami? ";
    cin >> esami;

    if (studenti <= 0 || esami <= 0) {
        cout << "Valori non validi" << endl;
        return 1;
    }

    // La matrice sta nello heap; voti (il puntatore) sta nello stack di main
    int** voti = creaMatrice(studenti, esami);

    for (int s = 0; s < studenti; s++) {
        cout << "Studente " << s + 1 << endl;
        for (int e = 0; e < esami; e++) {
            cout << "  Esame " << e + 1 << ": ";
            cin >> voti[s][e];
        }
    }

    cout << endl << "Medie:" << endl;
    for (int s = 0; s < studenti; s++) {
        // voti[s] è la riga dello studente s: un int* che passa a mediaRiga
        cout << "Studente " << s + 1 << ": " << mediaRiga(voti[s], esami) << endl;
    }

    liberaMatrice(voti, studenti);  // ogni new di creaMatrice ha il suo delete
    voti = nullptr;                 // il puntatore non indica più niente di valido

    return 0;
}

// Crea una matrice righe x colonne nello heap, tutta a 0.
// Chi la riceve deve liberarla con liberaMatrice.
int** creaMatrice(int righe, int colonne) {
    int** matrice = new int*[righe];        // array di puntatori alle righe

    for (int r = 0; r < righe; r++) {
        matrice[r] = new int[colonne]{};    // una riga di int a 0
    }

    return matrice;                         // l'indirizzo esce, la memoria resta nello heap
}

// Libera dall'interno verso l'esterno: prima le righe, poi l'array di puntatori
void liberaMatrice(int** matrice, int righe) {
    for (int r = 0; r < righe; r++) {
        delete[] matrice[r];
    }
    delete[] matrice;
}

// const int* : legge la riga senza modificarla
double mediaRiga(const int* riga, int colonne) {
    int somma = 0;

    for (int c = 0; c < colonne; c++) {
        somma += riga[c];
    }

    return static_cast<double>(somma) / colonne;
}
```

**Esecuzione:**
```
Quanti studenti? 2
Quanti esami? 3
Studente 1
  Esame 1: 28
  Esame 2: 30
  Esame 3: 25
Studente 2
  Esame 1: 24
  Esame 2: 27
  Esame 3: 30

Medie:
Studente 1: 27.6667
Studente 2: 27
```

Mentre il programma legge i voti, la memoria è divisa così:

| Cosa | Dove | Perché |
| ---- | ---- | ------ |
| `studenti`, `esami`, `s`, `e` | Stack (frame di `main`) | Variabili locali |
| `voti` (il puntatore `int**`) | Stack (frame di `main`) | Variabile locale |
| L'array dei puntatori alle righe | Heap | Creato con `new int*[righe]` |
| Le righe con i voti | Heap | Create con `new int[colonne]{}` |
| `riga`, `somma`, `c` di `mediaRiga` | Stack (frame di `mediaRiga`) | Nascono e muoiono a ogni chiamata |
| Il codice di tutte le funzioni | Codice (*text*) | Istruzioni del programma |

Con `vector<vector<int>> voti(studenti, vector<int>(esami));` lo stesso programma non avrebbe bisogno né di `creaMatrice` né di `liberaMatrice`: la memoria nello heap verrebbe chiesta e restituita in automatico. Scriverlo con `new` e `delete` serve a vedere cosa succede sotto, ed è esattamente quello che fa il vector al posto tuo.


---

⬅️ [Precedente: Coda (Queue)](16-coda.md) | [📚 Indice](.github/README.md)
