import time  # NOQA
import subprocess
import os
import signal
import json
import getpass
import hashlib
try:
    import mmw
except ImportError as e:
    print('mmw:', e)
    print('Nie można zaimportować mmw3.py.')
    print('Wciśnij Ctrl C aby się zatrzymać ten program, i się wylogować.')
    print('.... prawdopodobnie')
    while 1:
        pass


def recode_file(name, encodingFrom='Latin2'):
    f = open(name, 'r', encoding=encodingFrom)
    lines = []
    num = 0
    while 1:
        num += 1
        line = f.readline()
        if line == "":
            break
        lines.append(line)
        print('\033[A\033[2KPrzeczytano linię', num, '/ ?')
    print('\033[A\033[2KPrzeczytano', num, 'linii\n')
    f.close()
    f = open(name, 'w')
    for num, line in enumerate(lines):
        f.write(line)
        procent = format(num/len(lines)*100, '.0f')
        print('\033[A\033[2KZapisywanie linii', num, '/', len(lines),
              str(procent)+"%")
    print('\033[A\033[2KZapisano', len(lines), 'linii')
    print('['+name+']: Plik Przekodowany\n')


def recode():
    print('Przekodowano 0/2')
    recode_file('osec_pzk.txt')
    print('Przekodowano 1/2')
    recode_file('osec_kluby.txt')
    print('Przekodowano 2/2')
    time.sleep(1)


print('\n')
try:
    f = open('osec_pzk.txt', 'r')
    lines = f.readlines()
    lines.pop(0)
    f2 = open('osec_kluby.txt', 'r')
    kluby = f2.readlines()
    kluby.pop(0)
except UnicodeDecodeError:
    recode()
    f = open('osec_pzk.txt', 'r')
    lines = f.readlines()
    lines.pop(0)
    f2 = open('osec_kluby.txt', 'r')
    kluby = f2.readlines()
    kluby.pop(0)
newlines = []
nowekluby = []
for num, line in enumerate(lines):
    procent = format(num/len(lines)*100, '.0f')
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(lines), '(' +
          str(procent)+'%')
    newline = line
    while '  ' in newline:  # Dwie spacje som w tym stringu
        newline = newline.replace('  ', ' ')
    newlines.append(newline[:-1])

for num, line in enumerate(kluby):
    procent = format(num/len(lines)*100, '.0f')
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(kluby), '(' +
          str(procent)+'%')
    newline = line
    while '  ' in newline:
        newline = newline.replace('  ', ' ')
    nowekluby.append(newline[:-1])
print('\033[A\033[2K(PZK)Usunięto spacje w', len(newlines), 'liniach')
print('(KLUBY)Usunięto spacje w', len(nowekluby), 'liniach')
lines = newlines
newlines = []
kluby = nowekluby
nowekluby = []
print()
for num, line in enumerate(lines):
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(lines))
    newline = line
    newlines.extend(line.split(' ') if 'oddział' not in line.lower() else
                    [line])
kluby_fin = {}
for num, line in enumerate(kluby):
    spl = line.split(' ')
    for snum in range(1, len(spl), 2):
        try:
            part = spl[snum]
        except IndexError:
            continue
        if part not in ['KLUBY', 'INNE', 'ZNAKI']:
            try:
                kluby_fin[part] = spl[snum+1]
            except Exception:
                continue
lines = newlines
newlines = []
for num, line in enumerate(lines):
    if line != '':
        newlines.append(line)
lines = newlines
newlines = []
oddzial = ''
przet_odzialy = []
pzk = {}
pzk.update(kluby_fin)
print()
for num, line in enumerate(lines):
    if line[0] == ' ':
        przet_odzialy.append(oddzial+'')
        oddzial = line.split(' ')[2]
        print('\033[2A\033[2KPrzetworzone oddziły:', ' '.join(przet_odzialy))
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
for i in range(len(skrl)):
        skrs.append(skrl[i].split("="))
for i in range(len(skrs)):
        try:
            if skrs[i][1][len(skrs[i][1])-1] == "\n":
                skrytki[skrs[i][0]] = skrs[i][1][:-1]
            else:
                skrytki[skrs[i][0]] = skrs[i][1]
        except Exception:
            try:
                skrytki[skrs[i][0]] = skrs[i][1]
            except IndexError:
                continue
del skrr, skrs
s = mmw.Screen()
znak = ''
nazwa = mmw.FormattedString('Sprawdzacz PZK. Autor: Maciek Marciniak SO5AM')
bg = mmw.FormattedString('$(b_blue)$(bright_white)')
prompt = mmw.FormattedString('$(b_cyan)Znak>')
traf = mmw.FormattedString(bg.string+'\033[J\033[2K$(b_green)$(white)')
brakTrafien = mmw.FormattedString(bg.string +
                                  '\033[J\033[2K$(b_bright_yellow)$(black)'
                                  'Brak Trafień.')
traf_klub = mmw.FormattedString(bg.string +
                                '$(b_bright_magenta)$(bright_white)'
                                'Skrytka:')
znakWyczyszczenie = mmw.FormattedString(bg.string +
                                        "$(b_gray)Znak>")
nacisnijEnter = mmw.FormattedString(bg.string + "$(b_gray)[Naciśnij enter]")
screenwarn = mmw.FormattedString('$(b_red)$(bright_white)'
                                 'UWAGA: Screen nie respektuje '
                                 'CSI[2J i kodów koloru, a więc ten '
                                 'program nie będzie się poprawnie '
                                 'wyświetlał')
brakKontroliZadan = mmw.FormattedString('$(b_red)$(bright_white)'
                                        'Rodzicem procesu nie jest powłoka, '
                                        'nie można uśpić procesu')
adminStr = mmw.FormattedString('$(b_red)[A]')
s.setChar(bg.string, 0, 0)
s.clear()
wyczysc = False
try:
    with open('ustawienia.json') as plk:
        zawPlikuUst = plk.readlines()
except FileNotFoundError:
    pass
try:
    ustawienia = json.loads('\n'.join(zawPlikuUst))
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
        ustawienia = {'MaksWynikow': 30, 'pozwalajNaUsypianie': False,
                      'dynWysz': True,
                      'pozwalajNaWyczyszczenie': True,
                      'trybCzyszczenia': 'backspace',
                      'hashHasla': 'N/A',
                      'czasAdmina': 0.1,
                      'adminDoWylogowania': False}
        nzaw = json.dumps(ustawienia, indent=2, sort_keys=True)
        with open('ustawienia.json', 'w') as plk:
            plk.write(nzaw)
# ustawienia['MaksWynikow'] = 30
if not isinstance(ustawienia['MaksWynikow'], int):
        print('-'*80)
        print('[FATAL] [ustawienia] MaksWynikow isdigit(): False')
        print('ustawienia["MaksWynikow"] =', repr(ustawienia['MaksWynikow']))
        print('^C - Wyjdź')
        while 1:
            pass


ustawienia['trybCzyszczenia'] = 'backspace'
if 'trybCzyszczenia' in ustawienia:
    if ustawienia['trybCzyszczenia'] not in ['*', 'backspace']:
        s.setChar(mmw.FormattedString(
                 'Konfiguracja: $(red)Niewłaściwy tryb czyszczenia:$(yellow)'
                  + ustawienia['trybCzyszczenia'] + '$(reset)'), 1, 1)
        s.setChar(nacisnijEnter, 1, 2)
        input()
        exit()

cname = open('/proc/'+str(os.getppid())+'/comm').read().replace('\x00', ' ')\
    .replace('\n', '').replace('\r', '')
if cname == 'screen':
    s.setChar(screenwarn.string, 0, 1)
    s.setChar(nacisnijEnter.string, 0, 2)
    input()
    s.clear()
listaShelli = open('/etc/shells', 'r').readlines()
listaShelli.pop(0)
for num, shell in enumerate(listaShelli):
    listaShelli[num] = shell.split('/')
trybAdmina = False
if ustawienia['hashHasla'].lower() == 'n/a':
    s.clear()
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
                ustawienia['hashHasla'] = kupa
                nzaw = json.dumps(ustawienia, indent=2, sort_keys=True)
                with open('ustawienia.json', 'w') as plk:
                    plk.write(nzaw)
                break
            else:
                print('Hasła nie są takie same.')
    except (KeyboardInterrupt, EOFError):
        print(mmw.FormattedString('$(reset)'))
        s.clear()
        print(mmw.FormattedString('$(reset)\n\nAnulowano$(reset)'))
        exit()
    s.clear()
skrotyStr = mmw.FormattedString('$(b_cyan)\033[K$(b_gray)[F2]$(b_cyan) '
                                '$(b_gray)[Ctrl+R]'
                                '$(b_cyan) Czyść ')
skr_admin = mmw.FormattedString('$(b_gray)[F10]$(b_cyan) Tryb admina ')
skr_wyloguj = mmw.FormattedString('$(b_gray)[F10]$(b_cyan) Wyloguj ')
skr_cmd = mmw.FormattedString('$(b_gray)[ENTER]$(b_cyan) $(b_gray)[TAB]'
                              '$(b_cyan) Wykonaj komende')
skr_szukaj = mmw.FormattedString('$(b_gray)[ENTER]$(b_cyan) $(b_gray)[TAB]'
                                 '$(b_cyan) Szukaj')
while __name__ == '__main__':
    s.setChar(bg.string+nazwa.string, 1, 1)
    s.setChar(skrotyStr.string
              + (skr_wyloguj.string if trybAdmina else skr_admin.string)
              + (skr_cmd.string if znak.startswith('/') else
                 (skr_szukaj.string if not ustawienia['dynWysz'] else '')),
              0, s.size[1])
    if (not wyczysc) or not ustawienia['pozwalajNaWyczyszczenie']:
        if trybAdmina:
            s.setChar(adminStr.string+prompt.string+' '+znak+bg.string, 1, 2)
        else:
            s.setChar(prompt.string+' '+znak+bg.string, 4, 2)
    else:
        if trybAdmina:
            s.setChar(adminStr.string+znakWyczyszczenie.string+' '+znak, 1, 2)
        else:
            s.setChar(znakWyczyszczenie.string+' '+znak, 4, 2)
    ch = s.getChar()
    if wyczysc and ustawienia['pozwalajNaWyczyszczenie']:
        wyczysc = False
        if znak == '':
            pass
        elif ustawienia['trybCzyszczenia'] == '*':
            isSlash = False
            try:
                isSlash = znak[0] != '/'
            except IndexError:
                pass
            if not isSlash:
                znak = ch.upper() if ch.isprintable() and not ch.isspace()\
                    else ''
        elif ustawienia['trybCzyszczenia'] == 'backspace':
            oldlen = len(znak)
            if ch == '\x7f':
                wyczysc = False
                znak = ''
                s.setChar(bg.string, 0, 0)
                s.setChar(prompt.string+' '+znak+bg.string+(' '*oldlen), 2, 2)
                print('\n\033[K'*(ustawienia['MaksWynikow']+2))
            else:
                znak += ch.upper() if ch.isprintable() and \
                    not ch.isspace() else ''
                wyczysc = True
        continue
    elif ch == '\x1a':
        if ustawienia['pozwalajNaUsypianie'] or trybAdmina:
            if cname == os.environ['SHELL'].split('/')[-1] or\
                    cname in listaShelli:
                s.setChar('\033[0m', 1, 1)
                s.clear()
                os.kill(os.getpid(), signal.SIGSTOP)
                s.setChar(bg.string, 1, 1)
                s.clear()
            else:
                s.clear()
                s.setChar(brakKontroliZadan.string, 1, 1)
                s.setChar(nacisnijEnter.string, 1, 2)
                input()
                s.clear()
        else:
            s.clear()
            s.setChar('Polityka ustawień zabrania akcji: Usypianie', 1, 1)
            s.setChar(nacisnijEnter.string, 1, 2)
            while 1:
                ch = s.getChar()
                if ch == '\n' or ch == '\r':
                    break
            s.clear()
    elif ch == '\x12':  # ^R
        znak = ''
        s.setChar(bg.string, 0, 0)
        s.clear()
        continue
    elif ch == '\x0c':  # ^L
        s.setChar(bg.string, 0, 0)
        s.clear()
    elif ch == '\033':  # ESC
        ch2 = s.getChar()
        if ch2 == 'O':  # ..
            ch3 = s.getChar()
            if ch3 == 'Q':  # F2
                znak = ''
                s.setChar(bg.string, 0, 0)
                s.clear()
        if ch2 == '[':
            ch3 = s.getChar()
            if ch3 == '2':
                ch4 = s.getChar()
                if ch4 == '1':
                    ch5 = s.getChar()
                    if ch5 == '~':  # F10
                        s.clear()
                        s.setCur(0, 0)
                        if trybAdmina:
                            trybAdmina = False
                            print('Wylogowano')
                            input('[enter]')
                        else:
                            # print('Wpisz hasło admina>>', end=' ')
                            passwd = getpass.getpass('Wpisz hasło admina>>')
                            # s.clear()
                            hasher = hashlib.sha256()
                            hasher.update(bytes(passwd, 'utf-8'))
                            kupa = hasher.hexdigest()
                            if kupa == ustawienia['hashHasla']:
                                trybAdmina = True
                                logoutTime = time.time()\
                                    + (ustawienia['czasAdmina']*60)
                            else:
                                trybAdmina = False
                                print('Hasło nie poprawne')
                                input('[enter]')
                        s.clear()
            if ch3 == '[':
                ch4 = s.getChar()
                if ch4 == 'B':  # F2 alt
                    znak = ''
                    s.setChar(bg.string, 0, 0)
                    s.clear()
            else:
                key = mmw.decoding.decode(ch+ch2+ch3)
    elif ch == '\t' or ch == '\n' or ch == '\r':
        if znak.startswith('/O'):
            try:
                trafienia = 0
                s.setChar(bg.string, 0, 0)
                s.clear()
                # print(znak[3:])
                # input('.')
                print('\033[1;'+str(s.size[1]-2)+'r')
                num = 0
                listTraf = []
                for i in pzk.keys():
                    num += 1
                    if pzk[i] == znak[3:]:
                        s.setChar(bg.string+i+'\n', 1, s.size[1]-2)
                        listTraf.append(i)
                        trafienia += 1
                    procent = format(num/len(pzk.keys())*100, '.0f')
                    s.setChar(bg.string+'Przeszukiwanie... ('+str(num)+' / ' +
                              str(len(pzk.keys()))+' ' +
                              procent+'%)\n',
                              1, s.size[1]-1)
                    time.sleep(0.0003125)
                print('Znaleziono', trafienia, 'wyników')
                # input('[Naciśnij Enter, aby wrócic]')
                print('\033[r')
                s.clear()  # Żeby na less'sie nie wyświetlał się tekst
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
                s.clear()  # Żeby less nie wyświetlał się na głównym ekranie
            except KeyboardInterrupt:
                pass
            znak = ''
        if znak.startswith('/AKT'):
            znak = ''
            if not trybAdmina:
                s.clear()
                s.setCur(0, 0)
                print('Nie można zaktualizować plików z OSECu: '
                      'nie jesteś w trybie admina')
                input('[enter]')
                s.clear()
            else:
                print(mmw.FormattedString('$(reset)'))
                s.clear()
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
                try:
                    input('[ENTER || Ctrl+C]')
                    exit()
                except (KeyboardInterrupt, EOFError):
                    pass
        if znak.startswith('/KONFIG'):
            if not trybAdmina:
                s.clear()
                s.setCur(0, 0)
                print('Nie można edytować konfiguracji: '
                      'nie jesteś w trybie admina')
                input('[enter]')
            else:
                proc = subprocess.Popen('sensible-editor ustawienia.json',
                                        shell=True)
                while True:
                    if proc.poll() is not None:
                        break
                with open('ustawienia.json', 'r') as plk:
                    zaw = plk.readlines()
                    ustawienia = json.loads(''.join(zaw))
            s.setChar(bg.string, 0, 0)
            s.clear()
            znak = ''
    elif ch == '\x7f':
        znak = znak[:-1]
        s.setChar(bg.string, 0, 0)
        print('\033[2;0H\033[K\n\033[K')
    elif ch == '\x03':
        try:
            if ustawienia['adminDoWylogowania']:
                if not trybAdmina:
                    s.clear()
                    s.setCur(0, 0)
                    print('Nie można wyjść: wymagane są uprawnienia admina')
                    input('[enter]')
                    # s.clear()
                else:
                    exit()
            else:
                exit()
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            s.clear()
    elif ch.isprintable():
        znak += ch.upper()
    else:
        s.setChar(mmw.FormattedString('$(b_red)$(bright_white)Znak?' +
                                      repr(ch)).string +
                  bg.string, 1, 3)
    if znak.startswith('/'):
        komendy = ['/KONFIG',
                   '/AKT',
                   '/O <ODDZIAŁ>']
        # subkomendy = {'/U': ['/U PNW', '/U MTR', '/U DYN', '/U TRC'],
        #               '/O': ['<ODDZIAŁ>']}
        podpowiedzi = ""
        trafienia = 0
        if znak not in komendy:
            for i in komendy:
                if znak in i:
                    podpowiedzi += '\n'+bg.string+'\033[K'+traf.string+i
                    trafienia += 1
                if trafienia >= ustawienia['MaksWynikow']:
                    break
        s.setChar(podpowiedzi, 1, 3)

    elif ch == '\r' or ch == '\n' or ustawienia['dynWysz']:
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
        for i in pzk.keys():
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
                    lt.append(traf.string+i+' '+pzk[i]+' ' +
                              traf_klub.string +
                              skrytki[i])
                    # s.setChar(traf.string+i+' '+pzk[i]+' ' +
                    #           traf_klub.string +
                    #           skrytki[i], 1, 4+trafienia)
                elif sznakinskrytki:
                    lt.append(traf.string+i+' '+pzk[i]+' ' +
                              traf_klub.string +
                              skrytki[sznak[1]])
                    # s.setChar(traf.string+i+' '+pzk[i]+' ' +
                    #           traf_klub.string +
                    #           skrytki[sznak[1]], 1, 4+trafienia)
                else:
                    lt.append(traf.string+i+' '+pzk[i])
                    # s.setChar(traf.string+i+' '+pzk[i], 1, 4+trafienia)
                trafienia += 1
                ostat_traf = i
                if trafienia >= ustawienia['MaksWynikow']:
                    break
        trafstr = ""
        for num, i in enumerate(lt):
            if num >= s.size[1]-4:
                break
            trafstr += i+"\n"
        s.setChar(trafstr+bg.string+"\033[K", 1, 4, flush=False)
        if znak in skrytki:
            s.setChar(traf_klub.string+' '+skrytki[znak], 1, 3,
                      flush=False)
        try:
            if sznak[1] in skrytki:
                s.setChar(traf_klub.string+' '+skrytki[sznak[1]], 1, 3,
                          flush=False)
        except IndexError:
            pass
        if trafienia == 0:
            s.setChar(brakTrafien.string, 1, 3, flush=False)
        if trafienia == 1:
            if ostat_traf in skrytki:
                s.setChar(traf_klub.string+' '+skrytki[ostat_traf], 1, 3,
                          flush=False)
            wyczysc = True
        # print('', end='', flush=True)
