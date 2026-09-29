#!/usr/bin/env python3
"""Crea un nuovo capitolo della guida e aggiorna tutto ciò che lo collega.

Uso:
    python3 scripts/nuovo-capitolo.py NUMERO NOME "Titolo"

Esempi:
    python3 scripts/nuovo-capitolo.py 17 classi "Classi e oggetti"
    python3 scripts/nuovo-capitolo.py 16 lista "Lista collegata"   # stesso numero = stesso capitolo

Cosa fa:
    1. crea NUMERO-NOME.md in root con titolo e barra di navigazione;
    2. aggiunge il capitolo alla lista "Capitoli:" di .github/README.md;
    3. riscrive la barra di navigazione del capitolo precedente e del successivo;
    4. aggiorna la riga "Catena:" di CLAUDE.md.

L'ordine dei capitoli è quello della lista nel README: il testo dei link
del README è anche l'etichetta usata nei pulsanti Precedente/Successivo.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / ".github" / "README.md"
CLAUDE_MD = ROOT / "CLAUDE.md"

INDICE = "[📚 Indice](.github/README.md)"
NUMERI_IN_LETTERE = {2: "due", 3: "tre", 4: "quattro", 5: "cinque"}
RIGA_CAPITOLO = re.compile(r"^(\d+)\. (.*)$")
LINK = re.compile(r"\[([^\]]+)\]\(\.\./([^)]+\.md)\)")


def errore(messaggio):
    print(f"Errore: {messaggio}", file=sys.stderr)
    sys.exit(1)


def leggi_capitoli(righe):
    """Restituisce la lista ordinata (numero, file, etichetta) presa dal README."""
    capitoli = []
    dentro = False
    for riga in righe:
        if riga.startswith("## "):
            dentro = riga.startswith("## Capitoli")
            continue
        if dentro and (m := RIGA_CAPITOLO.match(riga)):
            for etichetta, file in LINK.findall(m.group(2)):
                capitoli.append((int(m.group(1)), file, etichetta))
    return capitoli


def aggiorna_readme(righe, numero, file, titolo):
    """Aggiunge il capitolo alla lista: stessa riga se il numero esiste già."""
    link = f"[{titolo}](../{file})"
    ultima_prima = None  # indice dell'ultima riga con numero < numero
    for i, riga in enumerate(righe):
        m = RIGA_CAPITOLO.match(riga)
        if not m:
            continue
        n = int(m.group(1))
        if n == numero:
            link_esistenti = [f"[{e}](../{f})" for e, f in LINK.findall(m.group(2))]
            tutti = link_esistenti + [link]
            elenco = ", ".join(tutti[:-1]) + " e " + tutti[-1]
            quanti = NUMERI_IN_LETTERE.get(len(tutti), str(len(tutti)))
            righe[i] = f"{n}. {elenco} (**sono {quanti} link separati**)"
            return
        if n < numero:
            ultima_prima = i
    if ultima_prima is None:
        errore("non trovo la lista 'Capitoli:' nel README")
    righe.insert(ultima_prima + 1, f"{numero}. {link}")


def barra(precedente, successivo):
    """Costruisce la barra di navigazione; None = pulsante assente."""
    parti = []
    if precedente:
        parti.append(f"⬅️ [Precedente: {precedente[2]}]({precedente[1]})")
    parti.append(INDICE)
    if successivo:
        parti.append(f"[Successivo: {successivo[2]}]({successivo[1]}) ➡️")
    return " | ".join(parti)


def sostituisci_barra(percorso, nuova):
    """Rimpiazza l'ultima riga con il link all'indice (la barra esistente)."""
    righe = percorso.read_text(encoding="utf-8").rstrip("\n").split("\n")
    for i in range(len(righe) - 1, -1, -1):
        if INDICE in righe[i]:
            righe[i] = nuova
            break
    else:
        righe += ["", "---", "", nuova]
    percorso.write_text("\n".join(righe) + "\n", encoding="utf-8")


def aggiorna_catena(capitoli):
    testo = CLAUDE_MD.read_text(encoding="utf-8")
    catena = " → ".join(f"`{c[1].removesuffix('.md')}`" for c in capitoli)
    nuovo, n = re.subn(r"^(- Catena: ).*?(\. Primo senza)", rf"\g<1>{catena}\g<2>",
                       testo, count=1, flags=re.M)
    if n == 0:
        print("Attenzione: riga 'Catena:' non trovata in CLAUDE.md, aggiornala a mano.")
        return
    CLAUDE_MD.write_text(nuovo, encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    numero_testo, nome, titolo = sys.argv[1], sys.argv[2], sys.argv[3].strip()
    if not numero_testo.isdigit():
        errore(f"il numero deve essere un intero, non '{numero_testo}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome):
        errore(f"il nome deve essere kebab-case minuscolo senza accenti (es. 'ciclo-for'), non '{nome}'")
    if not titolo:
        errore("il titolo non può essere vuoto")

    numero = int(numero_testo)
    file = f"{numero}-{nome}.md"
    percorso = ROOT / file
    if percorso.exists():
        errore(f"{file} esiste già")

    righe_readme = README.read_text(encoding="utf-8").split("\n")
    capitoli = leggi_capitoli(righe_readme)
    if not capitoli:
        errore("nessun capitolo trovato nel README")

    # Posizione: subito dopo l'ultimo capitolo con numero <= quello nuovo
    posizione = sum(1 for c in capitoli if c[0] <= numero)
    nuovo = (numero, file, titolo)
    capitoli.insert(posizione, nuovo)
    precedente = capitoli[posizione - 1] if posizione > 0 else None
    successivo = capitoli[posizione + 1] if posizione + 1 < len(capitoli) else None

    percorso.write_text(f"# {titolo}\n\n\n\n---\n\n{barra(precedente, successivo)}\n",
                        encoding="utf-8")

    aggiorna_readme(righe_readme, numero, file, titolo)
    README.write_text("\n".join(righe_readme), encoding="utf-8")

    # I vicini cambiano pulsante: ricalcolo la loro barra con i loro vicini
    for i in (posizione - 1, posizione + 1):
        if 0 <= i < len(capitoli):
            vicino = ROOT / capitoli[i][1]
            prima = capitoli[i - 1] if i > 0 else None
            dopo = capitoli[i + 1] if i + 1 < len(capitoli) else None
            if vicino.exists():
                sostituisci_barra(vicino, barra(prima, dopo))
            else:
                print(f"Attenzione: {capitoli[i][1]} è nel README ma non esiste.")

    aggiorna_catena(capitoli)

    print(f"Creato {file}")
    print(f"  Precedente: {precedente[1] if precedente else '-'}")
    print(f"  Successivo: {successivo[1] if successivo else '-'}")
    print("  Aggiornati: .github/README.md, CLAUDE.md e le barre dei capitoli vicini")


if __name__ == "__main__":
    main()
