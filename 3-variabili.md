# Tipi di Variabili in C++

Un programma ha bisogno di ricordare dei dati mentre lavora: un'età, un prezzo, un nome. Per farlo usa le **variabili**.

Una **variabile** è uno spazio nella memoria del computer a cui dai un **nome**. Immaginala come una scatola con un'etichetta: dentro c'è un **valore**, che puoi leggere e cambiare. Ogni variabile ha anche un **tipo**, che stabilisce cosa può contenere (un numero intero, un numero con la virgola, un carattere...) e quanto spazio occupa.

Lo spazio si misura in **byte**. Un byte è formato da 8 **bit**, e un bit è la cella più piccola della memoria: può valere solo `0` o `1`.

In C++ esistono diversi tipi di variabili:
| Tipo     | Descrizione                           | Dimensione | Intervallo                     |
| -------- | ------------------------------------- | ---------- | ------------------------------ |
| `int`    | Intero normale **signed** (con segno) | 4 byte     | ~ da -2 miliardi a +2 miliardi |
| `float`  | Numero decimale, ~7 cifre precise     | 4 byte     | ~ da -3.4e38 a +3.4e38         |
| `double` | Numero decimale, ~15 cifre precise    | 8 byte     | ~ da -1.8e308 a +1.8e308       |
| `char`   | Singolo carattere (signed o unsigned) | 1 byte     | da -128 a 127 (o da 0 a 255)   |
| `string` | Stringa di caratteri alfanumerici     | Variabile  | Dipende dal contenuto          |
| `bool`   | Valore booleano                       | 1 byte     | `true` / `false`               |

Le cifre precise di `float` e `double` dicono quante cifre significative il numero riesce a conservare senza errori: oltre quella soglia le cifre vengono approssimate. `3.4e38` si legge "3.4 per 10 alla 38".

> Nota: Gli intervalli e le dimensioni possono variare in base all'architettura: lo standard fissa solo dei minimi, quelli indicati sono i valori tipici su macchine moderne. Un `bool` occupa un byte intero anche se gli basterebbe un singolo bit: è la dimensione minima indirizzabile in memoria.

> Nota: `string` non è un tipo base del linguaggio ma arriva dalla libreria standard: per usarlo scrivi `#include <string>` in cima al file. La variabile `string` in sé ha una dimensione fissa (32 byte con `g++`), ma il testo vero viene conservato altrove, in uno spazio che cresce insieme al numero di caratteri.

## Tipi di `int`

Le variabili `int` supportano dei modificatori come `signed`, `unsigned`, `short`, `long`. Questi valori modificano l'intervallo (la grandezza del numero inserito).
| Tipo                 | Descrizione                 | Dimensione   | Intervallo (tipico)            |
| -------------------- | --------------------------- | ------------ | ------------------------------ |
| `short`              | Intero corto **signed**     | 2 byte       | da -32.768 a 32.767            |
| `unsigned short`     | Intero corto **unsigned**   | 2 byte       | da 0 a 65.535                  |
| `int`                | Intero normale **signed**   | 4 byte       | ~ da -2 miliardi a +2 miliardi |
| `unsigned int`       | Intero normale **unsigned** | 4 byte       | da 0 a ~4 miliardi             |
| `long`               | Intero lungo **signed**     | 4 o 8 byte   | dipende dal sistema            |
| `unsigned long`      | Intero lungo **unsigned**   | 4 o 8 byte   | dipende dal sistema            |
| `long long`          | Intero lungo **signed**     | 8 byte       | da -9e18 a +9e18               |
| `unsigned long long` | Intero lungo **unsigned**   | 8 byte       | da 0 a 18e18                   |

Più byte occupa un tipo, più valori diversi riesce a rappresentare. Con `n` byte hai `8 × n` bit, e quindi `2^(8n)` combinazioni possibili: uno `short` (2 byte, 16 bit) arriva a 65.536 valori distinti, un `int` (4 byte, 32 bit) a poco più di 4 miliardi.

La differenza tra `signed` e `unsigned` non cambia il numero di valori, ma dove li colloca: `signed` li divide tra negativi e positivi, `unsigned` li usa tutti a partire da zero. Ecco perché `short` e `unsigned short` occupano entrambi 2 byte ma hanno intervalli diversi.

> Nota: `long` è il caso più variabile. Su Linux e macOS a 64 bit occupa 8 byte, su Windows a 64 bit ne occupa 4. Quando ti serve la certezza di avere 8 byte, usa `long long`.

## Misurare la Dimensione: `sizeof`

Non devi fidarti delle tabelle: C++ ti permette di chiedere direttamente al compilatore quanti byte occupa un tipo, con l'operatore `sizeof`.

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "char:      " << sizeof(char)      << " byte" << endl;   // 1
    cout << "bool:      " << sizeof(bool)      << " byte" << endl;   // 1
    cout << "short:     " << sizeof(short)     << " byte" << endl;   // 2
    cout << "int:       " << sizeof(int)       << " byte" << endl;   // 4
    cout << "float:     " << sizeof(float)     << " byte" << endl;   // 4
    cout << "double:    " << sizeof(double)    << " byte" << endl;   // 8
    cout << "long long: " << sizeof(long long) << " byte" << endl;   // 8

    return 0;
}
```

`sizeof` funziona sia su un tipo che su una variabile già dichiarata:

```cpp
int numero = 42;

cout << sizeof(int) << endl;      // 4 - chiedo al tipo
cout << sizeof(numero) << endl;   // 4 - chiedo alla variabile
```

Il conto avviene in fase di compilazione, non mentre il programma gira: il risultato è già deciso prima dell'esecuzione.

> Nota: eseguire questo programma sul tuo computer è il modo più affidabile per sapere quanto occupano davvero i tipi sulla **tua** macchina.

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

C++11 introduce un'altra sintassi usando le graffe `{}`. Il vantaggio è che il compilatore rifiuta le conversioni che perderebbero dati: `int x{3.5};` è un errore, mentre `int x = 3.5;` compila e salva `3` senza dire nulla.

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
#include <string>
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

    cout << "Nome: " << nome << endl;
    cout << "Eta: " << eta << endl;
    cout << "Altezza: " << altezza << endl;
    cout << "Maggiorenne: " << maggiorenne << endl;   // un bool si stampa come 1 (true) o 0 (false)
    cout << "Anni di esperienza: " << anni_esperienza << endl;
    
    return 0;
}
```

**Output:**
```
Nome: Alice
Eta: 25
Altezza: 1.75
Maggiorenne: 1
Anni di esperienza: 5
```

### Regole Importanti

- I nomi delle variabili iniziano con una **lettera o underscore** `_`
- Contengono solo **lettere senza accenti** (`a`-`z`, `A`-`Z`), **numeri e underscore**
- Non possono iniziare con un **numero**
- Non possono contenere **spazi** o **caratteri speciali**
- Non possono essere **parole riservate** del linguaggio, come `int`, `return` o `if`
- C++ distingue tra **maiuscole e minuscole** (`eta` ≠ `Eta`)
- Usa nomi **significativi** e leggibili

**Esempi di nomi validi:**
```cpp
int eta;
int contatore2;
float prezzoProdotto;
string nome_utente;
```

**Esempi di nomi NON validi:**
```cpp
int 1numero;        //  Inizia con un numero
int nome utente;    //  Contiene uno spazio
float prezzo-totale; //  Contiene un trattino
int return;         //  È una parola riservata
```

## Il Tipo `auto`: Lo Deduce il Compilatore

Finora il tipo di ogni variabile l'hai sempre scritto tu. Da C++11 esiste un'alternativa: la parola chiave **`auto`** dice al compilatore di capire da solo il tipo, guardando il valore che le assegni.

```cpp
auto numero = 42;         // il compilatore vede 42 -> numero è un int
auto prezzo = 19.99;      // vede 19.99            -> prezzo è un double
auto lettera = 'A';       // vede 'A'              -> lettera è un char
auto attivo = true;       // vede true             -> attivo è un bool
```

Queste quattro righe sono **identiche** a quelle scritte per esteso:

```cpp
int numero = 42;
double prezzo = 19.99;
char lettera = 'A';
bool attivo = true;
```

Il punto importante: `auto` **non** è un tipo "generico" o "variabile", e non rende il programma più lento. Il tipo viene deciso in fase di compilazione e poi resta fisso per sempre, esattamente come se l'avessi scritto a mano. Una volta che `numero` è un `int`, non può più diventare altro:

```cpp
auto numero = 42;
numero = 10;        // Corretto: 10 è un int
numero = "Ciao";    // ERRORE: numero è un int e tale resta
```

### L'Inizializzazione è Obbligatoria

Se non c'è un valore, il compilatore non ha niente da cui dedurre il tipo:

```cpp
auto x = 5;     // Corretto
auto y;         // ERRORE: da cosa dovrebbe capire il tipo?
```

Più avanti in questo capitolo vedrai che la stessa regola vale per le costanti `const`, per un motivo diverso: lì il valore non potrà più cambiare, qui senza valore non esiste proprio un tipo.

### La Trappola delle Stringhe

Questo è l'unico caso in cui `auto` sorprende chi inizia:

```cpp
auto nome = "Alice";      // NON è una string!
```

Il testo tra virgolette doppie non è un `std::string`: è un letterale in stile C, e `auto` deduce `const char*`. La differenza si vede appena provi a usare i metodi delle stringhe:

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    auto nomeA = "Alice";               // const char*
    string nomeB = "Alice";             // std::string

    cout << nomeA << endl;              // Alice - stamparla funziona
    cout << nomeB.length() << endl;     // 5
    // cout << nomeA.length() << endl;  // ERRORE: const char* non ha metodi

    return 0;
}
```

Per ottenere una `string` con `auto` serve il suffisso `s` (da C++14), che richiede una riga in più:

```cpp
using namespace std::string_literals;

auto nome = "Alice"s;     // ora è davvero una std::string
```

In pratica, per le stringhe conviene scrivere `string` per esteso.

### Quando Usarlo Davvero

`auto` non serve a scrivere meno: serve a **non ripetere** un tipo che è già evidente dal valore. Su tipi corti non guadagni niente, e anzi nascondi un'informazione utile a chi legge.

```cpp
auto eta = 25;        // Poco utile: 'int eta = 25;' è altrettanto corto e più chiaro
```

Il guadagno arriva quando il tipo è lungo o scomodo da scrivere, cosa che succede con gli strumenti della libreria standard che incontrerai più avanti (iteratori, contenitori), e nei cicli sugli array che vedrai nel capitolo 11.

**La regola pratica mentre impari:** scrivi i tipi per esteso. Vedere `int`, `double` e `string` nel codice aiuta a fissare la differenza tra i tipi, che è esattamente quello che stai imparando in questo capitolo. Usa `auto` quando il tipo è lungo, ovvio o entrambe le cose.

> Nota: `auto` esiste dal C++11. Con `-std=c++23` (il comando consigliato nel capitolo 0) funziona sempre.

### Conoscere il Tipo di una Variabile

Domanda naturale a questo punto: se lo decide il compilatore, io come faccio a sapere che tipo è?

Prima di tutto, **`typeof()` non esiste in C++**. La trovi in molti esempi online, ma è un'estensione del compilatore GCC: `g++` la accetta solo se compili senza `-std`, perché in quel caso attiva le estensioni GNU. Con il comando consigliato (`-std=c++23`) dà errore, e anche altri compilatori la rifiutano. Non usarla.

Gli strumenti veri sono due:

| Strumento    | Cosa fa                                                | Header        |
| ------------ | ------------------------------------------------------ | ------------- |
| `decltype(x)`| Ricava il tipo di `x` per dichiarare un'altra variabile | nessuno       |
| `typeid(x)`  | Restituisce informazioni sul tipo, leggibili a runtime  | `<typeinfo>`  |

```cpp
int numero = 42;
decltype(numero) altro = 10;    // 'altro' è un int, come numero
```

`typeid` serve invece a **stampare** il tipo, ma il risultato delude:

```cpp
#include <iostream>
#include <typeinfo>
using namespace std;

int main() {
    auto numero = 42;
    cout << typeid(numero).name() << endl;   // con g++ stampa: i

    return 0;
}
```

Quella `i` sta per `int`, `d` sta per `double`, e i tipi più complessi diventano sigle incomprensibili. Il formato non è stabilito dallo standard e cambia da compilatore a compilatore.

> Nota: in pratica, per sapere che tipo ha dedotto `auto`, il trucco più usato è provocare un errore di proposito — per esempio assegnare la variabile a un tipo sbagliato. Il messaggio del compilatore nominerà il tipo reale, in chiaro e per esteso.

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

## Basi Numeriche: Binario, Ottale, Esadecimale

Quando scrivi `255`, stai usando la **base 10** (decimale): dieci cifre disponibili, da `0` a `9`. È l'abitudine con cui contiamo tutti i giorni, ma non è l'unico modo per scrivere un numero.

Il computer lavora in **base 2** (binario): due sole cifre, `0` e `1`, che corrispondono ai due stati elettrici di un circuito. Poiché scrivere lunghe sequenze di zeri e uni è scomodo per un essere umano, si usano spesso anche la **base 8** (ottale) e la **base 16** (esadecimale), che si convertono in binario con estrema facilità.

| Base | Nome         | Cifre disponibili | Il numero 255 si scrive |
| ---- | ------------ | ----------------- | ----------------------- |
| 2    | Binario      | `0` `1`           | `11111111`              |
| 8    | Ottale       | da `0` a `7`      | `377`                   |
| 10   | Decimale     | da `0` a `9`      | `255`                   |
| 16   | Esadecimale  | da `0` a `9`, poi `A` `B` `C` `D` `E` `F` | `FF` |

In esadecimale le cifre da sole non bastano: servono sedici simboli, quindi dopo il `9` si continua con le lettere. `A` vale 10, `B` vale 11, fino a `F` che vale 15.

Il punto fondamentale: **il numero è sempre lo stesso**. `255`, `0xFF` e `11111111` sono tre modi di scrivere la stessa identica quantità, e in memoria occupano gli stessi identici bit. Cambia solo la notazione con cui lo rappresentiamo.

### Scrivere Numeri in Basi Diverse

C++ ti permette di scrivere un valore direttamente in un'altra base, usando un **prefisso**:

```cpp
int decimale    = 255;          // nessun prefisso -> base 10
int esadecimale = 0xFF;         // prefisso 0x     -> base 16
int ottale      = 0377;         // prefisso 0      -> base 8
int binario     = 0b11111111;   // prefisso 0b     -> base 2 (da C++14)
```

Tutte e quattro le variabili contengono **255**. Il prefisso serve solo al compilatore per capire come leggere le cifre che seguono: una volta letto il valore, la variabile è un normalissimo `int`.

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 255;
    int b = 0xFF;

    cout << a << endl;   // 255
    cout << b << endl;   // 255: cout stampa in decimale, qualunque prefisso tu abbia usato

    return 0;
}
```

> Nota: attenzione allo zero iniziale. `int x = 012;` **non** vale 12: lo zero davanti indica l'ottale, quindi `012` in base 8 corrisponde a 10 in decimale. È un errore classico e silenzioso, perché il programma compila senza lamentarsi.

### Stampare in Basi Diverse: `hex`, `oct`, `dec`

Per stampare un numero in un'altra base si usano i **manipolatori** `hex`, `oct` e `dec`. Si inseriscono nel flusso di `cout` prima del valore da stampare:

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 255;

    cout << dec << numero << endl;   // 255
    cout << hex << numero << endl;   // ff
    cout << oct << numero << endl;   // 377

    return 0;
}
```

Questi manipolatori sono **persistenti**: una volta impostato `hex`, `cout` continua a stampare in esadecimale *tutti* i numeri interi successivi, finché non gli dici di cambiare. È la causa più comune di output inaspettati:

```cpp
cout << hex << 255 << endl;   // ff
cout << 16 << endl;           // 10  <- ancora in esadecimale!

cout << dec;                  // torno esplicitamente in decimale
cout << 16 << endl;           // 16
```

Prendi l'abitudine di rimettere `dec` appena hai finito.

### Rendere l'Output più Leggibile

Due manipolatori aggiuntivi aiutano a capire a colpo d'occhio in che base è scritto un numero:

- `showbase` aggiunge il prefisso (`0x` per l'esadecimale, `0` per l'ottale)
- `uppercase` scrive le lettere esadecimali in maiuscolo

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << hex << 255 << endl;                  // ff
    cout << showbase << 255 << endl;             // 0xff
    cout << uppercase << 255 << endl;            // 0XFF

    cout << nouppercase << noshowbase << dec;    // rimetto tutto a posto

    return 0;
}
```

Ogni manipolatore ha il suo opposto: `noshowbase` e `nouppercase` annullano l'effetto.

> Nota: questi manipolatori arrivano già con `#include <iostream>`, non serve includere altro. La libreria `<iomanip>` serve invece per manipolatori come `setw` (larghezza del campo) e `setprecision` (cifre decimali).

### Stampare in Binario: `bitset`

Il binario è il caso speciale: **non esiste** un manipolatore `bin` per `cout`. Per stampare un numero in base 2 si usa `bitset`, che va incluso a parte:

```cpp
#include <iostream>
#include <bitset>
using namespace std;

int main() {
    int numero = 5;

    cout << bitset<8>(numero)  << endl;   // 00000101
    cout << bitset<16>(numero) << endl;   // 0000000000000101

    cout << bitset<8>(255) << endl;       // 11111111

    return 0;
}
```

Il numero tra parentesi angolari (`<8>`, `<16>`) è quanti bit vuoi vedere, e lo decidi tu. Gli zeri a sinistra vengono aggiunti per riempire lo spazio richiesto.

> Nota: se scegli troppi pochi bit, le cifre in eccesso vengono **tagliate** senza alcun avviso: `bitset<4>(255)` stampa `1111`, non 255. Scegli una dimensione coerente con il tipo che stai stampando (8 bit per un `char`, 32 per un `int`).

### Convertire una Stringa in Numero: `stoi`

Il percorso inverso: hai un testo come `"FF"` e vuoi ottenere il numero 255. La funzione `stoi` (*string to int*) accetta un terzo parametro con la base da usare:

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int da_esadecimale = stoi("FF", nullptr, 16);         // 255
    int da_ottale      = stoi("377", nullptr, 8);         // 255
    int da_binario     = stoi("11111111", nullptr, 2);    // 255
    int da_decimale    = stoi("255");                     // 255 (base 10 di default)

    cout << da_esadecimale << endl;   // 255
    cout << da_ottale      << endl;   // 255
    cout << da_binario     << endl;   // 255
    cout << da_decimale    << endl;   // 255

    return 0;
}
```

Il secondo parametro serve a sapere fino a che punto la stringa è stata letta; quando non ti interessa, scrivi `nullptr`. La base può andare da 2 a 36.

### Convertire un Numero in Stringa

Per il binario basta chiedere la stringa direttamente al `bitset`:

```cpp
#include <bitset>
#include <string>
using namespace std;

string testo = bitset<8>(5).to_string();   // "00000101"
```

Per le altre basi si usa un flusso di testo, `ostringstream`, che funziona esattamente come `cout` ma scrive in una stringa invece che a schermo:

```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    ostringstream flusso;
    flusso << hex << 255;

    string testo = flusso.str();   // "ff"
    cout << testo << endl;

    return 0;
}
```

---

⬅️ [Precedente: Come si strutturano i programmi](2-struttura.md) | [📚 Indice](.github/README.md) | [Successivo: Input e Output](4-input-output.md) ➡️
