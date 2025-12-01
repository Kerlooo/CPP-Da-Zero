# If, Else e Else If in C++

Le istruzioni condizionali permettono al programma di prendere decisioni e eseguire codice diverso in base a condizioni specifiche.

## Struttura Base: `if`

L'istruzione `if` esegue un blocco di codice **solo se una condizione è vera**.

### Sintassi

```cpp
if (condizione) {
    // Codice eseguito se la condizione è true
}
```

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 18;
    
    if (eta >= 18) {
        cout << "Sei maggiorenne!" << endl;
    }
    
    return 0;
}
```

**Output:**
```
Sei maggiorenne!
```

## `if` con `else`

L'istruzione `else` esegue un blocco di codice se la condizion
 è **falsa**.

### Sintassi

```cpp
if (condizione) {
    // Codice se condizione è true
}
else {
    // Codice se condizione è false
}
```

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 15;
    
    if (eta >= 18) {
        cout << "Sei maggiorenne!" << endl;
    }
    else {
        cout << "Sei minorenne." << endl;
    }
    
    return 0;
}
```

**Output:**
```
Sei minorenne.
```

## `else if`

Quando hai **più di due condizioni**, usa `else if` per testare condizioni aggiuntive.

### Sintassi

```cpp
if (condizione1) {
    // Codice se condizione1 è true
}
else if (condizione2) {
    // Codice se condizione1 è false E condizione2 è true
}
else if (condizione3) {
    // Codice se condizione1 e condizione2 sono false E condizione3 è true
}
else {
    // Codice se nessuna condizione precedente è true
}
```

### Esempio

```cpp
#include <iostream>
using namespace std;

int main() {
    int voto = 75;
    
    if (voto >= 90) {
        cout << "Voto: A (Eccellente)" << endl;
    }
    else if (voto >= 80) {
        cout << "Voto: B (Buono)" << endl;
    }
    else if (voto >= 70) {
        cout << "Voto: C (Sufficiente)" << endl;
    }
    else if (voto >= 60) {
        cout << "Voto: D (Passabile)" << endl;
    }
    else {
        cout << "Voto: F (Insufficiente)" << endl;
    }
    
    return 0;
}
```

**Output:**
```
Voto: C (Sufficiente)
```

## Operatori di Confronto

Prima di usare `if`, devi conoscere gli operatori per creare condizioni:

| Operatore | Significato       | Esempio | Risultato |
|-----------|-------------------|---------|-----------|
| `==`      | Uguale a          | `5 == 5`| `true`    |
| `!=`      | Diverso da        | `5 != 3`| `true`    |
| `>`       | Maggiore di       | `5 > 3` | `true`    |
| `<`       | Minore di         | `5 < 3` | `false`   |
| `>=`      | Maggiore o uguale | `5 >= 5`| `true`    |
| `<=`      | Minore o uguale   | `5 <= 3`| `false`   |

## Operatori Logici

Puoi combinare più condizioni usando operatori logici:

### AND (`&&`)

Entrambe le condizioni devono essere **true**.

```cpp
if (eta >= 18 && eta <= 65) {
    cout << "Sei in eta lavorativa" << endl;
}
```

| Condizione 1 | Condizione 2 | Risultato |
|--------------|--------------|-----------|
| `true`       | `true`       | `true`    |
| `true`       | `false`      | `false`   |
| `false`      | `true`       | `false`   |
| `false`      | `false`      | `false`   |

### OR (`||`)

**Almeno una** delle condizioni deve essere `true`.

```cpp
if (giorno == "Sabato" || giorno == "Domenica") {
    cout << "E' weekend!" << endl;
}
```

| Condizione 1 | Condizione 2 | Risultato |
|--------------|--------------|-----------|
| `true`       | `true`       | `true`    |
| `true`       | `false`      | `true`    |
| `false`      | `true`       | `true`    |
| `false`      | `false`      | `false`   |

### NOT (`!`)

Inverte il risultato della condizione.

```cpp
bool piove = true;

if (!piove) {
    cout << "Non piove, posso uscire!" << endl;
} else {
    cout << "Piove, prendo l'ombrello." << endl;
}
```

| Condizione | Risultato |
|------------|-----------|
| `true`     | `false`   |
| `false`    | `true`    |

## Tabella Completa degli Operatori Logici

A       | B       | A && B  | A \|\| B  | !A
--------|---------|---------|-----------|--------
true    | true    | true    | true      | false
true    | false   | false   | true      | false
false   | true    | false   | true      | true
false   | false   | false   | false     | true

## Esempi Pratici con Operatori Logici

### Esempio 1: AND

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 25;
    bool ha_patente = true;
    
    if (eta >= 18 && ha_patente) {
        cout << "Puoi guidare!" << endl;
    }
    else {
        cout << "Non puoi guidare." << endl;
    }
    
    return 0;
}
```

**Output:**
```
Puoi guidare!
```

### Esempio 2: OR

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 12;
    
    if (eta < 5 || eta > 65) {
        cout << "Hai diritto a uno sconto!" << endl;
    }
    else {
        cout << "Prezzo pieno." << endl;
    }
    
    return 0;
}
```

**Output:**
```
Hai diritto a uno sconto!
```

### Esempio 3: NOT

```cpp
#include <iostream>
using namespace std;

int main() {
    bool login_valido = false;
    
    if (!login_valido) {
        cout << "Credenziali non valide. Riprova." << endl;
    }
    
    return 0;
}
```

**Output:**
```
Credenziali non valide. Riprova.
```

> NB: Un `if` non ha per forza bisogno di un `else` ma un `else` deve sempre avere un `if` prima