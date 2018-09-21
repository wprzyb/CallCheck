"""Mały program do sprawdzania zanków w osecu
Licencja: GNU GPL v3

Copyright (C) 2018 Maciej Marciniak (SO5AM)"""
from textwrap import dedent
import time  # NOQA
import subprocess
import os
import signal
import json
import getpass
import hashlib
try:
    import mmw
except ImportError as err:
    print('mmw:', err)
    print('Nie można zaimportować mmw3.py.')
    print('Wciśnij Ctrl C aby się zatrzymać ten program, i się wylogować.')
    print('.... prawdopodobnie')
    while 1:
        pass

if __name__ != '__main__':
    raise ImportError('Why you import my program?')

num = 0

def przekoduj_plik(nazwa, kodowanie_pliku='Latin2'):
    """Przekoduj plik (duh)"""
    zaw_pliku = []
    with open(nazwa, 'r', encoding=kodowanie_pliku) as plk_czt:
        zaw_pliku = plk_czt.readlines()
        # linie = []
        # num_lini = 0
        # while 1:
        #     num += 1
        #     linia = plk_czt.readline()
        #     if linia == "":
        #         break
        #     linie.append(line)
        #     print('\033[A\033[2KPrzeczytano linię', num, '/ ?')
        # print('\033[A\033[2KPrzeczytano', num, 'linii\n')
    with open(nazwa, 'w') as plk_zaps:
        for numer, linia in enumerate(zaw_pliku):
            plk_zaps.write(linia)
            procent_zapisany = format(num/len(zaw_pliku)*100, '.0f')
            print('\033[A\033[2KZapisywanie linii', numer, '/', len(zaw_pliku),
                  str(procent_zapisany)+"%")
        print('\033[A\033[2KZapisano', len(zaw_pliku), 'linii')
        print('['+nazwa+']: Plik Przekodowany\n')


print('\n')
try:
    with open('osec_pzk.txt', 'r') as osec_pzk_f:
        osec_pzk_raw = osec_pzk_f.readlines()  # Zawartość nie przetworzona
        osec_pzk_raw.pop(0)
    with open('osec_kluby.txt', 'r') as osec_kluby_f:
        osec_kluby_raw = osec_kluby_f.readlines()
        osec_kluby_raw.pop(0)
except UnicodeDecodeError:
    print('Przekodowano 0/2')
    przekoduj_plik('osec_pzk.txt')
    print('Przekodowano 1/2')
    przekoduj_plik('osec_kluby.txt')
    print('Przekodowano 2/2')
    time.sleep(1)
    with open('osec_pzk.txt', 'r') as osec_pzk_f:
        osec_pzk_raw = osec_pzk_f.readlines()  # Zawartość nie przetworzona
        osec_pzk_raw.pop(0)
    with open('osec_kluby.txt', 'r') as osec_kluby_f:
        osec_kluby_raw = osec_kluby_f.readlines()
        osec_kluby_raw.pop(0)
osec_pzk = []
for num, line in enumerate(osec_pzk_raw):
    procent = format(num/len(osec_pzk_raw)*100, '.0f')
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(osec_pzk_raw),
          '(' + str(procent)+'%')
    while '  ' in line:  # Dwie spacje som w tym stringu
        line = line.replace('  ', ' ')
    osec_pzk.extend(line[:-1].split(' ')
                    if 'oddział' not in line.lower()
                    else [line[:-1]])
osec_pzk_raw = osec_pzk + []
osec_pzk = []
for num, linia_pzk in enumerate(osec_pzk_raw):
    if linia_pzk != '':
        osec_pzk.append(linia_pzk)
# for num, line in enumerate(lines):
#     print('\033[A\033[2KKonwertowanie linii', num, '/', len(lines))
#     newline = line
#     newlines.extend(line.split(' ') if 'oddział' not in line.lower() else
#                     [line])
kluby_fin = {}
for num, line in enumerate(osec_kluby_raw):
    procent = format(num/len(osec_kluby_raw)*100, '.0f')
    print('\033[A\033[2KKonwertowanie linii', num, '/',
          len(osec_kluby_raw), '(' +
          str(procent)+'%')
    newline = line
    while '  ' in newline:
        newline = newline.replace('  ', ' ')
    spl = newline[:-1].split(' ')
    for snum in range(1, len(spl), 2):
        try:
            part = spl[snum]
        except IndexError:
            continue
        if part not in ['KLUBY', 'INNE', 'ZNAKI']:
            try:
                kluby_fin[part] = spl[snum+1]
            except IndexError:
                continue
# print('\033[A\033[2K(PZK)Usunięto spacje w', len(newlines), 'liniach')
# print('(KLUBY)Usunięto spacje w', len(nowekluby), 'liniach')
# lines = newlines
# newlines = []
# kluby = nowekluby
# nowekluby = []
print()

# lines = newlines
# newlines = []
#
# lines = newlines
# newlines = []
oddzial = ''
przet_odzialy = []
pzk = {}
pzk.update(kluby_fin)
print(osec_pzk)
for num, line in enumerate(osec_pzk):
    if line[0] == ' ':
        przet_odzialy.append(oddzial+'')
        oddzial = line.split(' ')[2]
        # print('\033[2A\033[2KPrzetworzone oddziły:', ' '.join(przet_odzialy))
        print('\033[2KPrzetwarzanie oddziału:', oddzial)
        # time.sleep(0.1)
    else:
        pzk[line] = oddzial
print('\033[2A\033[2KLiczba przetworzonych oddziałów:',
      len(przet_odzialy))
del przet_odzialy

print('\033[2KLista liczy:', len(pzk.keys()), 'wpisów')
print('Czytanie pliku skrytki.txt.')
skr = open('skrytki.txt', "r")
skrl = skr.readlines()
skr.close()
del skr
skrr = []
skrs = []
skrytki = {}
for elem in skrl:
    skrs.append(elem.split("="))
for elem in skrs:
    try:
        if elem[1][len(elem[1])-1] == "\n":
            skrytki[elem[0]] = elem[1][:-1]
        else:
            skrytki[elem[0]] = elem[1]
    except IndexError:
        try:
            skrytki[elem[0]] = elem[1]
        except IndexError:
            continue
del skrr, skrs
ekran = mmw.Screen()
znak = ''
BANNER = mmw.FormattedString('Sprawdzacz PZK. Autor: Maciek Marciniak SO5AM')
BG = mmw.FormattedString('$(b_blue)$(bright_white)')
PROMPT = mmw.FormattedString('$(b_cyan)Znak>')
PROMPT_WYCZ = mmw.FormattedString(BG.string +
                                  "$(b_gray)Znak>")
TRAF = mmw.FormattedString(BG.string+'\033[J\033[2K$(b_green)$(white)')
BRAK_TRAFIEN = mmw.FormattedString(BG.string +
                                   '\033[J\033[2K$(b_bright_yellow)$(black)'
                                   'Brak Trafień.')
TRAF_KLUB = mmw.FormattedString(BG.string +
                                '$(b_bright_magenta)$(bright_white)'
                                'Skrytka:')
NACISNIJ_ENTER = mmw.FormattedString(BG.string + "$(b_gray)[Naciśnij enter]")
SCREEN_WARN = mmw.FormattedString('$(b_red)$(bright_white)'
                                  'UWAGA: Screen nie respektuje '
                                  'CSI[2J i kodów koloru, a więc ten '
                                  'program nie będzie się poprawnie '
                                  'wyświetlał')
KONTROLA_ZADAN = mmw.FormattedString('$(b_red)$(bright_white)'
                                     'Rodzicem procesu nie jest powłoka, '
                                     'nie można uśpić procesu')
ADMIN = mmw.FormattedString('$(b_red)[A]')
ekran.setChar(BG.string, 0, 0)
ekran.clear()
wyczysc = False
DOMYSLNE_USTAWIENIA = {'MaksWynikow': 30, 'pozwalajNaUsypianie': False,
                       'dynWysz': True,
                       'pozwalajNaWyczyszczenie': False,
                       'trybCzyszczenia': 'backspace',
                       'hashHasla': 'N/A',
                       'czasAdmina': 0.1,
                       'adminDoWylogowania': False,
                       'pozwalajNaShutdown': True}
try:
    with open('ustawienia.json') as plk_ust:
        zawPlikuUst = plk_ust.readlines()
except FileNotFoundError:
    pass
try:
    USTAWIENIA = json.loads('\n'.join(zawPlikuUst))
    del zawPlikuUst
except (json.decoder.JSONDecodeError, NameError) as e:
    ans = 'n'
    if isinstance(e, NameError):
        ans = 't'
    else:
        print('[ERR] nie można załadować ustawień.')
        print('Czy chcesz aby je nadpisać?')
        ans = input('[T/n]')
    if ans.lower()[0] == 't':
        USTAWIENIA = DOMYSLNE_USTAWIENIA
        nzaw = json.dumps(USTAWIENIA, indent=2, sort_keys=True)
        with open('USTAWIENIA.json', 'w') as plk:
            plk.write(nzaw)
USTAWIENIA_temp = DOMYSLNE_USTAWIENIA.copy()
USTAWIENIA_temp.update(USTAWIENIA)
USTAWIENIA = USTAWIENIA_temp
del USTAWIENIA_temp
# USTAWIENIA['MaksWynikow'] = 30
if not isinstance(USTAWIENIA['MaksWynikow'], int):
    print('-'*80)
    print('[FATAL] [USTAWIENIA] MaksWynikow isdigit(): False')
    print('USTAWIENIA["MaksWynikow"] =', repr(USTAWIENIA['MaksWynikow']))
    print('^C - Wyjdź')
    while 1:
        pass


USTAWIENIA['trybCzyszczenia'] = 'backspace'
if 'trybCzyszczenia' in USTAWIENIA:
    if USTAWIENIA['trybCzyszczenia'] not in ['*', 'backspace']:
        ekran.setChar(mmw.FormattedString('Konfiguracja: $(red)Niewłaściwy '
                                          'tryb '
                                          'czyszczenia:$(yellow)'
                                          + USTAWIENIA['trybCzyszczenia']
                                          + '$(reset)'),
                      1, 1)
        ekran.setChar(NACISNIJ_ENTER, 1, 2)
        input()
        exit()

cname = open('/proc/'+str(os.getppid())+'/comm').read().replace('\x00', ' ')\
    .replace('\n', '').replace('\r', '')
if cname == 'screen':
    ekran.setChar(SCREEN_WARN.string, 0, 1)
    ekran.setChar(NACISNIJ_ENTER.string, 0, 2)
    input()
    ekran.clear()
listaShelli = open('/etc/shells', 'r').readlines()
listaShelli.pop(0)
for num, shell in enumerate(listaShelli):
    listaShelli[num] = shell.split('/')
trybAdmina = False
if USTAWIENIA['hashHasla'].lower() == 'n/a':
    ekran.clear()
    print('Wymagane jest ustawienie hasła admina')
    kupa = ''
    try:
        while 1:
            passwd = getpass.getpass('Wpisz nowe hasło admina>>')
            passwd2 = getpass.getpass('Potwierdź nowe hasło admina>>')
            if passwd == passwd2:
                hasher = hashlib.sha256()
                hasher.update(bytes(passwd, 'utf-8'))
                kupa = hasher.hexdigest()
                USTAWIENIA['hashHasla'] = kupa
                nzaw = json.dumps(USTAWIENIA, indent=2, sort_keys=True)
                with open('USTAWIENIA.json', 'w') as plk:
                    plk.write(nzaw)
                break
            else:
                print('Hasła nie są takie same.')
    except (KeyboardInterrupt, EOFError):
        print(mmw.FormattedString('$(reset)'))
        ekran.clear()
        print(mmw.FormattedString('$(reset)\n\nAnulowano$(reset)'))
        exit()
    ekran.clear()
SKROTY = mmw.FormattedString('$(b_cyan)\033[K$(b_gray)[F2]$(b_cyan) '
                             '$(b_gray)[Ctrl+R]'
                             '$(b_cyan) Czyść ')
SKR_ADMIN = mmw.FormattedString('$(b_gray)[F10]$(b_cyan) Tryb admina ')
SKR_WYLOGUJ = mmw.FormattedString('$(b_gray)[F10]$(b_cyan) Wyloguj ')
SKR_CMD = mmw.FormattedString('$(b_gray)[ENTER]$(b_cyan) $(b_gray)[TAB]'
                              '$(b_cyan) Wykonaj komende')
SKR_SZUKAJ = mmw.FormattedString('$(b_gray)[ENTER]$(b_cyan) $(b_gray)[TAB]'
                                 '$(b_cyan) Szukaj')
while __name__ == '__main__':
    ekran.setChar(BG.string+BANNER.string, 1, 1)
    ekran.setChar(SKROTY.string
                  + (SKR_WYLOGUJ.string if trybAdmina else SKR_ADMIN.string)
                  + (SKR_CMD.string if znak.startswith('/') else
                     (SKR_SZUKAJ.string if not USTAWIENIA['dynWysz'] else '')),
                  0, ekran.size[1])
    if (not wyczysc) or not USTAWIENIA['pozwalajNaWyczyszczenie']:
        if trybAdmina:
            ekran.setChar(ADMIN.string+PROMPT.string+' '+znak+BG.string,
                          1, 2)
        else:
            ekran.setChar(PROMPT.string+' '+znak+BG.string, 4, 2)
    else:
        if trybAdmina:
            ekran.setChar(ADMIN.string+PROMPT_WYCZ.string+' '+znak,
                          1, 2)
        else:
            ekran.setChar(PROMPT_WYCZ.string+' '+znak, 4, 2)
    ch = ekran.getChar()
    if wyczysc and USTAWIENIA['pozwalajNaWyczyszczenie']:
        wyczysc = False
        if znak == '':
            pass
        elif USTAWIENIA['trybCzyszczenia'] == '*':
            isSlash = False
            try:
                isSlash = znak[0] != '/'
            except IndexError:
                pass
            if not isSlash:
                znak = ch.upper() if ch.isprintable() and not ch.isspace()\
                    else ''
        elif USTAWIENIA['trybCzyszczenia'] == 'backspace':
            oldlen = len(znak)
            if ch == '\x7f':
                wyczysc = False
                znak = ''
                ekran.setChar(BG.string, 0, 0)
                ekran.setChar(PROMPT.string+' '+znak+BG.string+(' '*oldlen),
                              2, 2)
                print('\n\033[K'*(USTAWIENIA['MaksWynikow']+2))
            else:
                znak += ch.upper() if ch.isprintable() and \
                    not ch.isspace() else ''
                wyczysc = True
        continue
    elif ch == '\x1a':
        if USTAWIENIA['pozwalajNaUsypianie'] or trybAdmina:
            if cname == os.environ['SHELL'].split('/')[-1] or\
                    cname in listaShelli:
                ekran.setChar('\033[0m', 1, 1)
                ekran.clear()
                os.kill(os.getpid(), signal.SIGSTOP)
                ekran.setChar(BG.string, 1, 1)
                ekran.clear()
            else:
                ekran.clear()
                ekran.setChar(KONTROLA_ZADAN.string, 1, 1)
                ekran.setChar(NACISNIJ_ENTER.string, 1, 2)
                input()
                ekran.clear()
        else:
            ekran.clear()
            ekran.setChar('Polityka ustawień zabrania akcji: Usypianie', 1, 1)
            ekran.setChar(NACISNIJ_ENTER.string, 1, 2)
            while 1:
                ch = ekran.getChar()
                if ch in ['\n', '\r']:
                    break
            ekran.clear()
    elif ch == '\x12':  # ^R
        znak = ''
        ekran.setChar(BG.string, 0, 0)
        ekran.clear()
        continue
    elif ch == '\x0c':  # ^L
        ekran.setChar(BG.string, 0, 0)
        ekran.clear()
    elif ch == '\033':  # ESC
        ch2 = ekran.getChar()
        if ch2 == 'O':  # ..
            ch3 = ekran.getChar()
            if ch3 == 'Q':  # F2
                znak = ''
                ekran.setChar(BG.string, 0, 0)
                ekran.clear()
        if ch2 == '[':
            ch3 = ekran.getChar()
            if ch3 == '2':
                ch4 = ekran.getChar()
                if ch4 == '1':
                    ch5 = ekran.getChar()
                    if ch5 == '~':  # F10
                        ekran.clear()
                        ekran.setCur(0, 0)
                        if trybAdmina:
                            trybAdmina = False
                            print('Wylogowano')
                            input('[enter]')
                        else:
                            # print('Wpisz hasło admina>>', end=' ')
                            passwd = getpass.getpass('Wpisz hasło admina>>')
                            # ekran.clear()
                            hasher = hashlib.sha256()
                            hasher.update(bytes(passwd, 'utf-8'))
                            kupa = hasher.hexdigest()
                            if kupa == USTAWIENIA['hashHasla']:
                                trybAdmina = True
                                logoutTime = time.time()\
                                    + (USTAWIENIA['czasAdmina']*60)
                            else:
                                trybAdmina = False
                                print('Hasło nie poprawne')
                                input('[enter]')
                        ekran.clear()
            if ch3 == '[':
                ch4 = ekran.getChar()
                if ch4 == 'B':  # F2 alt
                    znak = ''
                    ekran.setChar(BG.string, 0, 0)
                    ekran.clear()
            else:
                key = mmw.decoding.decode(ch+ch2+ch3)
    elif ch in ['\t', '\n', '\r']:
        if znak.startswith(('/POMOC', '/HELP')):
            znak = ''
            ekran.clear()
            print(dedent('''
                    /POMOC
                        Opis: Wyświetla tę pomoc
                        Składnia: /POMOC
                        Aliasy: /HELP

                    /ZAMKNIJ
                        Opis: Zamknij komputer
                        Składnia: /ZAMKNIJ
                        Aliasy: SHUTDOWN, HALT, WYJDZ

                    /O
                        Opis: Wyświetl wszystkich członków oddziału
                        Składnia: /O <Oddział>

                    /AKT
                        Wymagany Admin
                        Opis: Aktualizuj OSEC
                        Składnia: /AKT

                    /KONFIG
                        Wymagany Admin
                        Opis: Edytuj konfiguracje
                        Składnia: /KONFIG'''))
            input('[Enter]')
            ekran.clear()
        if znak.startswith(('/WYJDZ', '/SHUTDOWN', '/HALT', '/ZAMKNIJ')):
            if USTAWIENIA['pozwalajNaShutdown']:
                proc = subprocess.Popen('sudo shutdown -h now')
                exit()
        if znak.startswith('/O'):
            try:
                trafienia = 0
                ekran.setChar(BG.string, 0, 0)
                ekran.clear()
                # print(znak[3:])
                # input('.')
                print('\033[1;'+str(ekran.size[1]-2)+'r')
                num = 0
                listTraf = []
                for i in pzk:
                    num += 1
                    if pzk[i] == znak[3:] or pzk[i] == '0'+znak[3:]:
                        ekran.setChar(BG.string+i+'\n', 1, ekran.size[1]-2)
                        listTraf.append(i)
                        trafienia += 1
                    procent = format(num/len(pzk.keys())*100, '.0f')
                    ekran.setChar(BG.string+'Przeszukiwanie... ('+str(num)
                                  + ' / '
                                  + str(len(pzk.keys()))
                                  + ' '
                                  + procent+'%)\n',
                                  1, ekran.size[1]-1)
                    time.sleep(0.0003125)
                print('Znaleziono', trafienia, 'wyników')
                # input('[Naciśnij Enter, aby wrócic]')
                print('\033[r')
                ekran.clear()  # Żeby na less'sie nie wyświetlał się tekst
                createProc = subprocess.Popen('mkfifo wynikiWyszukiwania.txt',
                                              shell=True)
                createProc.wait(timeout=3)

                proc = subprocess.Popen('less -f wynikiWyszukiwania.txt',
                                        shell=True)

                tfile = open('wynikiWyszukiwania.txt', 'w')
                for trafienie in sorted(listTraf):
                    tfile.write(trafienie+'\n')
                tfile.close()
                proc.wait()
                ekran.clear()
                # ^^ Żeby less nie wyświetlał się na głównym ekranie
            except KeyboardInterrupt:
                pass
            znak = ''
        if znak.startswith('/AKT'):
            znak = ''
            if not trybAdmina:
                ekran.clear()
                ekran.setCur(0, 0)
                print('Nie można zaktualizować plików z OSECu: '
                      'nie jesteś w trybie admina')
                input('[enter]')
                ekran.clear()
            else:
                print(mmw.FormattedString('$(reset)'))
                ekran.clear()
                print('Uruchamianie skryptu...')
                proc = subprocess.Popen('./aktualizujOSEC.sh',
                                        shell=True)
                while True:
                    if proc.poll() is not None:
                        break
                print('-'*80)
                print('Skrypt zakończony.')
                print('Wymagany jest restart, aby zatwierdzić zmiany')
                print('Naciśnij enter aby wyjść.')
                print('Wciśnij control+c aby anulować')
                try:
                    input('[ENTER || Ctrl+C]')
                    exit()
                except (KeyboardInterrupt, EOFError):
                    pass
        if znak.startswith('/KONFIG'):
            if not trybAdmina:
                ekran.clear()
                ekran.setCur(0, 0)
                print('Nie można edytować konfiguracji: '
                      'nie jesteś w trybie admina')
                input('[enter]')
            else:
                proc = subprocess.Popen('sensible-editor USTAWIENIA.json',
                                        shell=True)
                while True:
                    if proc.poll() is not None:
                        break
                with open('USTAWIENIA.json', 'r') as plk:
                    zaw = plk.readlines()
                    USTAWIENIA = json.loads(''.join(zaw))
            ekran.setChar(BG.string, 0, 0)
            ekran.clear()
            znak = ''
    elif ch == '\x7f':
        znak = znak[:-1]
        ekran.setChar(BG.string, 0, 0)
        print('\033[2;0H\033[K\n\033[K')
    elif ch == '\x03':
        try:
            if USTAWIENIA['adminDoWylogowania']:
                if not trybAdmina:
                    ekran.clear()
                    ekran.setCur(0, 0)
                    print('Nie można wyjść: wymagane są uprawnienia admina')
                    input('[enter]')
                    # ekran.clear()
                else:
                    exit()
            else:
                exit()
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            ekran.clear()
    elif ch.isprintable():
        znak += ch.upper()
    else:
        ekran.setChar(mmw.FormattedString('$(b_red)$(bright_white)Znak?'
                                          + repr(ch)).string
                      + BG.string, 1, 3)
    if znak.startswith('/'):
        komendy = ['/KONFIG',
                   '/AKT',
                   '/O <ODDZIAŁ>',
                   '/WYJDZ',
                   'Ukryto 3 aliasy (wpisz /POMOC aby je zobaczyć.)']
        # subkomendy = {'/U': ['/U PNW', '/U MTR', '/U DYN', '/U TRC'],
        #               '/O': ['<ODDZIAŁ>']}
        podpowiedzi = ""
        trafienia = 0
        if znak not in komendy:
            for i in komendy:
                if znak in i:
                    podpowiedzi += '\n'+BG.string+'\033[K'+TRAF.string+i
                    trafienia += 1
                if trafienia >= USTAWIENIA['MaksWynikow']:
                    break
        ekran.setChar(podpowiedzi, 1, 3)

    elif ch == '\r' or ch == '\n' or USTAWIENIA['dynWysz']:
        trafienia = 0
        ostat_traf = ''
        sznak = znak.split('/')
        # print(sznak)
        # input('....')
        wyniki = []
        try:
            sznakinskrytki = sznak[1] in skrytki
        except IndexError:
            sznakinskrytki = False
        lt = []  # Lista Trafień
        for i in pzk:
            try:
                if (not sznak[1].isalpha()) and (sznak[1] not in ['MM', 'AM'
                                                                  'M', 'P',
                                                                  'D', 'QRP',
                                                                  '']):
                    sznakini = sznak[1] in i
                else:
                    sznakini = sznak[0] in i
            except IndexError:
                sznakini = False
            if znak in i or sznakini:
                if i in skrytki:
                    lt.append(TRAF.string+i+' '+pzk[i]+' ' +
                              TRAF_KLUB.string +
                              skrytki[i])
                    # ekran.setChar(TRAF.string+i+' '+pzk[i]+' ' +
                    #           TRAF_KLUB.string +
                    #           skrytki[i], 1, 4+trafienia)
                elif sznakinskrytki:
                    lt.append(TRAF.string+i+' '+pzk[i]+' ' +
                              TRAF_KLUB.string +
                              skrytki[sznak[1]])
                    # ekran.setChar(TRAF.string+i+' '+pzk[i]+' ' +
                    #           TRAF_KLUB.string +
                    #           skrytki[sznak[1]], 1, 4+trafienia)
                else:
                    lt.append(TRAF.string+i+' '+pzk[i])
                    # ekran.setChar(TRAF.string+i+' '+pzk[i], 1, 4+trafienia)
                trafienia += 1
                ostat_traf = i
                if trafienia >= USTAWIENIA['MaksWynikow']:
                    break
        trafstr = ""
        for num, i in enumerate(lt):
            if num >= ekran.size[1]-4:
                break
            trafstr += i+"\n"
        ekran.setChar(trafstr+BG.string+"\033[K", 1, 4, flush=False)
        if znak in skrytki:
            ekran.setChar(TRAF_KLUB.string+' '+skrytki[znak], 1, 3,
                          flush=False)
        try:
            if sznak[1] in skrytki:
                ekran.setChar(TRAF_KLUB.string+' '+skrytki[sznak[1]], 1, 3,
                              flush=False)
        except IndexError:
            pass
        if trafienia == 0:
            ekran.setChar(BRAK_TRAFIEN.string, 1, 3, flush=False)
        if trafienia == 1:
            if ostat_traf in skrytki:
                ekran.setChar(TRAF_KLUB.string+' '+skrytki[ostat_traf], 1, 3,
                              flush=False)
            wyczysc = True
        # print('', end='', flush=True)
