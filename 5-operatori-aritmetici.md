# Operatori Aritmetici in C++

Gli operatori aritmetici servono a fare calcoli con le variabili e con i numeri. Sono la base di quasi ogni programma: prima di poter prendere decisioni (`if`) o ripetere istruzioni (cicli), bisogna saper calcolare.

## I Cinque Operatori di Base

| Operatore | Nome            | Esempio  | Risultato |
| --------- | --------------- | -------- | --------- |
| `+`       | Addizione       | `7 + 3`  | `10`      |
| `-`       | Sottrazione     | `7 - 3`  | `4`       |
| `*`       | Moltiplicazione | `7 * 3`  | `21`      |
| `/`       | Divisione       | `7 / 3`  | `2`       |
| `%`       | Modulo (resto)  | `7 % 3`  | `1`       |

> Nota: `7 / 3` fa `2` e non `2.33`. Il motivo è spiegato qui sotto, nella sezione sulla divisione.

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 7;
    int b = 3;

    cout << "Somma: " << a + b << endl;           // 10
    cout << "Differenza: " << a - b << endl;      // 4
    cout << "Prodotto: " << a * b << endl;        // 21
    cout << "Divisione: " << a / b << endl;       // 2
    cout << "Resto: " << a % b << endl;           // 1

    return 0;
}
```

**Output:**
```
Somma: 10
Differenza: 4
Prodotto: 21
Divisione: 2
Resto: 1
```

## La Divisione: Intera o Decimale?

Questo è l'errore più comune per chi inizia. Il risultato della divisione dipende dal **tipo degli operandi**, non dal tipo della variabile in cui salvi il risultato.

- Se **entrambi** gli operandi sono interi → la divisione è **intera**: la parte decimale viene buttata via (non arrotondata).
- Se **almeno uno** dei due è decimale (`float` o `double`) → la divisione è **decimale**.

```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 7;
    int y = 2;

    cout << x / y << endl;              // 3   -> int / int = divisione intera
    cout << 7.0 / 2 << endl;            // 3.5 -> uno dei due è decimale

    double risultato = x / y;           // ATTENZIONE: vale 3, non 3.5
    cout << risultato << endl;          // 3

    double corretto = (double)x / y;    // forziamo x a double: 3.5
    cout << corretto << endl;           // 3.5

    return 0;
}
```

> Nota: `(double)x` si chiama **cast**: converte temporaneamente il valore di `x` in `double` solo per quel calcolo. La variabile `x` resta un `int`. Alla sezione [Conversioni di Tipo](#conversioni-di-tipo) vedremo come funzionano nel dettaglio.

> [!WARNING]
> Dividere un intero per zero (`x / 0`) fa **crashare** il programma. Prima di dividere, controlla sempre che il divisore non sia zero.

## Conversioni di Tipo

Nell'esempio sopra abbiamo scritto `(double)x` per ottenere una divisione decimale. Quella operazione si chiama **conversione di tipo**, o **cast**: prendere un valore di un tipo e usarlo come se fosse di un altro tipo.

Le conversioni sono di due famiglie: quelle che fa il compilatore da solo e quelle che chiedi tu esplicitamente.

### Conversioni Implicite

Quando in un'espressione compaiono tipi diversi, il compilatore converte automaticamente il valore "più piccolo" verso quello "più grande", senza che tu debba scrivere nulla:

```cpp
int interi = 5;
double decimali = 2.5;

double risultato = interi + decimali;   // interi diventa 5.0, risultato vale 7.5
```

Questo è il motivo per cui `7.0 / 2` dà `3.5`: il `2` viene convertito in `2.0` prima della divisione.

La conversione automatica avviene anche nel verso opposto, ed è lì che nascono i problemi. Assegnare un `double` a un `int` **tronca** la parte decimale: non arrotonda, la butta via.

```cpp
int troncato = 9.99;      // vale 9, non 10
int negativo = -3.7;      // vale -3, non -4
```

> Nota: molti compilatori segnalano questi casi con un *warning*, non con un errore. Il programma compila lo stesso, ma il dato che hai perso non torna più indietro.

### Conversioni Esplicite: `static_cast`

Quando la conversione la vuoi tu, la scrivi in modo esplicito. C++ mette a disposizione `static_cast`:

```cpp
static_cast<tipo_destinazione>(valore)
```

**Esempio:**
```cpp
#include <iostream>
using namespace std;

int main() {
    int voti_totali = 17;
    int numero_esami = 4;

    double media = static_cast<double>(voti_totali) / numero_esami;

    cout << "Media: " << media << endl;   // Media: 4.25

    return 0;
}
```

Basta convertire **uno solo** dei due operandi: da quel momento la divisione diventa decimale, e il compilatore converte l'altro da solo.

Il cast non modifica la variabile di partenza. `voti_totali` resta un `int` che vale `17`: la conversione produce un valore temporaneo, usato solo per quel calcolo.

### `static_cast` o `(tipo)valore`?

Le due scritture fanno la stessa cosa in questo contesto:

```cpp
double a = (double)voti_totali / numero_esami;                 // stile C
double b = static_cast<double>(voti_totali) / numero_esami;    // stile C++
```

La prima è ereditata dal C ed è più corta. La seconda è quella consigliata in C++ moderno, per due motivi: si vede a colpo d'occhio anche in mezzo a un'espressione lunga, e il compilatore rifiuta le conversioni davvero insensate invece di provarci comunque.

Troverai la forma `(double)x` in tantissimo codice esistente, quindi va conosciuta. Nel codice che scrivi tu, preferisci `static_cast`.

### Il Caso Classico: la Percentuale

```cpp
#include <iostream>
using namespace std;

int main() {
    int risposte_corrette = 7;
    int domande_totali = 9;

    double percentuale_sbagliata = (risposte_corrette / domande_totali) * 100;
    double percentuale_corretta = (static_cast<double>(risposte_corrette) / domande_totali) * 100;

    cout << "Sbagliata: " << percentuale_sbagliata << endl;   // 0
    cout << "Corretta:  " << percentuale_corretta << endl;    // 77.7778

    return 0;
}
```

Nella prima riga la divisione `7 / 9` avviene tra interi e vale `0`. Moltiplicare `0` per `100` dà `0`: il cast arrivato dopo, sul risultato, non serve a niente. La conversione va fatta **prima** della divisione, non dopo.

## L'Operatore Modulo `%`

Il modulo restituisce il **resto** della divisione intera.

| Espressione | Divisione | Resto |
| ----------- | --------- | ----- |
| `10 % 3`    | 10 : 3 = 3 con resto 1 | `1` |
| `10 % 5`    | 10 : 5 = 2 con resto 0 | `0` |
| `4 % 7`     | 4 : 7 = 0 con resto 4  | `4` |

Il suo uso più frequente è capire se un numero è **pari o dispari**: un numero è pari se il resto della divisione per 2 è zero.

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero = 14;

    cout << "Resto della divisione per 2: " << numero % 2 << endl;  // 0 -> pari

    return 0;
}
```

> [!WARNING]
> `%` funziona **solo con i numeri interi**. Su `float` e `double` dà errore di compilazione.

## Incremento `++` e Decremento `--`

Aumentare o diminuire una variabile di 1 è così frequente che C++ ha due operatori dedicati.

```cpp
int contatore = 5;

contatore++;    // ora vale 6  (equivale a contatore = contatore + 1)
contatore--;    // ora vale 5  (equivale a contatore = contatore - 1)
```

### Prefisso e Postfisso

Entrambi gli operatori si possono scrivere **prima** o **dopo** la variabile. Il valore finale della variabile è lo stesso, ma cambia il valore **restituito dall'espressione**:

| Forma  | Nome      | Cosa fa                                  |
| ------ | --------- | ---------------------------------------- |
| `++x`  | Prefisso  | Prima incrementa, poi restituisce il valore nuovo |
| `x++`  | Postfisso | Prima restituisce il valore vecchio, poi incrementa |

```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 5;
    cout << x++ << endl;    // stampa 5, poi x diventa 6
    cout << x << endl;      // 6

    int y = 5;
    cout << ++y << endl;    // y diventa 6, poi stampa 6
    cout << y << endl;      // 6

    return 0;
}
```

> Nota: se l'incremento è su una riga da solo (`contatore++;`), prefisso e postfisso sono equivalenti. La differenza conta solo quando usi il risultato dentro un'altra espressione.

## Operatori di Assegnazione Composti

Sono scorciatoie per modificare una variabile usando il suo valore attuale.

| Operatore | Esempio   | Equivale a     |
| --------- | --------- | -------------- |
| `=`       | `x = 5`   | assegna 5 a x  |
| `+=`      | `x += 3`  | `x = x + 3`    |
| `-=`      | `x -= 3`  | `x = x - 3`    |
| `*=`      | `x *= 3`  | `x = x * 3`    |
| `/=`      | `x /= 3`  | `x = x / 3`    |
| `%=`      | `x %= 3`  | `x = x % 3`    |

```cpp
#include <iostream>
using namespace std;

int main() {
    int punteggio = 100;

    punteggio += 50;    // 150
    punteggio -= 20;    // 130
    punteggio *= 2;     // 260
    punteggio /= 4;     // 65

    cout << "Punteggio finale: " << punteggio << endl;

    return 0;
}
```

**Output:**
```
Punteggio finale: 65
```

## Precedenza degli Operatori

Come in matematica, non tutti gli operatori vengono valutati nello stesso ordine. Si parte dall'alto della tabella.

| Priorità | Operatori     | Descrizione                          |
| -------- | ------------- | ------------------------------------ |
| 1 (alta) | `()`          | Parentesi                            |
| 2        | `++` `--`     | Incremento e decremento              |
| 3        | `*` `/` `%`   | Moltiplicazione, divisione, modulo   |
| 4        | `+` `-`       | Addizione e sottrazione              |
| 5 (bassa)| `=` `+=` `-=` | Assegnazione                         |

```cpp
#include <iostream>
using namespace std;

int main() {
    int risultato1 = 2 + 3 * 4;      // prima 3*4=12, poi 2+12 -> 14
    int risultato2 = (2 + 3) * 4;    // prima 2+3=5,  poi 5*4  -> 20

    cout << risultato1 << endl;      // 14
    cout << risultato2 << endl;      // 20

    return 0;
}
```

> Nota: nel dubbio, usa le parentesi. Non rallentano il programma e rendono il codice leggibile.

## Funzioni Matematiche: `<cmath>`

Gli operatori coprono le quattro operazioni, ma non bastano per una radice quadrata o una potenza. Per quelle C++ mette a disposizione una libreria di funzioni già pronte, da includere in cima al file:

```cpp
#include <cmath>
```

### Le Funzioni più Usate

| Funzione      | Cosa calcola                        | Esempio          | Risultato |
| ------------- | ----------------------------------- | ---------------- | --------- |
| `sqrt(x)`     | Radice quadrata                     | `sqrt(16)`       | `4`       |
| `pow(x, y)`   | `x` elevato a `y`                   | `pow(2, 10)`     | `1024`    |
| `abs(x)`      | Valore assoluto (toglie il segno)   | `abs(-7.5)`      | `7.5`     |
| `round(x)`    | Arrotonda all'intero più vicino      | `round(3.6)`     | `4`       |
| `floor(x)`    | Arrotonda per difetto                | `floor(3.9)`     | `3`       |
| `ceil(x)`     | Arrotonda per eccesso                | `ceil(3.1)`      | `4`       |
| `fmod(x, y)`  | Resto della divisione tra decimali   | `fmod(7.5, 2.0)` | `1.5`     |
| `sin(x)` `cos(x)` `tan(x)` | Funzioni trigonometriche (in radianti) | `sin(0)` | `0` |
| `log(x)`      | Logaritmo naturale                   | `log(1)`         | `0`       |
| `log10(x)`    | Logaritmo in base 10                 | `log10(1000)`    | `3`       |
| `exp(x)`      | `e` elevato a `x`                    | `exp(0)`         | `1`       |

### Esempio

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    cout << sqrt(25) << endl;        // 5
    cout << pow(3, 4) << endl;       // 81
    cout << abs(-12.5) << endl;      // 12.5
    cout << round(7.5) << endl;      // 8
    cout << floor(7.9) << endl;      // 7
    cout << ceil(7.1) << endl;       // 8

    return 0;
}
```

> Nota: queste funzioni restituiscono quasi sempre un `double`, anche quando il risultato sembra intero. `sqrt(25)` vale `5`, ma è il `double` `5.0`: se lo assegni a un `int`, la parte decimale viene troncata come visto nella sezione sulle conversioni.

### `pow` non è una Scorciatoia

`pow(x, 2)` funziona, ma per un semplice quadrato `x * x` è più rapido da leggere e da calcolare. Riserva `pow` agli esponenti che non conosci in anticipo o che non sono piccoli numeri interi.

```cpp
double lato = 4.0;

double area1 = lato * lato;     // Preferibile
double area2 = pow(lato, 2);    // Stesso risultato, senza vantaggi
```

### Arrotondare Davvero

Nella sezione sulle conversioni hai visto che assegnare un `double` a un `int` **tronca**. Se quello che vuoi è un arrotondamento vero, `round` va usato **prima** del cast:

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double valore = 7.8;

    int troncato = static_cast<int>(valore);            // 7  -> butta via il decimale
    int arrotondato = static_cast<int>(round(valore));  // 8  -> arrotonda, poi converte

    cout << "Troncato:    " << troncato << endl;
    cout << "Arrotondato: " << arrotondato << endl;

    return 0;
}
```

**Output:**
```
Troncato:    7
Arrotondato: 8
```

### Pi Greco

C++ standard **non** definisce una costante per pi greco. Su alcuni compilatori esiste `M_PI`, ma non è garantita: se ti serve, dichiarala tu.

```cpp
const double PI = 3.14159265358979;

double raggio = 5.0;
double area = PI * pow(raggio, 2);      // 78.5398
```

> Nota: le funzioni trigonometriche lavorano in **radianti**, non in gradi. Per convertire: `radianti = gradi * PI / 180`.

### Esempio: Teorema di Pitagora

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double cateto1, cateto2;

    cout << "Inserisci i due cateti: ";
    cin >> cateto1 >> cateto2;

    double ipotenusa = sqrt(pow(cateto1, 2) + pow(cateto2, 2));

    cout << "Ipotenusa: " << ipotenusa << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci i due cateti: 3 4
Ipotenusa: 5
```

> Nota: `min` e `max`, che spesso si cercano qui, non stanno in `<cmath>` ma in `<algorithm>`. Si usano come `max(a, b)` e restituiscono il maggiore o il minore dei due valori.

## Esempio Completo

```cpp
#include <iostream>
using namespace std;

int main() {
    int base, altezza;

    cout << "Inserisci base e altezza del rettangolo: ";
    cin >> base >> altezza;

    int perimetro = (base + altezza) * 2;
    int area = base * altezza;

    // La divisione tra interi taglierebbe i decimali: usiamo un double
    double rapporto = static_cast<double>(base) / altezza;

    cout << "Perimetro: " << perimetro << endl;
    cout << "Area: " << area << endl;
    cout << "Rapporto base/altezza: " << rapporto << endl;

    return 0;
}
```

**Esecuzione:**
```
Inserisci base e altezza del rettangolo: 7 2
Perimetro: 18
Area: 14
Rapporto base/altezza: 3.5
```

---

⬅️ [Precedente: Input e Output](4-input-output.md) | [📚 Indice](.github/README.md) | [Successivo: If Else](6-if-else.md) ➡️
