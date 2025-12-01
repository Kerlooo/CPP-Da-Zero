# Input/Output in C++

L'Input/Output (I/O) è fondamentale in C++. Permette al programma di:
- **Output**: Visualizzare messaggi e dati sullo schermo
- **Input**: Ricevere dati dall'utente tramite tastiera

## Output: `cout`

`cout` (character output) stampa dati sullo schermo.

### Sintassi Base

```cpp
cout << valore;
```

L'operatore `<<` è chiamato **stream insertion operator** e invia i dati verso lo stream di output.

### Esempio (senza usare `namespace std;`)

```cpp
#include <iostream>

int main() {
    std::cout << "Output!";
    std::cout << 42;
    std::cout << 3.14;
    
    return 0;
}
```

**Output:**
```
Output!423.14
```

### Esempi (usando `using namespace std;`)

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Output!";
    cout << 42;
    cout << 3.14;
    
    return 0;
}
```

### Andare a Capo: `endl`

Per andare a capo, si usa `endl` (end line):

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Prima riga" << endl;
    cout << "Seconda riga" << endl;
    cout << "Terza riga" << endl;
    
    return 0;
}
```

**Output:**
```
Prima riga
Seconda riga
Terza riga
```

### Concatenare Output

Puoi concatenare più valori usando più `<<`:

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 25;
    string nome = "Marco";
    
    cout << "Nome: " << nome << endl;
    cout << "Eta: " << eta << endl;
    cout << "Il mio nome è " << nome << " e ho " << eta << " anni" << endl;
    
    return 0;
}
```

**Output:**
```
Nome: Marco
Eta: 25
Il mio nome è Marco e ho 25 anni
```

## Input: `cin`

`cin` (character input) legge dati inseriti dall'utente.

### Sintassi Base

```cpp
cin >> variabile;
```

L'operatore `>>` è chiamato **stream extraction operator** e riceve i dati dallo stream di input.

### Esempi (senza usare `namespace std;`)

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    
    std::cout << "Inserisci un numero: ";
    std::cin >> numero;
    std::cout << "Hai inserito: " << numero << std::endl;
    
    return 0;
}
```

**Esecuzione:**
```
Inserisci un numero: 42
Hai inserito: 42
```

### Esempi (usando `namespace std;`)

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    
    cout << "Inserisci un numero: ";
    cin >> numero;
    cout << "Hai inserito: " << numero << endl;
    
    return 0;
}
```

### Leggere Più Input

Puoi leggere più valori concatenando `>>`:

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int base, altezza;
    cout << "Inserisci base e altezza: ";
    cin >> base >> altezza;
    
    return 0;
}
```