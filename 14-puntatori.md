# Puntatori in C++

Un **puntatore** è una variabile che contiene l'indirizzo di un'altra variabile. Invece del valore, conserva il posto in cui quel valore si trova.

È l'argomento con la fama peggiore del C++, e in parte se la merita: è il primo punto in cui devi pensare a **dove** stanno i dati, non solo a **quali** sono. Ma il meccanismo di base è fatto di due soli simboli.

## La Memoria e gli Indirizzi

La memoria del computer è una lunga fila di caselle numerate. Ogni casella tiene un byte, e ogni casella ha un **indirizzo**: un numero che dice dove si trova.

Quando scrivi `int numero = 42;` succedono tre cose: il programma riserva 4 byte (la dimensione di un `int`, come hai visto con [`sizeof`](3-variabili.md)), ci scrive dentro `42`, e chiama quella zona `numero`.

```
indirizzo:   1000   1004   1008   1012
            +------+------+------+------+
memoria:    |  42  |      |      |      |
            +------+------+------+------+
               ^
               |
            numero
```

Il nome `numero` esiste solo per te: il programma compilato lavora con l'indirizzo.

## L'Operatore `&`: Ottenere un Indirizzo

La `&` davanti a una variabile, **in un'espressione**, restituisce il suo indirizzo.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 42;

    cout << numero << endl;     // 42        -> il valore
    cout << &numero << endl;    // 0x7ffd... -> l'indirizzo

    return 0;
}
```

L'indirizzo viene stampato in esadecimale, la notazione che hai visto in [3-variabili.md](3-variabili.md): è la forma standard per gli indirizzi perché è compatta.

> Nota: l'indirizzo cambia a ogni esecuzione del programma, e sul tuo computer sarà diverso dal mio. Non ha nessun senso memorizzarlo o confrontarlo tra esecuzioni diverse: quello che conta è la relazione tra le variabili, non il numero preciso.

> [!WARNING]
> Attenzione a non confondere i due usi della `&`, già visti in [13-riferimenti.md](13-riferimenti.md):
> - `int& r = x;` — in una **dichiarazione**, dopo il tipo: crea un riferimento
> - `&x` — in un'**espressione**, davanti a una variabile: restituisce l'indirizzo
>
> Stesso simbolo, due significati che non c'entrano niente l'uno con l'altro.

## Dichiarare un Puntatore

Un puntatore si dichiara mettendo un asterisco tra il tipo e il nome:

```cpp
tipo* nome_puntatore;
```

Il tipo indica **cosa c'è all'indirizzo**, non cosa è il puntatore: `int*` si legge "puntatore a `int`".

```cpp
int numero = 42;
int* p = &numero;       // p contiene l'indirizzo di numero
```

```
            +------+                   +------+
    p       | 1000 |  ---------->      |  42  |   numero
            +------+                   +------+
         (indirizzo 2000)           (indirizzo 1000)
```

`p` è una variabile normale, con un suo indirizzo e un suo valore. Solo che il suo valore è l'indirizzo di qualcos'altro.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 42;
    int* p = &numero;

    cout << numero << endl;     // 42        -> il valore di numero
    cout << &numero << endl;    // 0x7ffd... -> dove sta numero
    cout << p << endl;          // 0x7ffd... -> lo stesso indirizzo

    return 0;
}
```

Il tipo deve corrispondere: un `int*` può contenere solo l'indirizzo di un `int`.

```cpp
double prezzo = 9.99;
int* p = &prezzo;       // ERRORE: int* non può puntare a un double
double* q = &prezzo;    // Corretto
```

## L'Operatore `*`: Accedere al Valore Puntato

L'asterisco davanti a un puntatore, **in un'espressione**, dice "vai all'indirizzo che contieni e dammi quello che c'è lì". Si chiama **dereferenziazione**.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 42;
    int* p = &numero;

    cout << p << endl;      // 0x7ffd... -> l'indirizzo
    cout << *p << endl;     // 42        -> il valore all'indirizzo

    *p = 99;                // scrivo attraverso il puntatore

    cout << numero << endl; // 99 -> ho modificato numero

    return 0;
}
```

Anche l'asterisco ha due significati a seconda della posizione, esattamente come la `&`:

| Dove appare                         | Cosa significa                | Esempio        |
| ----------------------------------- | ----------------------------- | -------------- |
| In una **dichiarazione**, dopo il tipo | "questo è un puntatore"    | `int* p;`      |
| In un'**espressione**, davanti a un puntatore | "vai a vedere lì"   | `*p = 99;`     |

I quattro modi di scrivere, tutti equivalenti e tutti presenti nel codice vero:

```cpp
int* p;     // stile C++: l'asterisco sta col tipo
int *p;     // stile C: l'asterisco sta col nome
int * p;
int*p;
```

> [!WARNING]
> Con più variabili sulla stessa riga, l'asterisco vale **solo per la prima**:
> ```cpp
> int* a, b;      // a è un puntatore, b è un normale int!
> int *a, *b;     // entrambi puntatori
> ```
> È il motivo per cui molti preferiscono dichiarare un puntatore per riga.

## Il Puntatore Nullo: `nullptr`

Un puntatore appena dichiarato senza valore contiene spazzatura, come qualsiasi altra variabile non inizializzata. Dereferenziarlo significa andare a leggere un indirizzo a caso.

```cpp
int* p;         // Contiene un indirizzo casuale
cout << *p;     // PERICOLO: il programma può crashare o stampare qualsiasi cosa
```

Quando un puntatore non deve puntare a niente, si usa `nullptr`: il valore che significa esplicitamente "nessun indirizzo".

```cpp
int* p = nullptr;       // Dichiaratamente vuoto

if (p != nullptr) {
    cout << *p << endl;     // Entra qui solo se p punta davvero a qualcosa
} else {
    cout << "Puntatore vuoto" << endl;
}
```

**Controlla sempre un puntatore prima di dereferenziarlo**, se non sei certo che sia valido. Dereferenziare `nullptr` fa crashare il programma — cosa che, per quanto sembri brutta, è molto meglio di leggere silenziosamente memoria sbagliata.

> Nota: nel codice più vecchio troverai `NULL` o `0` al posto di `nullptr`. Funzionano, ma `nullptr` (da C++11) è più sicuro perché è davvero un puntatore e non un numero mascherato. Nel codice nuovo usa sempre `nullptr`.

## Puntatori o Riferimenti?

Fanno cose simili, ma non sono intercambiabili.

| Aspetto                            | Riferimento (`int&`)      | Puntatore (`int*`)         |
| ---------------------------------- | ------------------------- | -------------------------- |
| Va inizializzato subito             | Sì, obbligatorio          | No                         |
| Può essere vuoto                    | No                        | Sì, `nullptr`              |
| Può cambiare bersaglio              | No                        | Sì                         |
| Serve un simbolo per leggere il valore | No, si usa come una variabile | Sì, `*p`              |
| Aritmetica (spostarsi in memoria)   | No                        | Sì                         |
| Sintassi                            | Più pulita                | Più esplicita              |

**La regola pratica:** usa un riferimento quando puoi, un puntatore quando devi. Ti serve un puntatore quando la cosa puntata può legittimamente non esistere (`nullptr`), quando deve cambiare nel tempo, o quando lavori con la memoria dinamica.

```cpp
void conRiferimento(int& n) { n = 99; }
void conPuntatore(int* p)   { *p = 99; }

int main() {
    int x = 1;
    int y = 1;

    conRiferimento(x);      // si chiama come una funzione normale
    conPuntatore(&y);       // devi passare l'indirizzo esplicitamente

    return 0;
}
```

Alla chiamata si vede la differenza principale: `conPuntatore(&y)` **dichiara** sul posto che quella variabile può essere modificata.

## Puntatori e Array

Qui i due argomenti si incontrano, e si capisce perché in [11-array.md](11-array.md) un array passato a una funzione non viene copiato.

**Il nome di un array è l'indirizzo del suo primo elemento.**

```cpp
#include <iostream>
using namespace std;

int main() {
    int numeri[5] = {10, 20, 30, 40, 50};

    cout << numeri << endl;         // 0x7ffd... -> indirizzo del primo elemento
    cout << &numeri[0] << endl;     // lo stesso indirizzo

    int* p = numeri;                // nessuna & : il nome è già un indirizzo

    cout << *p << endl;             // 10 -> primo elemento

    return 0;
}
```

Quando passi un array a una funzione, quello che viaggia è questo indirizzo: quattro o otto byte, non l'intero array. Ecco perché la funzione lavora sull'originale e perché la dimensione va passata a parte — l'indirizzo da solo non dice quanti elementi seguono.

### Aritmetica dei Puntatori

Sommare `1` a un puntatore non aggiunge un byte: lo sposta **all'elemento successivo**, qualunque sia la sua dimensione. Il compilatore sa che `p` è un `int*` e salta 4 byte per volta.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numeri[5] = {10, 20, 30, 40, 50};
    int* p = numeri;

    cout << *p << endl;         // 10 -> elemento 0
    cout << *(p + 1) << endl;   // 20 -> elemento 1
    cout << *(p + 3) << endl;   // 40 -> elemento 3

    return 0;
}
```

Questo spiega la notazione con le parentesi quadre: `numeri[i]` è esattamente un altro modo di scrivere `*(numeri + i)`. Le due forme sono la stessa cosa, e la prima esiste solo perché è più leggibile.

```cpp
cout << numeri[2] << endl;      // 30
cout << *(numeri + 2) << endl;  // 30, identico
```

> [!WARNING]
> L'aritmetica dei puntatori non ha nessun controllo sui limiti, esattamente come gli indici degli array. `*(p + 100)` su un array da 5 legge memoria che non ti appartiene, senza il minimo avviso.

## Memoria Dinamica: `new` e `delete`

Tutte le variabili viste finora hanno una durata decisa dal compilatore: nascono quando l'esecuzione entra nel loro blocco e muoiono quando ne esce. Per questo un array vuole una dimensione nota in anticipo.

Con `new` puoi invece chiedere memoria **mentre il programma gira**, e decidere tu quando restituirla.

```cpp
int* p = new int;       // Chiedo spazio per un int
*p = 42;                // Lo uso attraverso il puntatore

cout << *p << endl;     // 42

delete p;               // Restituisco la memoria
p = nullptr;            // Buona abitudine: il puntatore non punta più a niente di valido
```

Quella memoria non ha un nome: l'unico modo per raggiungerla è il puntatore. Se perdi il puntatore, perdi la memoria.

### Array Dinamici

È l'uso più concreto: finalmente un array la cui dimensione la decide l'utente.

```cpp
#include <iostream>
using namespace std;

int main() {
    int quantita;

    cout << "Quanti numeri? ";
    cin >> quantita;

    int* numeri = new int[quantita];        // dimensione decisa ora, non alla compilazione

    for (int i = 0; i < quantita; i++) {
        cout << "Numero " << i + 1 << ": ";
        cin >> numeri[i];                   // si usa come un array normale
    }

    int somma = 0;
    for (int i = 0; i < quantita; i++) {
        somma += numeri[i];
    }

    cout << "Somma: " << somma << endl;

    delete[] numeri;                        // parentesi quadre: era un array
    numeri = nullptr;

    return 0;
}
```

**Esecuzione:**
```
Quanti numeri? 3
Numero 1: 10
Numero 2: 20
Numero 3: 5
Somma: 35
```

> [!WARNING]
> `new` va con `delete`, `new[]` va con `delete[]`. Scambiarli è un errore che il compilatore non segnala e che produce comportamenti imprevedibili.

### Memory Leak

Se chiedi memoria e non la restituisci mai, quella memoria resta occupata fino alla fine del programma. Si chiama **memory leak**, perdita di memoria.

```cpp
void perdita() {
    int* p = new int[1000];
    // ...uso p...
}                               // la funzione finisce, p sparisce,
                                // ma i 1000 int restano occupati per sempre
```

Su un programma che chiude subito non si nota. Su un programma che gira per ore e ripete quella funzione mille volte, la memoria si esaurisce.

**Ogni `new` deve avere il suo `delete`.**

### Puntatori Penzolanti

Il problema opposto: usare un puntatore **dopo** aver liberato la memoria.

```cpp
int* p = new int(42);
delete p;               // la memoria è restituita

cout << *p << endl;     // PERICOLO: p punta a memoria che non è più tua
```

Un puntatore in questo stato si chiama **dangling pointer** (puntatore penzolante). Il programma spesso non crasha subito: legge quello che nel frattempo è finito lì, e sbaglia molto più avanti. Mettere `p = nullptr;` subito dopo il `delete` trasforma un bug silenzioso in un crash immediato, che è molto più facile da trovare.

## `const` e Puntatori

`const` può riferirsi a due cose diverse, a seconda di dove lo metti:

```cpp
int a = 1;
int b = 2;

const int* p = &a;      // Non puoi modificare il VALORE puntato
// *p = 99;             // ERRORE
p = &b;                 // ma puoi spostare il puntatore

int* const q = &a;      // Non puoi spostare il PUNTATORE
*q = 99;                // ma puoi modificare il valore
// q = &b;              // ERRORE
```

Si legge da destra verso sinistra: `int* const q` è "q è un `const` puntatore a `int`", `const int* p` è "p è un puntatore a `int` costante".

La prima forma, `const int*`, è di gran lunga la più usata: è il modo di dire "ti passo l'indirizzo, ma non toccare".

## Errori Frequenti

| Errore | Conseguenza |
| ------ | ----------- |
| Dereferenziare un puntatore non inizializzato | Comportamento imprevedibile, spesso crash |
| Dereferenziare `nullptr` | Crash immediato del programma |
| Dimenticare `delete` | Memory leak |
| Usare un puntatore dopo `delete` | Dati corrotti, crash ritardato |
| `delete` due volte sullo stesso puntatore | Comportamento imprevedibile |
| `int* a, b;` credendo che `b` sia un puntatore | `b` è un normale `int` |
| Confondere `p` con `*p` | Stampi un indirizzo invece del valore, o viceversa |

## Esempio Completo: Array Dinamico con Funzioni

```cpp
#include <iostream>
using namespace std;

// Prototipi
void riempi(int* numeri, int dimensione);
double calcolaMedia(const int* numeri, int dimensione);
int trovaMassimo(const int* numeri, int dimensione);

int main() {
    int quantita;

    cout << "Quanti voti vuoi inserire? ";
    cin >> quantita;

    if (quantita <= 0) {
        cout << "Quantita non valida" << endl;
        return 1;
    }

    int* voti = new int[quantita];      // memoria chiesta a runtime

    riempi(voti, quantita);

    cout << "Media:   " << calcolaMedia(voti, quantita) << endl;
    cout << "Massimo: " << trovaMassimo(voti, quantita) << endl;

    delete[] voti;                      // memoria restituita
    voti = nullptr;

    return 0;
}

void riempi(int* numeri, int dimensione) {
    for (int i = 0; i < dimensione; i++) {
        cout << "Voto " << i + 1 << ": ";
        cin >> numeri[i];
    }
}

// const int* : la funzione legge l'array ma non lo modifica
double calcolaMedia(const int* numeri, int dimensione) {
    int somma = 0;

    for (int i = 0; i < dimensione; i++) {
        somma += numeri[i];
    }

    return static_cast<double>(somma) / dimensione;
}

int trovaMassimo(const int* numeri, int dimensione) {
    int massimo = numeri[0];

    for (int i = 1; i < dimensione; i++) {
        if (numeri[i] > massimo) {
            massimo = numeri[i];
        }
    }

    return massimo;
}
```

**Esecuzione:**
```
Quanti voti vuoi inserire? 4
Voto 1: 28
Voto 2: 30
Voto 3: 25
Voto 4: 27
Media:   27.5
Massimo: 30
```

Nota che `int numeri[]` e `int* numeri` come parametri di funzione sono la stessa identica cosa: la prima forma è solo un modo più leggibile di dire "qui arriva un array".

## Riepilogo dei Simboli

| Scrittura     | Dove          | Significato                          |
| ------------- | ------------- | ------------------------------------ |
| `int* p;`     | dichiarazione | `p` è un puntatore a `int`            |
| `&x`          | espressione   | l'indirizzo di `x`                    |
| `*p`          | espressione   | il valore all'indirizzo contenuto in `p` |
| `nullptr`     | valore        | puntatore che non punta a niente      |
| `new int`     | espressione   | chiede memoria per un `int`           |
| `delete p`    | istruzione    | restituisce la memoria                |

## Cosa Viene Dopo

Gestire `new` e `delete` a mano è faticoso e facile da sbagliare: basta un `return` anticipato o un errore a metà funzione per saltare il `delete`. Il C++ moderno risolve il problema in due modi, che incontrerai più avanti:

- I **contenitori** come `std::vector`, che gestiscono da soli la memoria di cui hanno bisogno.
- Gli **smart pointer** (`unique_ptr`, `shared_ptr`), puntatori che chiamano `delete` automaticamente quando non servono più.

Nel codice C++ di oggi `new` e `delete` scritti a mano sono rari. Vanno comunque capiti: sono il meccanismo su cui tutto il resto è costruito, e li incontrerai in qualsiasi codice esistente.

---

⬅️ [Precedente: Riferimenti](13-riferimenti.md) | [📚 Indice](.github/README.md) | [Successivo: Vector](15-vector.md) ➡️
