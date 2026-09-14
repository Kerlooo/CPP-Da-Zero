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

> Nota: `(double)x` si chiama **cast**: converte temporaneamente il valore di `x` in `double` solo per quel calcolo. La variabile `x` resta un `int`.

> [!WARNING]
> Dividere un intero per zero (`x / 0`) fa **crashare** il programma. Prima di dividere, controlla sempre che il divisore non sia zero.

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
    double rapporto = (double)base / altezza;

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
