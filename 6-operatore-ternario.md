# Operatore Ternario: `?` e `:`

L'operatore ternario (detto anche operatore condizionale) è un'**espressione** che sceglie tra due valori in base a una condizione. Fa lo stesso lavoro di un `if-else` che assegna un valore, ma **su una sola riga**.

## Sintassi Base

```cpp
condizione ? valore_se_true : valore_se_false
```

**Componenti:**
- `condizione` → L'espressione da valutare
- `?` → Domanda: "la condizione è vera?"
- `valore_se_true` → Risultato se la condizione è `true`
- `:` → Altrimenti
- `valore_se_false` → Risultato se la condizione è `false`

> Nota: il ternario **produce un valore**, quindi i due rami devono avere tipi compatibili. `(voto >= 60) ? "PROMOSSO" : 0` non compila: un ramo è un testo, l'altro un numero. Per eseguire istruzioni diverse (non solo scegliere un valore) usa l'`if-else`.

## Esempio

### Con `if-else` tradizionale

```cpp
#include <iostream>
#include <string>
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
#include <string>
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
#include <string>
using namespace std;

int main() {
    int numero;
    string tipo;

    cout << "Inserisci un numero: ";
    cin >> numero;
    tipo = (numero % 2 == 0) ? "Pari" : "Dispari";
    
    cout << "Il numero " << numero << " e' " << tipo << endl;
    return 0;
}
```

**Esecuzione:**
```
Inserisci un numero: 7
Il numero 7 e' Dispari
```

### Esempio 2: Voto Positivo o Negativo

```cpp
#include <iostream>
#include <string>
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
    
    cout << "Il numero piu grande e': " << massimo << endl;
    
    return 0;
}
```

**Output:**
```
Il numero piu grande e': 20
```

> [!WARNING]
> Se usi il ternario direttamente dentro un `cout`, mettilo **tutto tra parentesi**: `cout << (x > y ? x : y);`. Scrivendo `cout << (x > y) ? x : y;` il `<<` viene eseguito per primo: stampa `0` (il risultato di `x > y`) invece del numero più grande.

## Operatore Ternario Annidato

Puoi usare più operatori ternari uno dentro l'altro, anche se può diventare difficile da leggere.

### Esempio: Classificazione Voto

```cpp
#include <iostream>
#include <string>
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

---

⬅️ [Precedente: If Else](6-if-else.md) | [📚 Indice](.github/README.md) | [Successivo: Switch](7-switch.md) ➡️
