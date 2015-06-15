# -*- coding: utf-8 -*-
__author__ = 'Jose Luis Villarejo'

import sys
import notas
import toneToBitbloq


#datos = "SpongeB:d=4,o=5,b=180:d.,8d,8e,8d,8b5,8g5,8b5,8d,8e,8d,b5,8p,16p,g.,e.,d.,b5,8p,g.,e.,d.,b5,8p,d.,e.,p,8p,f_.,g,8p,16p,d.,8g,8a,8b,8a,8p,8b,g,32p,8d,g"
#datos = "aadams:d=4,o=5,b=160:8c,f,8a,f,8c,b4,2g,8f,e,8g,e,8e4,a4,2f,8c,f,8a,f,8c,b4,2g,8f,e,8c,d,8e,1f,8c,8d,8e,8f,1p,8d,8e,8f#,8g,1p,8d,8e,8f#,8g,p,8d,8e,8f#,8g,p,8c,8d,8e,8f"
cancion = ""
defDur = 4
defOct = 5
bmp = 63
notaEntera = 0

num = 0

duracion = 0
nota = 0
escala = 0
misTonos = notas.notas()


def separa(pn):
    escala = defOct
    valor = []
    nota = 0
    i = 0

#    print "--------------- Trozo: " + pn
#-- Obtenemos la duración (provisional por ahora) --
    num = 0
    while pn[i].isdigit():
        valor.insert(i, pn[i])
        i += 1
    if len(valor):
        num = int(float("".join(valor)))
        dur = notaEntera / num
    else:
        dur = notaEntera / defDur

#-- Obtenemos la nota
    tipo = 't'
    if pn[i] == 'c':
        nota = 1
    elif pn[i] == 'd':
        nota = 3
    elif pn[i] == 'e':
        nota = 5
    elif pn[i] == 'f':
        nota = 6
    elif pn[i] == 'g':
        nota = 8
    elif pn[i] == 'a':
        nota = 10
    elif pn[i] == 'b':
        nota = 12
    else:
        nota = 0
        tipo = 's'

    i += i
    if i < len(pn):
    #-- miramos si la nota tiene el caracter '#'
        if pn[i] == '#':
            nota += 1
            i +=1
    #-- miramos si la nota tiene el caracter opcional '.'
    if i < len(pn):
        if pn[i] == '.':
            dur = dur / 2
            i += 1
    #-- Obtenemos la escala
    if i < len(pn):
        if  pn[i].isdigit():
            escala = int(pn[i])

    ind = (int(escala) - 4) * 12 + int(nota)

    tono = misTonos.gettono(ind)
#    print "tono" + str(tono)
    return [tipo, tono, dur]


def getParametros(par):
    global defOct
    global bmp
    global notaEntera

    lpar = par.split(',')
    defDur = lpar[0][2:]
    defOct = lpar[1][2:]
    bmp= lpar[2][2:]
    notaEntera = ((60 * 1000) // int(bmp)) * 4

def rtttlToTone(pm):
    sonido =[]
    vMusica = pm.split(',')
    i = 0
    while i < len(vMusica):
        sonido.insert(i, separa(vMusica[i]))
        i += 1
    return sonido

def generaTonos(ml):
    global cancion
    global musica
    global mTonos
    trozos = ml.split(':')
    cancion = trozos[0]
    parametros = trozos[1]
    musica = trozos[2]
    getParametros(parametros)
    mTonos = rtttlToTone(musica)


if (sys.argv) >= 2:
    nt = notas.notas()
    melodia = sys.argv[1]
    generaTonos(melodia)
    print "Cancion:" + cancion
#    print "defDur" + str(defDur)
#    print "defOct" + str(defOct)
#    print "bmp" + str(bmp)
    miXML = toneToBitbloq.toBitbloq(cancion, mTonos, "6")
    miCadena = miXML.toxml()
    llamadaCan = toneToBitbloq.blqCallProcSinReturn(cancion, "20", "10").toxml()
    llamadaCan = llamadaCan[llamadaCan.find("?>")+1:]
    #print llamadaCan
    miCadena = '<xml xmlns="http://www.w3.org/1999/xhtml">' + llamadaCan + miCadena[miCadena.find("?>")+2:] + "</xml>"
    #print miCadena
    fw = open(cancion + ".xml", "w")
    fw.write(miCadena)
    fw.close()
else:
    print "Tiene que pasar la melodia RTTTL como parametro"

"""
melodia = datos
generaTonos(melodia)

print "Cancion: " + cancion
print "defDur: " + str(defDur)
print "defOct: " + str(defOct)
print "bmp: " + str(bmp)
print "notaEntera: " + str(notaEntera)
print "musica: " + musica
print "Tono 5: " + "".join(map(str, mTonos[11]))

miXML = toneToBitbloq.toBitbloq(cancion, mTonos, "6")
miCadena = miXML.toxml()
llamadaCan = toneToBitbloq.blqCallProcSinReturn(cancion, "20", "10").toxml()
llamadaCan = llamadaCan[llamadaCan.find("?>")+1:]
#print llamadaCan
miCadena = '<xml xmlns="http://www.w3.org/1999/xhtml">' + llamadaCan + miCadena[miCadena.find("?>")+2:] + "</xml>"
#print miCadena
fw = open(cancion + ".xml", "w")
fw.write(miCadena)
fw.close()
"""