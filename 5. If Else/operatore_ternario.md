# Operatore Ternario: `?` e `:`

L'operatore ternario (detto anche operatore condizionale) permette di scrivere un'istruzione `if-else` **su una sola riga** in modo conciso.

## Sintassi Base

```cpp
condizione ? valore_se_true : valore_se_false
```

**Componenti:**
- `condizione` --> L'espressione da valutare
- `?` → Domanda: "la condizione è vera?"
- `valore_se_true` --> Risultato se la condizione è `true`
- `:` → Altrimenti
- `valore_se_false` --> Risultato se la condizione è `false`

## Esempio

### Con `if-else` tradizionale

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 18;
    string risultato;
    
    if (eta >= 18) {
        risultato = "Maggiorenne";
    } 
    else {
        risultato = "Minorenne";
    }
    
    cout << risultato << endl;
    
    return 0;
}
```

### Con operatore ternario

```cpp
#include <iostream>
using namespace std;

int main() {
    int eta = 18;
    
    string risultato = (eta >= 18) ? "Maggiorenne" : "Minorenne";
    
    cout << risultato << endl;
    
    return 0;
}
```

**Output (entrambi):**
```
Maggiorenne
```

## Esempi Pratici

### Esempio 1: Numero Pari o Dispari

```cpp
#include <iostream>
using namespace std;

int main() {
    int numero;
    string tipo;

    cout << "Inserisci un numero: ";
    cin >> numero;
    tipo = (numero % 2 == 0) ? "Pari" : "Dispari";
    
    cout << "Il numero " << numero << " è " << tipo << endl;
    return 0;
}
```

### Esempio 2: Voto Positivo o Negativo

```cpp
#include <iostream>
using namespace std;

int main() {
    int voto = 65;
    
    string esito = (voto >= 60) ? "PROMOSSO" : "BOCCIATO";
    
    cout << "Risultato: " << esito << endl;
    
    return 0;
}
```

**Output:**
```
Risultato: PROMOSSO
```

### Esempio 3: Assegnazione Diretta

```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 10;
    int y = 20;
    
    int massimo = (x > y) ? x : y;
    
    cout << "Il numero piu grande è: " << massimo << endl;
    
    return 0;
}
```

**Output:**
```
Il numero piu grande è: 20
```

## Operatore Ternario Annidato

Puoi usare più operatori ternari uno dentro l'altro, anche se può diventare difficile da leggere.

### Esempio: Classificazione Voto

```cpp
#include <iostream>
using namespace std;

int main() {
    int voto = 78;
    
    string classificazione = (voto >= 90) ? "A" : 
                             (voto >= 80) ? "B" : 
                             (voto >= 70) ? "C" : 
                             (voto >= 60) ? "D" : "F";
    
    cout << "Classificazione: " << classificazione << endl;
    
    return 0;
}
```

**Output:**
```
Classificazione: C
```