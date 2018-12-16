import sys
import re
from collections import Counter

def composer(filePath):
    ctr = Counter()
    for line in open(filePath, 'r', encoding='UTF8'):
        r = re.compile( r"Composer: (.*)" )
        m = r.match(line)
        if m:
            s = m.group(1).split(';')
            for composer in (s):
                something = composer.split('(')
                cleared = something[0].strip()
                if not cleared:
                    continue
                ctr[cleared] += 1
    for k in ctr:
        print(k + ": " + str(ctr[k]))

def century(filePath):
    ctr = Counter()
    for line in open(filePath, 'r', encoding='UTF8'):
        r = re.compile( r"Composition Year: (.*)" )
        m = r.match(line)
        if m:
            century = m.group(1)
            r = re.compile( "(.*(\d{2})th.*)|(.*(\d{4}).*)" )
            m = r.match(century)
            if(m.group(2)):
                year = m.group(2)
                ctr[year + 'th century'] += 1
            elif(m.group(4)):
                year = m.group(4)
                century = 0
                if '00' == year[2:]:
                    century = int(year[:2])
                else:
                    century = int(year[:2]) + 1
                ctr[str(century) + 'th century'] += 1
            else:
                print("wrong pattern")
    for k in ctr:
        print(k + ": " + str(ctr[k]))

if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("Wrong number of arguments!")
    elif sys.argv[2] == 'composer':
        composer(sys.argv[1])
    elif sys.argv[2] == 'century':
        century(sys.argv[1])
    else:
        print("Unknown arguments!")
