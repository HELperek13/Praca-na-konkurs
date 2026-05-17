# 🐢 Turtle Snake

Gra inspirowana kultowym Wężem — ale zamiast węża sterujemy **żółwiem**, który je liście!

## Wymagania

- Python 3.1 lub nowszy
- Tylko moduły ze standardowej biblioteki (`turtle`, `random`, `json`, `os`, `time`)
- Brak zewnętrznych zależności — działa od razu po pobraniu!

## Uruchomienie

```bash
python main.py
```

## Sterowanie

| Klawisz | Akcja |
|---------|-------|
| `↑ ↓ ← →` lub `W A S D` | Zmiana kierunku |
| `R` | Start / Restart |
| `P` | Pauza / Wznowienie |
| `Esc` | Wyjście |

## Zasady gry

- Żółw porusza się **bez zatrzymania** — jak w klasycznym wężu
- Jedz **pomarańczowe liście** (+10 punktów każdy)
- Co 5 zjedzonych liści gra przyspiesza
- Uderzenie w ścianę lub własny ogon = **koniec gry**
- Rekord zapisywany jest automatycznie w pliku `highscore.json`

## Konfiguracja

Plik `config.json` pozwala dostosować grę:

- `cell_size` — rozmiar kratki (domyślnie 20px)
- `cols` / `rows` — rozmiar planszy (domyślnie 28×28)
- `initial_speed` — prędkość startowa w ms (mniej = szybciej)
- `min_speed` — maksymalna prędkość (ograniczenie)
- `start_length` — długość startowa węża

## Struktura projektu

```
turtle_snake/
├── main.py          # Punkt startowy
├── game.py          # Logika gry i rysowanie
├── config.json      # Ustawienia gry
├── highscore.json   # Rekord (tworzony automatycznie)
└── README.md        # Ten plik
```
