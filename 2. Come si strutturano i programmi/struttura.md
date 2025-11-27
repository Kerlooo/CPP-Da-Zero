# Come si strutturano i programmi

## Struttura di base

### 1. Include delle Librerie (Header Files)

All'inizio del programma vanno inserite le **librerie `#include`** che importano le librerie necessarie.

```cpp
#include <iostream>    // Libreria base per Input/Output
#include <vector>      // Libreria per i vettori
#include <cmath>       // Libreria per le funzioni matematiche
```

**Tipi di include:**
- `#include <libreria>` → Librerie standard del sistema (racchiuse tra `< >`)
- `#include "mio_file.h"` → File custom nel tuo progetto (racchiuse tra `" "`)

**Solo la libreria `iostream` è fondamentale**

### 2. Using Namespace std

Dopo gli include, si usa `using namespace std;` per evitare di scrivere `std::` ogni volta.

```cpp
using namespace std;
```

**Cosa significa?**
- `std` è uno **namespace** (spazio dei nomi) che contiene tutte le funzioni e gli oggetti della libreria standard
- Senza `using namespace std;`, dovresti scrivere `std::cout` invece di `cout`
- Scrivere `using namespace std;` è comodo ma può causare conflitti in progetti grandi

### 3. La funzione main()

La funzione `main()` è il **punto di ingresso** del programma. È qui che inizia l'esecuzione.

```cpp
int main() {

}
```

**Spiegazione:**
- `int` → La funzione ritorna un **intero** (0 = successo, altri numeri = errore)
- `main()` → Nome della funzione speciale riconosciuta dal compilatore
- `return 0;` → Segnala al sistema che il programma è terminato correttamente

### Struttura Completa di un Programma

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    // Qui va il tuo codice
    
    return 0;
}
```