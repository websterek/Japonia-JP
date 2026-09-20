# Japonia 2027 — 26 maja–9 czerwca

Publiczny plan podróży: https://websterek.github.io/Japonia-JP/

Przylot i wylot z Tokio. Wylot z Polski 26 maja; przylot 27 maja pozostaje założeniem do potwierdzenia z biletem. 12 pełnych dni zwiedzania (28 maja–8 czerwca), powrót 9 czerwca. Układ noclegów i program zwiedzania nie zostały zmienione przez aktualizację graficzną.

## Aktualna prezentacja

Strona używa bezszeryfowego fontu Ubuntu, dużych fotografii i prostych krawędzi. Zdjęcia są publikowane razem ze stroną na GitHub Pages, a nie pobierane przez przeglądarkę odwiedzającego z Wikimedia. Mapa jest schematem SVG bez zewnętrznych kafelków.

## Edycja i publikacja

- `index.html` — źródłowy program, opisy, czasy, warianty i uwagi. Stary blok CSS jest ignorowany podczas budowania; nie trzeba go edytować.
- `presentation/site.css` — aktualny wygląd, układ telefonu i druk.
- `presentation/build.py` — zachowuje tekst planu, dodaje układ i pobiera legalnie udostępnione fotografie. Tworzy `_site/` z lokalnymi obrazami WebP.
- `presentation/check.py` — przeglądarkowe testy na komputerze i telefonie oraz zrzuty ekranu.
- `presentation/verify_public.py` — test rzeczywistej opublikowanej wersji i wszystkich zdjęć przez HTTPS.
- `.github/workflows/pages.yml` — budowanie, testy i publikacja po zmianie `main`.

W ustawieniach Pages pozostaw **Source: GitHub Actions**. Nie zmieniaj źródła na publikację bezpośrednio z gałęzi, bo ominęłoby to aktualny wygląd i przygotowanie zdjęć.

Zdjęcia są przechowywane w cache procesu budowania; odwiedzający otrzymuje pliki bezpośrednio z GitHub Pages. Jeżeli pobranie fotografii albo test obrazu się nie powiedzie, nowa wersja nie jest publikowana. Poprzednia udana wersja pozostaje dostępna.

Do uruchomienia lokalnego przygotuj środowisko Python z Pillow, beautifulsoup4 i playwright, wykonaj `python presentation/build.py`, a następnie `python -m http.server --directory _site 8000`. Pobranie oryginałów podczas pierwszego budowania wymaga internetu. Font Ubuntu jest ładowany z Google Fonts z systemowym fontem bezszeryfowym jako zapasem.

## Fotografie

Lista źródeł, autorów i licencji znajduje się w `PHOTOS` w skrypcie oraz w stopce opublikowanej strony. Zmiany zdjęć obejmują zmniejszenie, konwersję WebP i kadrowanie przez CSS. Każde zdjęcie zachowuje własną licencję CC BY / CC BY-SA albo status domeny publicznej. Zdjęcia pokazują różne pory roku, nie gwarantowane warunki w terminie wyjazdu.

Nie dodano formularza ani zbierania danych. Treść planu, rezerwacje i kalendarze atrakcji nadal wymagają sprawdzenia przed wyjazdem na 2027 rok.
