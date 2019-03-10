# -*- coding: utf-8 -*-
import pandas as pd
from langdetect import detect
import argparse
from tqdm import tqdm
import os.path
import re
from halo import Halo

ehbari = ["ސުމެއް","އެއް","ދެ","ތިން","ހަތަރު","ފަސް","ހަ","ހަތް","އަށް","ނުވަ","ދިހަ","އެގާރަ","ބާރަ","ތޭރަ","ސާދަ","ފަނަރަ","ސޯޅަ","ސަތާރަ","އަށާރަ","ނަވާރަ","ވިހި","އެކާވީސް","ބާވީސް","ތޭވީސް","ސައުވީސް","ފަންސަވީސް","ސައްބީސް","ހަތާވީސް","އަށާވީސް","ނަވާވީސް"]
dhihabari = ["ސުން","ދިހަ","ވިހި","ތިރީސް","ސާޅީސް","ފަންސާސް","ފަސްދޮޅަސް","ހައްދިހަ","އައްޑިހަ","ނުވަދިހަ"]
sunbari = ["","ހާސް","މިލިޔަން","ބިލިޔަން","ޓްރިލިޔަން"]

done = False

def Badhalu(inputString):
	intNum = eval(inputString.strip())
	if intNum < 1000:
	    return (HaasSub(inputString))
	else:
	    return (HaasMathi(inputString))

def HaasSub(inputNumber):
    number = int(inputNumber)
    satheyka = "ސަތޭކަ "
    if (0 <= number <= 29):
        return ehbari[number]
    elif (30 <= number <= 99):
        return (dhihabari[int(inputNumber[0])]) if (inputNumber[-1] == "0") else (dhihabari[int(inputNumber[0])] + " " + ehbari[int(inputNumber[1])])
    elif (100 <= number <= 999):
        rem = number % 100
        dig = number // 100
        if (dig == 2):
        	ehbari[2] = "ދުވި"
        	satheyka = "ސައްތަ "
        return (ehbari[dig] + satheyka) if (rem == 0) else (ehbari[dig] + satheyka + HaasSub(str(rem)))

def HaasBuri(inputNumber):
    number = int(inputNumber)
    arrHaas = []
    while number != 0:
        arrHaas.append(number % 1000)
        number //= 1000
    return arrHaas

def HaasMathi(inputNumber):
    number = int(inputNumber)
    arrZero = HaasBuri(number)
    lenArr = len(arrZero) - 1
    resArr = []
    z=0
    for z in arrZero[::-1]:
        wrd = HaasSub(str(z)) + " "
        zap = sunbari[lenArr] + " "
        if wrd == " ":
            break
        elif wrd == "ސުން ":
            wrd, zap = "", ""
        resArr.append(wrd + zap)
        lenArr -= 1
    res = "".join(resArr).strip()
    if res[-1] == ",": res = res[:-1]
    return res

def splitdhivehi(line,char):
    newlines = ""
    ls = line.split(char)
    for r in range (len(ls)):
        dline = (ls[r]) #.strip())
        newlines = newlines + dline +" \n" #(dline.strip()) +" \n"
        #print (newlines)
    return newlines

def AiiMaps(line):
    newline =""
    df = pd.read_csv("aaimaps.csv",sep=",",header=0)
    aaicount =(df.count().aai)
    bas_list = line.split()
    for i in range(0 , len(bas_list)):
        allbas = (bas_list[i])
        for r in range(aaicount):
            aai = df.iloc[r].aai
            bas = allbas[-(len(aai)):]
            if (aai == bas):
                newbas = allbas.replace(aai,df.iloc[r].normal)
                allbas = newbas
        newline = newline + " " + allbas

    return newline

def WriteFile(line,file):
    lang = ''
    try:
        lang = detect(line) == 'en' 
    except:
        if lang != 'en' : #if not english then we assume it's dhivehi. 
            if outfile is None:
                print (line.strip())
            else:
                file.write(line.strip()+"\n")    

def FixEveSheve(line,file):
    try:
        df = pd.read_csv("evemaps.csv",sep=",",header=0)
        evecount =(df.count().eve)
        bas_list = line.split()
        fahubas = (bas_list[-1])
        for r in range(evecount):
            eve = df.iloc[r].eve
            bas = fahubas[-(len(eve)):]
            if (eve == bas):
                newbas = fahubas.replace(eve,df.iloc[r].normal)
                newline = ""
                for rr in range (len(bas_list)-1):
                    newline = newline + " " + bas_list[rr] 
                newline = newline + " " + newbas
                WriteFile(newline,file)
                break
            else:
                WriteFile(line,file)
                break
    except:
        pass

def CleanAndReplaceNumbers(line,maxlen,minlen,file):
    print ("extracting sentences....\n")
    newlines = ""
    ls = line.split("\n")

    if (outfile is not None):
         xx = tqdm(range (len(ls)))
    else:
         xx = range (len(ls))

    for r in xx:
        dline = (ls[r].strip())
        if not (re.search('^[a-zA-Z0-9]+$',dline)):
            if (len(dline) > minlen) and (len(dline) < maxlen) :
                for s in dline.split():
                    if s.isdigit():
                        numbaru = Badhalu(str(int(s)))
                        dline = dline.replace(s, numbaru)
                        #to-do : one more valification to see if string (still) contrains a number. if so remove line ?
                FixEveSheve(AiiMaps(dline),file)

def processfile(file):
    spinner = Halo(text='cleaning file....', spinner='dots')
    spinner.start()

    file = open(file,"r") 
    all_of_it = file.read()
    result = splitdhivehi(all_of_it,".")
    result = splitdhivehi(result,"،")
    #result = splitdhivehi(result,"!")
    result = (result.replace(' ','  '))
    result = (result.replace('“',' '))
    result = (result.replace('"',' '))
    result = (result.replace('(',' '))
    result = (result.replace(')',' '))
    result = (result.replace('[',' '))
    result = (result.replace(']',' '))
    result = (result.replace(')',' '))
    result = (result.replace('(',' '))
    result = (result.replace(':',' '))
    result = (result.replace('-',' '))
    result = (result.replace('/',' '))
    result = (result.replace('\\','')) 
    result = (result.replace('”',' ')) 
    result = (result.replace('–',' ')) 
    result = (result.replace('…',''))
    result = (result.replace('_',''))

    spinner.stop()
    
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--maxlen", help="optional: max number of characters to select for sentences (default is 120)", default=120, type=int)
    parser.add_argument("--minlen", help="optional: min number of characters to select for sentences (default is 10)", default=10, type=int)
    parser.add_argument("--input", help = "input filename")
    parser.add_argument("--output", help = "optional: output filename")

    args = parser.parse_args()

    inputfile = args.input 
    outfile = args.output
    maxlen = args.maxlen
    minlen = args.minlen

    if inputfile is None:
        print ("err: need input file")
    else:
        if os.path.isfile(inputfile):
            if args.output:
                file = open(outfile,"w") 
                CleanAndReplaceNumbers(processfile(inputfile),maxlen,minlen,file)
                file.close()
                num_lines = sum(1 for line in open(outfile))
                print ("no of sentences extracted: "+ str(num_lines))
                print ("done.\n")
            else:
                CleanAndReplaceNumbers(processfile(inputfile),maxlen,minlen,None)
        else:
            print ("file does not exist!\n")
