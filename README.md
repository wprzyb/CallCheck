# CallCheck
Sprawdza czy znak jest w OSEC'u i w klubie
# Jak uruchomić ten program
1. Uruchom _aktualizujOSEC.sh_
2. Stwórz plik _skrytki.txt_ 
3. Wypełnij _skrytki.txt_ zgodnie z formatem (__ZNAK=SKRYTKA__, *skrytka nie może zawierać znaku równania*)
4. Uruchom _checkPzk.py_ za pomocą Python'a 3
# Dodatkowe polecenia
* /U - Ustawienia, /U <3-LITEROWA NAZWA> <WARTOŚĆ>
* /O - Wypisz członków oddziału, /O<ODZIAŁ> *Zwróć uwagę na brak spacji*
* Ctrl+L - Czyszczenie ekranu
* Ctrl+C - Wyjdź z programu

Ustawienia
----------
* **TRC** - Tryb czyszczcenia, Wartości: *B*, _*_ Wartość *B* uniemożliwi usuwanie znaku innym klawiszem niż BACKSPACE.
Domyślnie: *B*ackspace
* **PNW** - Pozwalaj na wyczyszczenie, Wartości: *T*, *N*, Jeżeli wyświetla się jeden wynik to wciśnięcie klawisza usunie *znak*. Domyślnie: *N*ie
* **DYN** - Dynamiczne wyszukiwanie. Wyszukuj po naciśnięciu klawisza, Wartości: *T*, *N*. Domyślnie: *T*ak
* **MTR** - Maksymalna ilość wyników, Wartości: **int**. Domyślnie: *30*
