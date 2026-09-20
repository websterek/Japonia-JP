# Japonia 2027 — 26 maja–9 czerwca

Zaktualizowana strona grupowego wyjazdu. **Przylot i wylot w Japonii: Tokio.**

## Zaktualizowane daty

- **26 maja:** dodany osobny dzień wylotu do Japonii.
- **27 maja:** przylot do Tokio przyjęty z poprzedniego planu, do sprawdzenia z biletem.
- **28 maja–8 czerwca:** 12 pełnych dni zwiedzania.
- **9 czerwca:** wylot z Tokio i powrót zgodnie z rezerwacją.

Rok **2027** zachowany z wcześniejszej wersji. Nie otrzymano numerów lotów, dokładnego dnia przylotu, godzin ani lotniska w Tokio. Nie wstawiono wymyślonego rozkładu i nie uznano, że 26 maja oznacza przylot do Japonii. Założenie przylotu 27 maja jest widoczne na początku strony oraz przy dniu lotu/przylotu.

**Nie przesunięto programu zwiedzania ani noclegów.** Przy przylocie 27 maja plan obejmuje 13 noclegów: Tokio 3 + Kioto 2 + Osaka 4 + Hakone 1 + Tokio 3. Noc 26/27 maja to podróż, a ostatni nocleg jest 8/9 czerwca w Tokio. Powrót do Tokio z Hakone 6 czerwca daje trzy noce w mieście wylotu.

Zachowano korektę: Nintendo Museum/Uji w poniedziałek 31 maja, Arashiyama we wtorek 1 czerwca. Wcześniejsze informacje o rezerwacjach wymagają ponownego sprawdzenia przed zakupem biletów na 2027.

## Wgranie na GitHub Pages

Zastąp dotychczasowe pliki zawartością ZIP-a, wraz z katalogami `assets` i `licenses`. Plik `index.html` powinien znajdować się w katalogu publikowanym przez GitHub Pages, bez dodatkowego folderu nadrzędnego.

Jeżeli Pages jest już włączone, wystarczy nowy commit. W nowym repozytorium: **Settings → Pages → Deploy from a branch → main → / (root)**. Plik `.nojekyll` jest dołączony. Nie ma npm, procesu budowania, klucza API ani serwera aplikacyjnego.

Oficjalna instrukcja: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Działanie i edycja

- `index.html` — cała treść, opisy, daty, notatki, rezerwacje i wbudowane mapy.
- `styles.css` — wygląd, telefon i druk.
- `app.js` — lokalne przełączanie map, klawiatura, obsługa zdjęć i druk.
- `photos.json` — dokumentacja zdjęć, autorów, źródeł i licencji.
- `assets/trasa-*.svg` — edytowalne kopie map.
- `assets/coastline.geojson` — geometria źródłowa wycinka Japonii.
- `licenses/` — kopie licencji danych geograficznych.

**Mapa działa bez internetu i bez serwera kafelków.** Nie korzysta z Leaflet, zewnętrznych skryptów ani mapowego API. Warianty: cała trasa, Kioto/Osaka, Tokio/okolice. Tokio zaznaczono jako miejsce zarówno przylotu, jak i wylotu. Linie pokazują schemat połączeń, nie rzeczywisty przebieg torów.

Zdjęcia pozostają zewnętrzne (Wikimedia Commons) i wymagają internetu. Nie są dołączone lokalnie. Gdy miniatura zawiedzie, strona próbuje raz załadować oryginał; przy braku połączenia zachowuje podpis i link do źródła. Brak zdjęć nie blokuje mapy ani planu. Linki ↗ otwierają zewnętrzne lokalizacje i wymagają internetu.

## Źródła i licencje

Zdjęcia i ich atrybucja zachowane z wcześniejszej wersji. Każdy plik zachowuje licencję wskazaną w stopce oraz `photos.json`; wizualne kadry zdjęć CC BY-SA pozostają na tej licencji. Zdjęcia pokazują różne pory roku, nie prognozę warunków wyjazdu.

Geografia: **GSHHG** (P. Wessel, W.H.F. Smith i współautorzy), dystrybucja przez **basemap-data**. Dane przycięto do środkowej Japonii i uproszczono z tolerancją 0,002 stopnia. Edytowalny wycinek w `assets/coastline.geojson`, licencja **LGPL-3.0-or-later**, kopie tekstów licencji w `licenses/`. Źródła: https://www.soest.hawaii.edu/pwessel/gshhg/ i https://matplotlib.org/basemap/ . Basemap nie jest wymagany do uruchomienia strony.

W tej aktualizacji zmieniono daty podróży i ich prezentację; nie weryfikowano na nowo cen ani dostępności atrakcji na 2027. Oficjalne źródła są podlinkowane w notatkach dni i rezerwacjach. Godziny zwiedzania są propozycjami, nie oficjalnym rozkładem.
