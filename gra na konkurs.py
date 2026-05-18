import turtle
import random
import math
import time
import sys

# --- Konfiguracja Stałych ---
WORLD_SIZE = 100
MAX_STEPS = 200
MOVE_COST = 5
TURN_COST = 1
CRATER_PENALTY = 10
SOLAR_BONUS = 20
SANDSTORM_PENALTY = 15

# Definicja elementów świata (dla prostoty kolizji)
ENVIRONMENT = {
    "craters": [(15, 15), (-20, 5), (5, -20)],
    "solar_panels": [(30, 0), (0, 30)],
    "storage_crates": [(50, 50)]
}

# Globalne zmienne dla zarządzania stanem gry
game_state = {}

# --- Funkcje Walidacji i Inputu ---

def get_user_input_validated(prompt, type_check=float):
    """Pętla do bezpiecznego pobierania danych od użytkownika."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("⚠️ Pole nie może być puste. Proszę spróbować ponownie.")
                continue
                
            if type_check == int:
                val = int(user_input)
                return val
            else:
                val = type_check(user_input)
                return val
        except ValueError:
            print("❌ Błąd: Wprowadzono niepoprawny typ danych. Proszę użyć liczb.")

def init_game():
    """Pobiera i waliduje wszystkie parametry początkowe gry."""
    print("-" * 50)
    print("🛰️ WŁASNY ROZWÓD: KONFIGURACJA MISJI MARSOWSKIEJ")
    print("-" * 50)
    
    # 1. Nazwa misji/łazika
    name = input("🔬 Nazwa misji/łazika (np. Misja Phoenix): ").strip() or "Łazik Mars Pathfinder"
    
    # 2. Pozycja startowa
    print("\n--- Konfiguracja Startu ---")
    while True:
        try:
            x_str = input("Enter X startowe (np. 0): ").strip()
            y_str = input("Enter Y startowe (np. 0): ").strip()
            start_x = float(x_str) if x_str else 0
            start_y = float(y_str) if y_str else 0
            
            if abs(start_x) > WORLD_SIZE or abs(start_y) > WORLD_SIZE:
                 raise ValueError("Pozycja poza granicami świata.")
            
            break
        except ValueError as e:
            print(f"⚠️ Błąd: Upewnij się, że podane współrzędne mieszczą się między {-WORLD_SIZE} a {WORLD_SIZE}. {e}")
            
    # 3. Kąt startowy
    while True:
        try:
            angle_str = input("Enter kąt startowy (0-359, 0=Wschód): ").strip()
            start_angle = float(angle_str) if angle_str else 0
            if 0 <= start_angle < 360:
                break
            else:
                print("⚠️ Kąt musi być między 0 a 359 stopni.")
        except:
            print("⚠️ Kąt musi być liczbą.")
            
    # 4. Początkowa energia
    while True:
        try:
            energy_str = input("Enter początkową energię (min. 10): ").strip()
            start_energy = int(energy_str) if energy_str else 100
            if start_energy >= 0:
                break
            else:
                print("⚠️ Energia musi być liczbą dodatnią.")
        except ValueError:
            print("⚠️ Energia musi być liczbą całkowitą.")

    # 5. Cel wyprawy
    print("\n--- Konfiguracja Celu ---")
    while True:
        try:
            cel_x = float(input("Enter cel X (Baza): ").strip() or 50)
            cel_y = float(input("Enter cel Y (Baza): ").strip() or 50)
            if abs(cel_x) > WORLD_SIZE or abs(cel_y) > WORLD_SIZE:
                raise ValueError("Cel poza granicami świata.")
            break
        except ValueError:
            print("⚠️ Błąd: Współrzędne celu muszą być w granicach świata.")

    # Inicjalizacja stanu gry
    game_state.update({
        'name': name,
        'x': start_x,
        'y': start_y,
        'angle': start_angle,
        'energy': start_energy,
        'target_x': cel_x,
        'target_y': cel_y,
        'history': [],  # Log najważniejszych zdarzeń
        'steps': 0,
        'is_running': True
    })
    
    return game_state

# --- Setup Graficzny (Turtle) ---

def setup_turtle():
    """Konfiguruje okno graficzne i łazika."""
    screen = turtle.Screen()
    screen.setup(width=1000, height=800)
    screen.title("Mars Rover Simulation")
    # Ustawienie trybu grafiki dla gładniejszego rysowania
    screen.tracer(0)
    
    rover = turtle.Turtle()
    rover.speed(0)  # Najszybciej
    rover.penup()
    rover.hideturtle()
    rover.pensize(3)
    rover.color("darkred")
    
    # Rysowanie granic świata
    draw_world_bounds(rover, screen)
    
    return screen, rover

def draw_world_bounds(rover, screen):
    """Rysuje prostokątną ramkę świata na płótnie."""
    rover.penup()
    rover.goto(-WORLD_SIZE, -WORLD_SIZE)
    rover.pendown()
    rover.color("gray")
    rover.pensize(2)
    
    # Rysowanie granic
    rover.goto(-WORLD_SIZE, WORLD_SIZE)
    rover.pendown()
    rover.hideturtle()
    
def draw_initial_markers(rover, x, y):
    """Rysuje punkty startu i celu na mapie."""
    rover.penup()
    
    # Start (Zielony)
    rover.goto(x, y)
    rover.dot(10, "green")
    
    # Cel (Czerwony)
    rover.goto(game_state['target_x'], game_state['target_y'])
    rover.dot(10, "red")
    
    # Ustawienie początkowej pozycji łazika na grafice
    rover.goto(x, y)
    rover.setheading(game_state['angle'])
    time.sleep(1)
    screen.update()

# --- Logika Ruchu i Zdarzeń ---

def calculate_movement(x, y, angle, distance=1.0):
    """Oblicza nowe współrzędne na podstawie kąta i odległości."""
    angle_rad = math.radians(angle)
    new_x = x + math.cos(angle_rad) * distance
    new_y = y + math.sin(angle_rad) * distance
    return new_x, new_y

def check_environment(x, y):
    """Sprawdza, czy łazik trafił na element świata."""
    
    # 1. Krater
    if (x, y) in ENVIRONMENT['craters']:
        return "Krater", CRATER_PENALTY, "Wypadając na teren niestabilny (Krater)!", True
        
    # 2. Panel Słoneczny
    elif (x, y) in ENVIRONMENT['solar_panels']:
        return "Panel Słoneczny", SOLAR_BONUS, "Znaleziono panel słoneczny! Energia się regeneruje.", False
        
    # 3. Skrzynia
    elif (x, y) in ENVIRONMENT['storage_crates']:
        return "Skrzynia", 25, "Znaleziono skrzynię z zapasem energii!", False
    
    return "Neutralny", 0, "", False

def check_random_event(step):
    """Generuje losowe zdarzenie (Burza, Awaria)."""
    
    # Burza Piaskowa (10% szansy co krok)
    if random.random() < 0.10:
        penalty = SANDSTORM_PENALTY
        new_angle = random.randint(0, 359)
        return "Burza Piaskowa", penalty, f"Silna burza piaskowa uderzyła w łazik! Energia spada o {penalty}. Kierunek jest zmieniony na {new_angle}°.", new_angle
    
    # Awaria Systemu (2% szansy co krok)
    if random.random() < 0.02:
        return "Awaria Systemu", 0, "Awaria! Układ napędowy zawiesił się na tę turę. Energia spada minimalnie.", None
    
    return None, 0, "", None


def run_simulation(state, rover, screen):
    """Główna pętla symulacji."""
    
    print("\n" + "=" * 50)
    print("🚀 START SYMULACJI WYPRAWY NA MARS")
    print("=" * 50)
    
    max_steps_reached = False
    
    while state['is_running']:
        state['steps'] += 1
        
        # --- Sprawdzenie warunków zakończenia ---
        if state['steps'] > MAX_STEPS:
            print(f"\n🚨 KONIEC GRY: Przekroczono limit kroków ({MAX_STEPS}).")
            state['is_running'] = False
            break
            
        if state['energy'] <= 0:
            print("\n🚨 KONIEC GRY: Energia wyczerpana. Łazik zgasł.")
            state['is_running'] = False
            break
        
        # 1. Wyświetlanie stanu
        print("\n" + "#" * 60)
        print(f"--- KROK {state['steps']} ---")
        print(f"STAN: Pozycja ({state['x']:.1f}, {state['y']:.1f}) | Kąt: {state['angle']}° | Energia: {state['energy']}")
        print("#" * 60)

        # 2. Pobranie akcji od użytkownika
        print("\n[Akcje dostępne]:")
        print("   'F' - Jedź do przodu (Koszt: 5 energii).")
        print("   'L' - Obróć w lewo (Koszt: 1 energii).")
        print("   'R' - Obróć w prawo (Koszt: 1 energii).")
        print("   'N' - Pozostań w miejscu (Koszt: 1 energii).")
        
        action = input("Wybierz akcję (F/L/R/N): ").upper()
        
        # Domyślne wartości dla tymczasowych zmian
        new_x, new_y, new_angle, energy_change = state['x'], state['y'], state['angle'], 0
        movement_log = ""
        
        # 3. Wykonanie ruchu i wyliczenie zmian
        if action == 'F':
            if state['energy'] < MOVE_COST:
                print("🛑 Za mało energii na ruch do przodu!")
                continue # Nie wykonujemy ruchu, ale zwiększamy krok (zgodnie z logiką)
            
            # Obliczanie nowego położenia
            new_x, new_y = calculate_movement(state['x'], state['y'], state['angle'], distance=1.0)
            energy_change = -MOVE_COST
            movement_log = "Ruch do przodu."
            
        elif action == 'L':
            if state['energy'] < TURN_COST:
                print("🛑 Za mało energii na obrót!")
                continue
            new_angle = state['angle'] - 15
            energy_change = -TURN_COST
            movement_log = "Obrót o 15° w lewo."
            
        elif action == 'R':
            if state['energy'] < TURN_COST:
                print("🛑 Za mało energii na obrót!")
                continue
            new_angle = state['angle'] + 15
            energy_change = -TURN_COST
            movement_log = "Obrót o 15° w prawo."
            
        elif action == 'N':
            if state['energy'] < TURN_COST:
                print("🛑 Za mało energii, by utrzymać system.")
                continue
            new_angle = state['angle']
            energy_change = -TURN_COST
            movement_log = "Pozostawanie w miejscu."
        
        else:
            print("❌ Nieznana komenda. Proszę użyć F, L, R lub N.")
            continue
            
        # Aktualizacja stanu po podstawowym ruchu
        current_energy = state['energy'] + energy_change
        state['x'], state['y'], state['angle'], state['energy'] = new_x, new_y, new_angle % 360, current_energy

        
        # 4. Aktualizacja graficzna (Turtle)
        rover.clear() # Czyścimy poprzednią ścieżkę
        
        # Rysowanie trasy do nowej pozycji
        start_pos = (state['x'] - 1.0 * math.cos(math.radians(state['angle'])), 
                     state['y'] - 1.0 * math.sin(math.radians(state['angle']))) # Przybliżony punkt startowy ruchu
        
        # Turtle rysuje po zaktualizowanej pozycji, więc trzeba ustawić ją na punkcie startowym
        # Dla uproszczenia, rysujemy tylko linię od starej pozycji do nowej, używając globalnego stanu.
        rover.penup()
        rover.goto((state['x'] - (new_x - state['x'])/2), (state['y'] - (new_y - state['y'])/2))
        rover.pendown()
        rover.color("blue")
        rover.goto(new_x, new_y)

        # 5. Sprawdzenie i obsługa elementów świata/zdarzeń
        
        print(f"\n[{movement_log}] ->")
        
        # A. Sprawdzenie elementów stałych
        env_type, env_value, env_message, is_hazard = check_environment(state['x'], state['y'])
        
        energy_change_total = energy_change
        event_log_message = ""

        if is_hazard:
            # Krater - priorytetowe zużycie energii
            energy_change_total -= CRATER_PENALTY
            state['history'].append("Krater")
            event_log_message = f"⚠️ UWAGA: Krater! Dodatkowe zużycie: {CRATER_PENALTY} energii."
            
        elif env_type != "Neutralny":
            # Panel/Skrzynia - bonus
            energy_change_total += env_value
            state['history'].append(env_type)
            event_log_message = f"✨ {env_message}"
        
        # B. Sprawdzenie zdarzeń losowych
        random_type, random_penalty, random_message, random_angle = check_random_event(state['steps'])
        
        if random_type:
            energy_change_total -= random_penalty
            state['history'].append(random_type)
            event_log_message += f"\n⚡ Zdarzenie losowe: {random_message}"
            
            # Zmiana kąta po burzy
            if random_angle is not None:
                state['angle'] = random_angle
                print(f"   >>> KĄT ZMIENIONY NA {random_angle}° przez burzę.")
                
        # C. Aktualizacja Energii
        
        # Musimy zapewnić, że energia nie spadnie poniżej zera
        final_energy = max(0, state['energy'] + energy_change_total)
        
        # Jeśli spadnie poniżej zera, ustawiamy na zero i ustawiamy flagę porażki
        if final_energy < state['energy']:
            energy_change_display = f" {state['energy']} -> {final_energy}"
        else:
            energy_change_display = f" {state['energy']} -> {final_energy}"

        state['energy'] = final_energy
        
        # 6. Raportowanie w konsoli
        print(f"Pozycja: ({state['x']:.1f}, {state['y']:.1f})")
        print(f"Kąt: {state['angle']:.1f}° | Energia: {energy_change_display}")
        print(f"=== Efekty: {event_log_message}")

        # 7. Sprawdzenie czy dotarliśmy do celu
        if abs(state['x'] - state['target_x']) < 2 and abs(state['y'] - state['target_y']) < 2:
            print("\n🎉 GRATULACJE! Dotarcie do celu potwierdzone!")
            state['is_running'] = False
            break

        # Pauza wizualna
        time.sleep(1.5)
        screen.update()


def end_report(state, result_message):
    """Generuje i wyświetla końcowy raport z wyprawy."""
    
    print("\n" + "█" * 60)
    print("██ RAPORT KOŃCOWY MISJI MARSOWSKIEJ ██".center(60, '█'))
    print("█" * 60)
    
    # Zliczanie zdarzeń
    event_counts = {"Krater": 0, "Panel Słoneczny": 0, "Awaria Systemu": 0, "Burza Piaskowa": 0}
    for event in state['history']:
        if event in event_counts:
            event_counts[event] += 1
        elif event == "Skrzynia":
             event_counts["Skrzynia"] = event_counts.get("Skrzynia", 0) + 1
    
    # Wyświetlanie statystyki
    print("\n[STATYSTYKA WYPRAWY]")
    print(f"-> Nazwa Misji: {state['name']}")
    print(f"-> Cel: ({state['target_x']:.1f}, {state['target_y']:.1f})")
    print(f"-> Koszty i Bonuse: {event_counts}")
    
    print("\n[WARUNKI KOŃCOWE]")
    print(f"-> Przyczyna Zakończenia: {result_message}")
    print(f"-> Wynik: {'SUKCES' if 'Sukces' in result_message else 'PORAŻKA / CZĘŚCIOWY SUKCES'}")
    
    print("\n[PODSUMOWANIE PARAMETRÓW]")
    print(f"-> Kroków wykonanych: {state['steps']}")
    print(f"-> Energia początkowa: {100 - state['history'].count('Krater') * 10} (dla przykładu)")
    print(f"-> Energia końcowa: {state['energy']}")
    print(f"-> Pozycja startowa: ({state['x']-1.0*math.cos(math.radians(state['angle'])), state['y']-1.0*math.sin(math.radians(state['angle']))})") # Użyjemy punktu startowego, który jest bardziej miarodajny
    print(f"-> Pozycja końcowa: ({state['x']:.1f}, {state['y']:.1f})")
    print(f"-> Kąt końcowy: {state['angle']:.1f}°")
    
    print("\n" + "█" * 60)
    input("Naciśnij ENTER, aby zakończyć symulację.")


# --- Główna Funkcja Wykonawcza ---

def main():
    """Kontroluje cykl życia gry."""
    while True:
        try:
            # 1. Inicjalizacja
            state = init_game()
            
            # 2. Setup grafiki
            screen, rover = setup_turtle()
            draw_world_bounds(rover, screen)
            draw_initial_markers(rover, state['x'], state['y'])
            
            # 3. Uruchomienie symulacji
            result_message = ""
            if state['is_running']:
                run_simulation(state, rover, screen)
                
                # Określenie wyniku po zakończeniu pętli
                if state['energy'] <= 0:
                    result_message = "Brak energii baterii."
                elif state['steps'] > MAX_STEPS:
                    result_message = "Limit kroków przekroczony."
                elif abs(state['x'] - state['target_x']) < 2 and abs(state['y'] - state['target_y']) < 2:
                    result_message = "Cel osiągnięty. Misja zakończona sukcesem!"
                else:
                    # Jeśli się zatrzymało z innych przyczyn
                    result_message = "Symulacja zakończona przerwaniem przez użytkownika."

            # 4. Raportowanie
            end_report(state, result_message)

        except Exception as e:
            print(f"\n[WYSOKI POZIOM BŁĘDU]: Wystąpił krytyczny błąd: {e}")
        
        # Pytanie o kontynuację
        if input("\nCzy chcesz rozpocząć nową symulację? (t/n): ").lower() != 't':
            print("\nDziękujemy za grę! Do zobaczenia na Marsie.")
            sys.exit(0)

if __name__ == "__main__":
    main()
