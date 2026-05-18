🛰️ Mars Rover Simulator: Misja na Czerwonej Planecie
[Projekt: Symulacja gry tekstowej z wizualizacją 2D]

Witamy w interaktywnej symulacji misji marsjańskiego łazika! Projekt został stworzony jako zaawansowany przykład symulacji fizycznej i zarządzania zasobami, wykorzystując pętli grę, losowe zdarzenia i wizualizację graficzną.

🌟 Zawartość i Funkcjonalności
Projekt realizuje najbardziej wymagające elementy mechaniki gry na platformie Python, integrując logikę symulacji tekstowej z wizualizacją w module turtle.

🛠️ SPEŁNIENIE WYMOGÓWEŃ TECHNICZNYCH
Walidacja Wejścia: Program wprowadza zaawansowaną walidację dla wszystkich parametrów startowych (pozycje, kąt, energia, cel), prosi o poprawki w przypadku błędów i używa wartości domyślnych.
Symulacja Fizyczna: Ruch do przodu jest obliczany poprawnie za pomocą funkcji trygonometrycznych ($\cos$ i $\sin$) z uwzględnieniem kąta startowego.
Interfejs Tekstowy (Logika): Każdy krok generuje szczegółowy, uporządkowany log w konsoli, pokazujący stan przed/po ruchu, zmienne i wszystkie zdarzenia.
Wizualizacja Graficzna (turtle): Łazik rysuje swoją trasę na płótnie w czasie rzeczywistym. Na początku mapy są zaznaczone granice świata, punkt startu (zielony) i cel (czerwony).
Zarządzanie Zasobami: Energia (bateria) jest głównym zasobem, który jest zużywany w każdym ruchu.
🌍 ELEMENTY ŚWIATA I ZDARZENIA (Mechanika)
Kratery (Przeszkody): Dotknięcie krateru powoduje dodatkową i natychmiastową utratę energii (kara).
Panele Słoneczne / Skrzynie: Trafienie na bonusowy element powoduje regenerację energii (bonus).
Burze Piaskowe (Losowe): Z pewnym prawdopodobieństwem zdarza się burza, która nie tylko obniża energię, ale również losowo zmienia kąt pojazdu.
Awaria Systemu (Losowe): Bardzo rzadkie zdarzenie, które powoduje tymczasowe spowolnienie lub spadek energii.
📊 RAPORT KOŃCOWY (Podsumowanie)
Po zakończeniu gry, niezależnie od przyczyny (sukces, porażka, limit), generowany jest szczegółowy raport zawierający:

Podsumowanie parametrów początkowych i końcowych.
Liczbę wykonanych kroków.
Całkowite zużycie i poziom pozostałej energii.
Statystyki zidentyfikowanych elementów świata (np. "2x Krater", "3x Burza Piaskowa").
Ostateczny wynik gry.
🚀 Jak uruchomić projekt
Wymagania Wstępne
Python 3.6 lub nowsza wersja (zalecany Python 3.11).
Nie są wymagane żadne zewnętrzne biblioteki poza standardową dystrybucją Pythona (turtle, random, math, time).
Instalacja
Skopiuj cały kod do pliku o nazwie main.py.
Upewnij się, że masz odpowiednie środowisko uruchomieniowe Python.
Uruchom grę z terminala:
python main.py
Obsługa Gry
Program poprosi o podanie wszystkich parametrów misji (Nazwa, Pozycja startowa, Kąt, Energia, Cel).
Po rozpoczęciu symulacji, w każdej turze program wyświetli:
Aktualny stan (Pozycja, Kąt, Energia).
Listę dostępnych akcji i ich kosztów energetycznych.
Wprowadź jedną z akcji:
F: Move Forward (Ruch do przodu)
L: Left (Obrót o 15° w lewo)
R: Right (Obrót o 15° w prawo)
N: None (Pozostań w miejscu)
Obserwuj logi w konsoli oraz wizualny ruch łazika w otwierającym się oknie turtle.
Gra trwa do momentu osiągnięcia celu, wyczerpania energii, lub przekroczenia limitu kroków.
🎯 Cel gry
Ostatecznym celem jest zorganizowanie i opuszczenie obszaru badań marsjańskich – dotarcie do wyznaczonych współrzędnych Bazy Badawczej przed wyczerpaniem całej dostępnej energii.

Powodzenia na Marsie!
