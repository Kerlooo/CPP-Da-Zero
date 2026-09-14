# Il Compilatore: da Codice a Programma

Prima di scrivere una sola riga di C++, serve capire una cosa: il computer **non capisce** il C++.

Il codice che scrivi è testo, leggibile da un essere umano. Il processore invece esegue solo **linguaggio macchina**, una sequenza di numeri. Il **compilatore** è il programma che fa da traduttore tra i due mondi.

```
codice sorgente  ──[ compilatore ]──>  file eseguibile
  programma.cpp                         programma / programma.exe
   (testo)                              (linguaggio macchina)
```

Il file che ottieni alla fine è **autonomo**: per eseguirlo non serve più né il codice sorgente né il compilatore.

## Cosa Succede Durante la Compilazione

La traduzione avviene in quattro fasi. Le lanci tutte con un solo comando, ma è utile sapere che esistono: quando un errore compare, il messaggio ti dice **in quale fase** è successo.

| Fase | Nome | Cosa fa |
| ---- | ---- | ------- |
| 1 | **Preprocessore** | Esegue le righe che iniziano con `#`, come `#include`: incolla nel tuo file il contenuto delle librerie richieste |
| 2 | **Compilazione** | Traduce il C++ in assembly e controlla che il codice rispetti le regole del linguaggio |
| 3 | **Assemblatore** | Converte l'assembly in codice macchina, creando un *file oggetto* |
| 4 | **Linker** | Unisce i file oggetto e il codice delle librerie in un unico file eseguibile |

> Nota: i due errori più comuni per chi inizia sono **errori di compilazione** (fase 2: hai sbagliato a scrivere il codice, per esempio un punto e virgola mancante) e **errori di linking** (fase 4: il codice è corretto ma manca un pezzo, per esempio hai dimenticato di scrivere la funzione `main`).

## `g++`: Il Compilatore che Useremo

**GCC** (*GNU Compiler Collection*) è una raccolta di compilatori gratuiti e open source. Il suo compilatore C++ si chiama **`g++`**, ed è quello usato in tutta questa guida: è gratuito, funziona su Windows, Linux e macOS, e i comandi sono identici ovunque.

> Nota: esistono anche altri compilatori (Clang, MSVC di Microsoft). Imparato `g++`, passare agli altri è questione di cambiare il nome del comando.

## Installazione su Linux

Su Linux `g++` è nei repository ufficiali: una riga e hai finito.

**Debian / Ubuntu / Linux Mint:**
```bash
sudo apt update
sudo apt install g++
```

**Arch Linux / Manjaro:**
```bash
sudo pacman -S gcc
```

**Fedora:**
```bash
sudo dnf install gcc-c++
```

### Verificare l'Installazione

```bash
g++ --version
```

Se risponde con un numero di versione, è tutto a posto:

```
g++ (GCC) 14.2.1 20250207
Copyright (C) 2024 Free Software Foundation, Inc.
```

## Installazione su Windows

Windows non include nessun compilatore C++. La via più semplice è **MSYS2**, un ambiente che porta su Windows gli strumenti da riga di comando del mondo Linux, `g++` compreso.

### 1. Scaricare e Installare MSYS2

Scarica l'installer dal sito ufficiale **[msys2.org](https://www.msys2.org/)** e installalo lasciando il percorso proposto, cioè `C:\msys64`.

### 2. Installare g++

Al termine dell'installazione si apre un terminale. Dal menu Start cerca e apri **MSYS2 UCRT64** (attenzione: non "MSYS2 MSYS", è un ambiente diverso), poi digita:

```bash
pacman -S mingw-w64-ucrt-x86_64-gcc
```

Conferma con `Invio` quando chiede se procedere.

### 3. Aggiungere g++ al PATH

Questo passaggio serve a poter usare `g++` da **qualsiasi** terminale di Windows (Prompt dei comandi, PowerShell, terminale di VS Code) e non solo da quello di MSYS2.

1. Premi `Win` e cerca **"Modifica le variabili di ambiente relative al sistema"**
2. Clicca su **Variabili d'ambiente...**
3. Nel riquadro in basso seleziona la riga **`Path`** e clicca **Modifica...**
4. Clicca **Nuovo** e incolla il percorso: `C:\msys64\ucrt64\bin`
5. Conferma con **OK** su tutte le finestre aperte

> [!WARNING]
> Chiudi e riapri il terminale dopo aver modificato il PATH: le finestre già aperte continuano a usare il valore vecchio e sembrerà che l'installazione non abbia funzionato.

### Verificare l'Installazione

Apri il **Prompt dei comandi** o **PowerShell** e digita:

```bash
g++ --version
```

Se ottieni `'g++' non è riconosciuto come comando interno o esterno`, il PATH non è configurato correttamente: ricontrolla il punto 3 e riapri il terminale.

## Il Primo Programma

Crea un file chiamato `ciao.cpp` con dentro questo codice:

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Ciao, mondo!" << endl;
    return 0;
}
```

> Nota: l'estensione deve essere `.cpp`. Se usi il Blocco note di Windows, assicurati che il file non venga salvato come `ciao.cpp.txt`: nella finestra di salvataggio scegli "Tutti i file" come tipo.

Non è importante capire ora cosa fa ogni riga: serve solo qualcosa da compilare. Le spiegazioni arrivano nei [prossimi](1-introduzione.md) [capitoli](2-struttura.md).

## Compilare da Terminale

Il procedimento è identico su Windows e Linux e si compone di tre passi: **spostarsi** nella cartella del file, **compilare**, **eseguire**.

### 1. Spostarsi nella Cartella

Il comando `cd` (*change directory*) sposta il terminale nella cartella indicata.

```bash
cd Documenti/cpp
```

Con `cd ..` torni indietro di una cartella. Per vedere i file presenti nella cartella corrente:

| Sistema | Comando |
| ------- | ------- |
| Linux   | `ls`    |
| Windows (Prompt) | `dir` |
| Windows (PowerShell) | `ls` oppure `dir` |

> Nota: se il percorso contiene spazi, va messo tra virgolette: `cd "I miei progetti"`.

### 2. Compilare

```bash
g++ ciao.cpp -o ciao
```

Il comando si legge così:

| Parte      | Significato                                    |
| ---------- | ---------------------------------------------- |
| `g++`      | Il compilatore                                 |
| `ciao.cpp` | Il file sorgente da compilare                  |
| `-o ciao`  | *output*: come chiamare il file eseguibile      |

**Se non compare nessun messaggio, la compilazione è riuscita.** Il compilatore parla solo quando c'è un problema: nessuna notizia è una buona notizia.

> Nota: se ometti `-o nome`, il compilatore crea un file con un nome predefinito: `a.out` su Linux, `a.exe` su Windows. Meglio dare sempre un nome esplicito.

### 3. Eseguire

Qui, e **solo qui**, i due sistemi si comportano in modo diverso.

**Linux:**
```bash
./ciao
```

**Windows:**
```bash
ciao.exe
```

**Output (identico sui due sistemi):**
```
Ciao, mondo!
```

> [!WARNING]
> Su Linux il `./` iniziale è obbligatorio. Significa "l'eseguibile che si trova in **questa** cartella": senza, il sistema cerca un programma chiamato `ciao` tra quelli installati, non lo trova e risponde `comando non trovato`.

### Riepilogo dei Comandi

| Passo     | Linux              | Windows                |
| --------- | ------------------ | ---------------------- |
| Compilare | `g++ ciao.cpp -o ciao` | `g++ ciao.cpp -o ciao` |
| Eseguire  | `./ciao`           | `ciao.exe`             |

Su Windows l'estensione `.exe` viene aggiunta automaticamente dal compilatore, anche se scrivi solo `-o ciao`.

## Opzioni Utili di g++

Le opzioni si aggiungono al comando, prima o dopo il nome del file.

| Opzione        | A cosa serve                                                |
| -------------- | ----------------------------------------------------------- |
| `-o nome`      | Sceglie il nome dell'eseguibile                              |
| `-Wall`        | Attiva **tutti gli avvisi**: segnala codice sospetto ma non illegale |
| `-std=c++17`   | Compila secondo lo standard C++17                            |
| `-g`           | Include le informazioni di debug, necessarie al debugger      |

Il comando consigliato mentre si impara:

```bash
g++ -Wall -std=c++17 ciao.cpp -o ciao
```

> Nota: `-Wall` è prezioso per un principiante. Gli **avvisi** (*warning*) non bloccano la compilazione, ma segnalano cose che quasi sicuramente sono errori: una variabile dichiarata e mai usata, un confronto sospetto, un valore mai restituito. Leggili sempre.

## Errori Frequenti

| Messaggio | Causa | Soluzione |
| --------- | ----- | --------- |
| `g++: command not found` / `'g++' non è riconosciuto` | Compilatore non installato o PATH non configurato | Rifai l'installazione; su Windows ricontrolla il PATH e riapri il terminale |
| `No such file or directory` | Sei nella cartella sbagliata, o hai sbagliato il nome del file | Verifica con `ls` (o `dir`) che il file sia lì; attenzione a maiuscole e minuscole |
| `comando non trovato` eseguendo il programma su Linux | Manca il `./` davanti al nome | Scrivi `./ciao` |
| `undefined reference to 'main'` | Errore di **linking**: manca la funzione `main` | Controlla di aver scritto `int main()` |
| `expected ';' before ...` | Errore di **compilazione**: punto e virgola mancante | Guarda la riga indicata **e quella sopra**: spesso il `;` manca alla precedente |

> Nota: quando gli errori sono tanti, correggi **sempre il primo** e ricompila. Un solo errore all'inizio del file ne genera spesso una decina a cascata, che spariscono tutti insieme.

## Ricompilare Dopo Ogni Modifica

Questo è il punto da ricordare meglio di ogni altro:

> [!WARNING]
> L'eseguibile è una **fotografia** del codice al momento della compilazione. Se modifichi il `.cpp` e lo riesegui senza ricompilare, vedrai ancora il comportamento vecchio.

Il ciclo di lavoro è sempre lo stesso:

```
scrivi il codice  ->  compila  ->  esegui  ->  correggi  ->  ricompila  ->  ...
```

---

[📚 Indice](.github/README.md) | [Successivo: Introduzione a C++](1-introduzione.md) ➡️
