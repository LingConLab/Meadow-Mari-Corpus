#-*-coding: utf-8; -*-
#qpy: 3
#qpy: console

import urllib.request as ur
import urllib.parse
import re
import os
import trans

#cleans files
def cleanf(one = "text.txt", two = "glosses.txt"):
    def templ(path):
        f = open(path, 'w', encoding = "utf-8")
        f.write('')
        f.close()
    templ(one)
    templ(two)

#gets html from analyzer
def from_site_get(word):
    print(word)
    url = 'http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text=' + urllib.parse.quote(word) + '&action=analyze&lang=mhr&plang=eng'
    try:
        page = ur.urlopen(url)
    except:
        print('Trouble with this one')
        return "\bell"
    text = page.read().decode("utf-8")
    return text

#reads html and returns a list of possible variants of analisis
def info_q(htm):
#    searcher(html) in info_q(html) does the actual work, only it is started if everything is ok
    def searcher(h):
        nar = re.findall('<pre>(.*?)</pre>', h, flags=re.DOTALL)
        if len(nar) > 1:
            print("Too bad :-(")
            return ""
        else:
            word_list = []
            for variant in re.findall('(<font color="red">.*?)\n', "".join(nar), flags=re.DOTALL):
                tags = []
                finreg = re.findall('>(.*?)<', "".join(variant), flags=re.DOTALL)
                endreg = re.findall('(?:.*)>(.*)', "".join(variant), flags=re.DOTALL)
                if endreg and len(endreg) == 1:
                    finreg.append("".join(endreg))
#                print(finreg)
                for smth in finreg:
                    if not smth in '\t+' and not smth == '':
                        tags.append(smth)
                word_list.append(tags)
        return word_list
                
    if not htm == "\bell":
        print(searcher(htm))
        return searcher(htm)
    else:
        return '\bell'

#And despise commas, they are analed too
def comma_d(anal):
    if anal == '\bell':
        return ''
    for vari in anal:
        if "CLB" in "".join(vari):
            trash = anal.pop()
    return anal

#simply opens a file
def fopen(path):
    f = open(path, 'r', encoding = "utf-8")
    text = f.read()
    f.close()
    return text

#reads file and splits it
def reader(path):
    text = fopen(path)
    if text:
        return text.split("\n")

#writes text into a file
def writer(pat, writings):
    if pat:
        f = open(pat, 'a', encoding = "utf-8")
        f.write(writings)
        f.close()

#walks down the text, sends words to anal and gets it to 'glosses.txt', text and translation go to 'text.txt'
def text_walker(text):
    for line in text:
        if line.startswith('\Tr'):
            writer("text.txt", line + '\n') 
        if line.startswith('\Tx'):
            #when I get a text line, a use my program that turns the transcription to the standerd meadow mari graphics
            line = trans.tran(line[3:])
            writer("text.txt", line + '\n')
            line = re.sub('[;:%"\(\)\?\.\!/\,—]', "", line)
            words = line.split(" ")
            writer("glosses.txt", "\gk")
            for word in words:
                if word == '\Tx' or word == "":
                    continue
                #next line sends the word to the site, gets the respond, processes it and writes into a special file
                #writings = "-".join(comma_d(verb_p(info_q(from_site_get(word))))) + "\t"
                writings = str(comma_d(info_q(from_site_get(word)))) + "\t"
                writer("glosses.txt", writings)
            writer("glosses.txt", "\n")

#The analyzer requires влак and шамыч to be written with a dash
def dasher(word):
    if word.endswith("влак"):
        word = "/".join(word)
        return word.replace("влак", "-влак").split("/")
    elif word.endswith("шамыч"):
        word = "/".join(word)
        return word.replace("шамыч", "-шамыч").split("/")
    else:
        return word

#Создать таблицу перевода тэгов
#def anal_turner(al):
#    for var in al:
        
        

def main():
    cleanf()
    text_walker(reader("t.txt"))

main()
