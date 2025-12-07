# Restaurant Client-Server Application

Aplikacja klient-serwer symulująca działanie restauracji. Projekt zaliczeniowy z programowania zaawansowanego.

## Struktura projektu

```
├── models.py        # Definicje klas: Soup, MainCourse, Dessert
├── server.py        # Serwer restauracji
├── client.py        # Klient (gość restauracji)
└── README.md
```

## Klasy modeli (`models.py`)

Aplikacja definiuje trzy klasy, każda z dwoma polami i metodami specjalnymi:

| Klasa | Pola | Opis |
|-------|------|------|
| `Soup` | `name: str`, `temperature: int` | Zupa z temperaturą podania |
| `MainCourse` | `name: str`, `price: float` | Danie główne z ceną |
| `Dessert` | `name: str`, `calories: int` | Deser z kalorycznością |

Każda klasa implementuje:
- `__init__` - konstruktor
- `__str__` / `__repr__` - reprezentacja tekstowa
- `__eq__` - porównywanie obiektów
- `__hash__` - hashowanie
- `describe()` - dodatkowa metoda opisowa

## Serwer (`server.py`)

### Funkcjonalności:
- Przy starcie tworzy po **4 obiekty** każdej klasy z różnymi danymi
- Przechowuje obiekty w mapie z kluczami: `Soup_1`, `Soup_2`, `MainCourse_1`, itd.
- Obsługuje **wielu klientów równocześnie** (wielowątkowość)
- Limit klientów: `MAX_CLIENTS = 3`
- **Losowe opóźnienia** przy obsłudze (0.5-2s)
- Loguje na konsoli: połączenia, odmowy, wysyłane obiekty

### Protokół komunikacji:
1. Klient wysyła swoje ID
2. Serwer odpowiada: `OK` lub `REFUSED`
3. Klient wysyła nazwę klasy (np. `"Soup"`)
4. Serwer odsyła zserializowaną kolekcję obiektów
5. Jeśli klasa nie istnieje (np. `"Drink"`) - serwer wysyła fallback obiekt innego typu - zupę

## Klient (`client.py`)

### Przepływ działania:
1. Łączy się z serwerem i wysyła swoje ID
2. Odbiera status: `OK` lub `REFUSED`
3. Przy `REFUSED` - kończy działanie
4. Przy `OK` - wyświetla menu i czeka na wybór użytkownika:
   ```
   === RESTAURANT MENU ===
   1. Soup
   2. MainCourse
   3. Dessert
   4. Drink
   =======================
   Choose option (1-4):
   ```
5. Wysyła żądanie do serwera
6. Odbiera kolekcję i przetwarza ją strumieniowo
7. Obsługuje błędy rzutowania gdy otrzyma obiekt innego typu niż oczekiwany

## Uruchomienie

### Wymagania
- Python 3.x

### Krok 1: Uruchom serwer
```powershell
python server.py
```

### Krok 2: Uruchom klienta (w nowym terminalu)
Można uruchomić wielu klientów w wielu terminalach. Wpuszczonych zostanie tylko tylu ile określono w `MAX_ClIENTS`
```powershell
python client.py
```

## Technologie

- **Socket** - komunikacja TCP/IP
- **Pickle** - serializacja obiektów Python
- **Threading** - obsługa wielu klientów równocześnie
