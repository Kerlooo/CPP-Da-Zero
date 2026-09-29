# Vector in C++

Alla fine di [11-array.md](11-array.md) abbiamo elencato i tre limiti degli array classici: dimensione fissa, nessuna conoscenza della propria lunghezza, nessun controllo sugli indici. Lo `std::vector` li risolve tutti e tre.

Un **vector** è un array che:

- **cresce e si restringe** mentre il programma gira;
- **sa quanti elementi contiene**;
- offre un modo **controllato** di accedere agli elementi.

Dietro le quinte usa proprio la memoria dinamica vista in [14-puntatori.md](14-puntatori.md): chiede spazio con `new` quando serve e lo restituisce da solo quando il vector non esiste più. Tu non devi scrivere né `new` né `delete`.

## Includere la Libreria

Il vector sta in una libreria a parte:

```cpp
#include <vector>
```

Senza questa riga il compilatore non sa cosa sia un `vector`.

## Dichiarazione e Inizializzazione

```cpp
vector<tipo> nome;
```

Il tipo degli elementi va tra **parentesi angolari** `< >`. Come per gli array, tutti gli elementi hanno lo stesso tipo.

| Scrittura                        | Risultato                                  |
| -------------------------------- | ------------------------------------------ |
| `vector<int> v;`                 | Vuoto, 0 elementi                           |
| `vector<int> v = {4, 8, 15};`    | 3 elementi: `4`, `8`, `15`                  |
| `vector<int> v(5);`              | 5 elementi, tutti `0`                       |
| `vector<int> v(5, 7);`           | 5 elementi, tutti `7`                       |
| `vector<string> nomi(3);`        | 3 stringhe vuote                            |

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vuoto;                  // nessun elemento
    vector<int> primi = {2, 3, 5, 7};   // elencati tra graffe
    vector<double> prezzi(3);           // 0, 0, 0
    vector<char> lettere(4, 'x');       // 'x', 'x', 'x', 'x'

    cout << vuoto.size() << endl;       // 0
    cout << primi.size() << endl;       // 4
    cout << prezzi.size() << endl;      // 3
    cout << lettere.size() << endl;     // 4

    return 0;
}
```

> [!WARNING]
> Parentesi tonde e graffe **non** sono la stessa cosa:
> ```cpp
> vector<int> a(5);       // 5 elementi, tutti 0
> vector<int> b{5};       // 1 elemento, che vale 5
> ```
> Tonde = "quanti elementi". Graffe = "questi sono gli elementi".

A differenza degli array, un vector **non contiene mai valori casuali**: gli elementi creati senza un valore esplicito partono da zero (o da stringa vuota).

## Dimensione: `size` ed `empty`

Il vector conosce la propria lunghezza. Niente più `int dimensione` da portarsi dietro.

| Metodo      | Cosa restituisce                         |
| ----------- | ---------------------------------------- |
| `v.size()`  | Il numero di elementi                     |
| `v.empty()` | `true` se il vector non ha elementi       |

Sono gli stessi nomi che hai visto per le stringhe in [12-stringhe.md](12-stringhe.md).

```cpp
vector<int> numeri = {10, 20, 30};

cout << numeri.size() << endl;      // 3

if (numeri.empty()) {
    cout << "Nessun numero" << endl;
}
```

## Accedere agli Elementi

Due modi, con una differenza importante:

| Scrittura  | Controlla l'indice? | Se l'indice è sbagliato                      |
| ---------- | ------------------- | -------------------------------------------- |
| `v[i]`     | No                  | Comportamento imprevedibile, come negli array |
| `v.at(i)`  | Sì                  | Il programma si ferma con un messaggio d'errore |

```cpp
vector<int> voti = {28, 30, 24};

cout << voti[0] << endl;        // 28
cout << voti.at(2) << endl;     // 24

voti[1] = 29;                   // modifica il secondo elemento
voti.at(2)++;                   // incrementa il terzo
```

Gli indici partono da `0` e arrivano a `size() - 1`, esattamente come negli array.

```cpp
vector<int> voti = {28, 30, 24};

cout << voti[10];       // Nessun controllo: stampa spazzatura (o peggio)
cout << voti.at(10);    // Il programma si ferma e dice che l'indice è fuori dai limiti
```

Con `at` un errore di indice diventa **visibile subito**, invece di nascondersi e saltare fuori molto più avanti.

> Nota: il messaggio stampato da `at` è qualcosa come `terminate called after throwing an instance of 'std::out_of_range'`. È un'**eccezione**: un meccanismo per segnalare errori che si può anche intercettare e gestire. Per ora basta sapere che ferma il programma.

### Primo e Ultimo Elemento

| Metodo      | Equivale a            |
| ----------- | --------------------- |
| `v.front()` | `v[0]`                |
| `v.back()`  | `v[v.size() - 1]`     |

```cpp
vector<int> numeri = {4, 8, 15, 16};

cout << numeri.front() << endl;     // 4
cout << numeri.back() << endl;      // 16
```

> [!WARNING]
> `front()` e `back()` su un vector **vuoto** non hanno senso: non c'è nessun elemento da restituire. Il risultato è imprevedibile. Controlla prima con `empty()`.

## Aggiungere e Togliere Elementi

È qui che il vector fa quello che un array non può fare.

| Metodo              | Cosa fa                                    |
| ------------------- | ------------------------------------------ |
| `v.push_back(x)`    | Aggiunge `x` **in fondo**                   |
| `v.pop_back()`      | Toglie l'**ultimo** elemento                |
| `v.clear()`         | Toglie **tutti** gli elementi               |

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> numeri;             // vuoto

    numeri.push_back(10);           // {10}
    numeri.push_back(20);           // {10, 20}
    numeri.push_back(30);           // {10, 20, 30}

    cout << "Elementi: " << numeri.size() << endl;      // 3

    numeri.pop_back();              // {10, 20}

    cout << "Elementi: " << numeri.size() << endl;      // 2
    cout << "Ultimo: " << numeri.back() << endl;        // 20

    numeri.clear();                 // {}

    cout << "Vuoto? " << numeri.empty() << endl;        // 1 (true)

    return 0;
}
```

**Output:**
```
Elementi: 3
Elementi: 2
Ultimo: 20
Vuoto? 1
```

> Nota: `pop_back()` **non restituisce** l'elemento tolto, lo butta e basta. Se ti serve il valore, leggilo prima con `back()`.

### Inserire e Cancellare in Mezzo

Per lavorare in una posizione qualsiasi si usano `insert` ed `erase`. La posizione si indica con `v.begin() + indice`:

```cpp
vector<int> numeri = {10, 20, 30, 40};

numeri.insert(numeri.begin() + 1, 15);  // {10, 15, 20, 30, 40}
numeri.erase(numeri.begin() + 3);       // {10, 15, 20, 40}
numeri.erase(numeri.begin());           // {15, 20, 40}
```

Per adesso considera `v.begin() + i` come una formula da ricordare: significa "la posizione dell'elemento di indice `i`". `begin()` restituisce un **iteratore**, un oggetto simile a un puntatore che indica una posizione dentro il contenitore.

> Nota: `insert` ed `erase` in mezzo sono **lenti** su vector grandi: per fare spazio (o chiudere il buco) devono spostare di un posto tutti gli elementi successivi. `push_back` e `pop_back` lavorano in fondo e non spostano niente, per questo sono le operazioni preferite.

## Scorrere un Vector

### Con il `for` Classico

```cpp
vector<int> voti = {28, 30, 24, 27};

for (size_t i = 0; i < voti.size(); i++) {
    cout << "Voto " << i + 1 << ": " << voti[i] << endl;
}
```

L'indice è di tipo `size_t` (visto in [12-stringhe.md](12-stringhe.md)) perché `size()` restituisce proprio un `size_t`, un intero senza segno.

> Nota: se scrivi `int i`, compilando con `-Wall` ricevi un avviso tipo `comparison of integer expressions of different signedness`. Il programma funziona lo stesso, ma confrontare un intero con segno e uno senza segno può dare risultati strani con i numeri negativi. Usa `size_t` e l'avviso sparisce.

### Con il `for` Range-Based

Quando l'indice non serve, è la forma più semplice:

```cpp
vector<string> nomi = {"Anna", "Luca", "Sara"};

for (const string& nome : nomi) {       // solo lettura, nessuna copia
    cout << nome << endl;
}
```

Per **modificare** gli elementi serve il riferimento, come spiegato in [13-riferimenti.md](13-riferimenti.md):

```cpp
vector<int> prezzi = {10, 20, 30};

for (int& p : prezzi) {
    p = p * 2;          // modifica davvero il vector
}
// prezzi ora vale {20, 40, 60}
```

| Forma                          | Quando usarla                            |
| ------------------------------ | ---------------------------------------- |
| `for (int x : v)`              | Leggere elementi piccoli (`int`, `double`) |
| `for (const string& x : v)`    | Leggere elementi grossi senza copiarli    |
| `for (int& x : v)`             | Modificare gli elementi                   |
| `for (size_t i = 0; ...)`      | Serve la posizione dell'elemento          |

## Vector e Funzioni

Qui c'è una differenza importante rispetto agli array.

Un array passato a una funzione **non viene copiato**: la funzione riceve l'indirizzo del primo elemento. Un vector, invece, si comporta come una normale variabile: passato **per valore** viene **copiato tutto**.

```cpp
void raddoppia(vector<int> v) {     // v è una COPIA
    for (int& x : v) {
        x = x * 2;
    }
}   // la copia viene distrutta qui: l'originale non è cambiato
```

Si applica la regola pratica di [13-riferimenti.md](13-riferimenti.md):

| Cosa deve fare la funzione  | Firma                         |
| --------------------------- | ----------------------------- |
| Solo leggere il vector      | `const vector<int>& v`        |
| Modificare il vector        | `vector<int>& v`              |

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Solo lettura: niente copia, niente modifiche
void stampa(const vector<int>& v) {
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;
}

// Modifica: lavora sull'originale
void raddoppia(vector<int>& v) {
    for (int& x : v) {
        x = x * 2;
    }
}

int main() {
    vector<int> numeri = {1, 2, 3};

    stampa(numeri);         // 1 2 3
    raddoppia(numeri);
    stampa(numeri);         // 2 4 6

    return 0;
}
```

**Output:**
```
1 2 3
2 4 6
```

Nota che non serve più passare la dimensione come secondo parametro: la funzione la chiede al vector con `size()`.

### Restituire un Vector

Una funzione può anche **creare e restituire** un vector, cosa impossibile con gli array:

```cpp
vector<int> primiN(int n) {
    vector<int> risultato;

    for (int i = 1; i <= n; i++) {
        risultato.push_back(i);
    }

    return risultato;
}

int main() {
    vector<int> numeri = primiN(5);     // {1, 2, 3, 4, 5}
    return 0;
}
```

> Nota: restituire un vector **non** costa una copia completa. Il compilatore sposta il contenuto direttamente nella variabile che lo riceve, senza duplicare gli elementi.

## Copiare e Confrontare

Due cose che con gli array non si potevano fare con un semplice operatore:

```cpp
vector<int> a = {1, 2, 3};
vector<int> b = a;          // copia completa: b è indipendente da a

b[0] = 99;                  // a resta {1, 2, 3}

if (a == b) {               // confronta elemento per elemento
    cout << "Uguali" << endl;
} else {
    cout << "Diversi" << endl;      // stampa questo
}
```

## Vector Bidimensionali

Una matrice è un **vector di vector**: ogni elemento del vector esterno è una riga.

```cpp
vector<vector<int>> matrice(righe, vector<int>(colonne, 0));
```

La riga si legge così: "`righe` elementi, ognuno dei quali è un `vector<int>` di `colonne` zeri".

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int righe = 3;
    int colonne = 4;

    vector<vector<int>> tabella(righe, vector<int>(colonne, 0));

    // Riempie con i numeri da 1 a 12
    int valore = 1;
    for (int r = 0; r < righe; r++) {
        for (int c = 0; c < colonne; c++) {
            tabella[r][c] = valore;
            valore++;
        }
    }

    // Stampa riga per riga
    for (const vector<int>& riga : tabella) {
        for (int x : riga) {
            cout << x << "\t";
        }
        cout << endl;
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

A differenza degli array bidimensionali, qui `righe` e `colonne` possono essere **variabili lette da tastiera**.

> Nota: `tabella.size()` è il numero di righe, `tabella[0].size()` il numero di colonne della prima riga. Ogni riga è un vector indipendente, quindi in teoria le righe potrebbero avere lunghezze diverse.

## Errori Frequenti

| Errore | Cosa succede | Come evitarlo |
| ------ | ------------ | ------------- |
| `v[0] = 5;` su un vector vuoto | Scrive in memoria che non esiste | Usa `push_back`, oppure crea il vector con la dimensione giusta: `vector<int> v(10);` |
| `pop_back()`, `back()`, `front()` su un vector vuoto | Comportamento imprevedibile | Controlla prima `if (!v.empty())` |
| Passare il vector per valore | Copia inutile, e le modifiche vanno perse | `const vector<int>&` per leggere, `vector<int>&` per modificare |
| `vector<int> v(5)` al posto di `{5}` (o viceversa) | 5 zeri invece di un 5 | Tonde = quanti, graffe = quali |
| Dimenticare `#include <vector>` | Errore di compilazione: `'vector' was not declared` | Aggiungi l'include in cima al file |

## Esempio Completo: Voti senza Sapere Quanti Sono

Con un array bisognava decidere in anticipo quanti voti leggere. Con un vector no: si continua finché l'utente non scrive `0`.

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Prototipi
vector<int> leggiVoti();
double calcolaMedia(const vector<int>& voti);
int trovaMassimo(const vector<int>& voti);
int contaEccellenti(const vector<int>& voti);

int main() {
    vector<int> voti = leggiVoti();

    if (voti.empty()) {
        cout << "Nessun voto inserito" << endl;
        return 0;
    }

    cout << "Voti inseriti: " << voti.size() << endl;
    cout << "Media:         " << calcolaMedia(voti) << endl;
    cout << "Massimo:       " << trovaMassimo(voti) << endl;
    cout << "Da 27 in su:   " << contaEccellenti(voti) << endl;

    return 0;
}

vector<int> leggiVoti() {
    vector<int> voti;
    int voto;

    cout << "Inserisci i voti (0 per finire):" << endl;
    cin >> voto;

    while (voto != 0) {
        if (voto >= 18 && voto <= 30) {
            voti.push_back(voto);
        } else {
            cout << "Voto non valido, ignorato" << endl;
        }
        cin >> voto;
    }

    return voti;
}

double calcolaMedia(const vector<int>& voti) {
    int somma = 0;

    for (int v : voti) {
        somma += v;
    }

    return static_cast<double>(somma) / voti.size();
}

int trovaMassimo(const vector<int>& voti) {
    int massimo = voti[0];

    for (int v : voti) {
        if (v > massimo) {
            massimo = v;
        }
    }

    return massimo;
}

int contaEccellenti(const vector<int>& voti) {
    int conteggio = 0;

    for (int v : voti) {
        if (v >= 27) {
            conteggio++;
        }
    }

    return conteggio;
}
```

**Esecuzione:**
```
Inserisci i voti (0 per finire):
28
30
35
Voto non valido, ignorato
21
26
0
Voti inseriti: 4
Media:         26.25
Massimo:       30
Da 27 in su:   2
```

Confrontalo con l'esempio finale di [11-array.md](11-array.md): niente costante `NUMERO_VOTI`, niente dimensione passata a ogni funzione, e il numero di voti lo decide chi usa il programma.

## Array o Vector?

| Caratteristica              | Array `int a[5]`         | Vector `vector<int> v`       |
| --------------------------- | ------------------------ | ---------------------------- |
| Dimensione                  | Fissa, decisa nel codice  | Cambia mentre il programma gira |
| Conosce la sua lunghezza    | No                       | Sì, con `size()`             |
| Controllo degli indici      | Mai                      | Con `at()`                   |
| Passato a una funzione      | Mai copiato              | Copiato, se passato per valore |
| Copia con `=`               | No                       | Sì                           |
| Confronto con `==`          | No                       | Sì                           |
| Restituito da una funzione  | No                       | Sì                           |

---

⬅️ [Precedente: Puntatori](14-puntatori.md) | [📚 Indice](.github/README.md) | [Successivo: Pila (Stack)](16-pila.md) ➡️
