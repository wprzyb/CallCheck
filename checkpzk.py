import time  # NOQA
import subprocess
try:
    import mmw3 as mmw
except ImportError:
    print('Nie można zaimportować mmw3.py.')
    print('Wciśnij Ctrl C aby się zatrzymać ten program, i się wylogować.')
    while 1:
        pass


def recode():
    f = open('osec_pzk.txt', 'r', encoding='Latin2')
    f2 = open('osec_kluby.txt', 'r', encoding='Latin2')
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
    f = open('osec_pzk.txt', 'w')
    for num, line in enumerate(lines):
        f.write(line)
        print('\033[A\033[2KZapisywanie linii', num, '/', len(lines))
    print('\033[A\033[2KZapisano', len(lines), 'linii')
    print('Plik Przekodowany\n')

    lines = []
    num = 0
    while 1:
        num += 1
        line = f2.readline()
        if line == "":
            break
        lines.append(line)
        print('\033[A\033[2KPrzeczytano linię', num, '/ ?')
    print('\033[A\033[2KPrzeczytano', num, 'linii\n')
    f2.close()
    f2 = open('osec_kluby.txt', 'w')
    for num, line in enumerate(lines):
        f2.write(line)
        print('\033[A\033[2KZapisywanie linii', num, '/', len(lines))
    print('\033[A\033[2KZapisano', len(lines), 'linii')
    print('Plik Przekodowany\n')


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
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(lines))
    newline = line
    while '  ' in newline:
        newline = newline.replace('  ', ' ')
        # print('\033[A\033[2K', newline)
    newlines.append(newline[:-1])

for num, line in enumerate(kluby):
    print('\033[A\033[2KKonwertowanie linii', num, '/', len(kluby))
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
znak = ''
s.setChar(bg.string, 0, 0)
s.clear()
wyczysc = False

plikUstawien = open('ustawienia.txt', 'r')
zawPlikuUst = plikUstawien.readlines()
ustawienia = {}
zPUS = []
for i in range(len(zawPlikuUst)):
        zPUS.append(zawPlikuUst[i].split("="))
for i in range(len(zPUS)):
        try:
            if zPUS[i][1][len(zPUS[i][1])-1] == "\n":
                ustawienia[zPUS[i][0]] = zPUS[i][1][:-1]
            else:
                ustawienia[zPUS[i][0]] = zPUS[i][1]
        except Exception:
            try:
                ustawienia[zPUS[i][0]] = zPUS[i][1]
            except IndexError:
                continue
del zPUS, zawPlikuUst
maxtrafien = 30
if 'MaksWynikow' in ustawienia:
    print(repr(ustawienia['MaksWynikow']))
    if ustawienia['MaksWynikow'].isdigit():
        maxtrafien = int(ustawienia['MaksWynikow'])
    else:
        print('[WARN] [ustawienia] MaksWynikow isdigit(): False')
        time.sleep(1)

dynSearch = True
if 'DynamiczneWyszukiwanie' in ustawienia:
    dynSearch = True if ustawienia['DynamiczneWyszukiwanie'] == "T" else False

trybCzyszczenia = ustawienia['trybCzyszczenia'] if 'trybCzyszczenia' in\
    ustawienia else 'b'
pozwalajNaWyczyszczenie = False
if 'pozwalajNaWyczyszczenie' in ustawienia:
    pozwalajNaWyczyszczenie = True if \
        ustawienia['pozwalajNaWyczyszczenie'] == "T" else False

menu = mmw.Menu("Ustawienia")
# popup.parent = s
log = open('log.txt', 'w')
while __name__ == '__main__':
    s.setChar(bg.string+nazwa.string, 1, 1)
    if (not wyczysc) or not pozwalajNaWyczyszczenie:
        s.setChar(prompt.string+' '+znak+bg.string, 2, 2)
    else:
        s.setChar(znakWyczyszczenie.string+' '+znak, 2, 2)
    ch = s.getChar()

    if wyczysc and pozwalajNaWyczyszczenie:
        wyczysc = False
        if trybCzyszczenia == '*':
            isSlash = False
            try:
                isSlash = znak[0] != '/'
            except IndexError:
                pass
            if not isSlash:
                znak = ch.upper() if ch.isprintable() and not ch.isspace()\
                    else ''
        elif trybCzyszczenia == 'backspace':
            if ch == '\x7f':
                wyczysc = False
                znak = ''
            else:
                znak += ch.upper() if ch.isprintable() and \
                    not ch.isspace() else ''
                wyczysc = True
        s.setChar(bg.string, 0, 0)
        s.clear()
        continue
    elif ch == '\x12':
        znak = ''
        s.setChar(bg.string, 0, 0)
        s.clear()
        continue
    elif ch == '\x0c':
        s.setChar(bg.string, 0, 0)
        s.clear()
    elif ch == '\033':
        ch2 = s.getChar()
        if ch2 == '[':
            ch3 = s.getChar()
            key = mmw.KeyMap.decode(ch+ch2+ch3)
            # print(key)
    elif ch == '\t' or ch == '\n' or ch == '\r':
        if len(znak) > 3:
            if znak[0:2] == '/O':
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
                    if pzk[i] == znak[2:]:
                        s.setChar(bg.string+i+'\n', 1, s.size[1]-2)
                        listTraf.append(i)
                        trafienia += 1
                    s.setChar(bg.string+'Przeszukiwanie... ('+str(num)+' / ' +
                              str(len(pzk.keys()))+')\n', 1, s.size[1]-1)
                    # time.sleep(0.00125)
                print('Znaleziono', trafienia, 'wyników')
                # input('[Naciśnij Enter, aby wrócic]')
                print('\033[r')
                s.clear()  # Żeby na less'sie nie wyświetlał się tekst
                proc = subprocess.Popen('less -f wynikiWyszukiwania.txt',
                                        shell=True)

                tfile = open('wynikiWyszukiwania.txt', 'w')
                for trafienie in sorted(listTraf):
                    tfile.write(trafienie+'\n')
                tfile.close()
                proc.wait()
                s.clear()  # Żeby less nie wyświetlał się na głównym ekranie
                znak = ''
        if len(znak) > 7:
            if znak[0:2] == '/U':
                ustZmien = False
                if znak[3:6] == 'PNW':
                    if znak[7] == "N":
                        pozwalajNaWyczyszczenie = False
                        ustZmien = True
                    elif znak[7] == 'T':
                        pozwalajNaWyczyszczenie = True
                        ustZmien = True
                elif znak[3:6] == 'MTR':
                    if znak[7:].isalnum():
                        maxtrafien = int(znak[7:])
                        ustZmien = True

                elif znak[3:6] == 'DYN':
                    if znak[7] == "N":
                        dynSearch = False
                        ustZmien = True
                    elif znak[7] == 'T':
                        dynSearch = True
                        ustZmien = True
                elif znak[3:6] == 'TRC':
                    if znak[7] == '*':
                        trybCzyszczenia = '*'
                        ustZmien = True
                    if znak[7] == 'B':
                        trybCzyszczenia = 'backspace'
                        ustZmien = True
                s.setChar(bg.string, 0, 0)
                s.clear()
                if ustZmien:
                    print('Ustawienie('+znak[3:6]+') zmienione na '+znak[7:])
                    input('[Naciśnij enter]')
                    s.setChar(bg.string, 0, 0)
                    s.clear()
                znak = ''
    elif ch == '\x7f':
        znak = znak[:-1]
        s.setChar(bg.string, 0, 0)
        s.clear()
    elif ch == '\x03':
        log.close()
        exit(0)
    elif ch.isprintable():
        znak += ch.upper()
    else:
        s.setChar(mmw.FormattedString('$(b_red)$(bright_white)Znak?' +
                                      repr(ch)).string +
                  bg.string, 1, 3)
    if ch == '\r' or ch == '\n' or dynSearch:
        trafienia = 0
        ostat_traf = ''
        sznak = znak.split('/')
        # print(sznak)
        # input('....')
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
                try:
                    sznakinskrytki = sznak[1] in skrytki
                except IndexError:
                    sznakinskrytki = False
                if i in skrytki:
                    s.setChar(traf.string+i+' '+pzk[i]+' '+traf_klub.string +
                              skrytki[i], 1, 4+trafienia)
                elif sznakinskrytki:
                    s.setChar(traf.string+i+' '+pzk[i]+' '+traf_klub.string +
                              skrytki[sznak[1]], 1, 4+trafienia)
                else:
                    s.setChar(traf.string+i+' '+pzk[i], 1, 4+trafienia)
                trafienia += 1
                ostat_traf = i
                if trafienia >= maxtrafien:
                    break
        if znak in skrytki:
            s.setChar(traf_klub.string+' '+skrytki[znak], 1, 3)
        try:
            if sznak[1] in skrytki:
                s.setChar(traf_klub.string+' '+skrytki[sznak[1]], 1, 3)
        except IndexError:
            pass
        if trafienia == 0:
            s.setChar(brakTrafien.string, 1, 3)
        if trafienia == 1:
            if ostat_traf in skrytki:
                s.setChar(traf_klub.string+' '+skrytki[ostat_traf], 1, 3)
            wyczysc = True
