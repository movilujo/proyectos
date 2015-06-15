# -*- coding: utf-8 -*-

__author__ = 'Jose Luis Villarejo'

from xml.dom.minidom import Document

id = 1
doc = Document()

def piezoBuzzerav(pin, tono, tp, ultimo ):
    global id
    blq = doc.createElement("block")
    blq.setAttribute("inline", "false")
    blq.setAttribute("id", str(id))
    id += 1
    blq.setAttribute("type", "zum_piezo_buzzerav")
    blq.appendChild(blqValue("PIN", pin))
    blq.appendChild(blqValue("TONE", tono))
    blq.appendChild(blqValue("DURA", tp))

    return blq

def blqValue(nombre, valor):
    global id
    bVal = doc.createElement("value")
    bVal.setAttribute("name", nombre)
    bBlq = doc.createElement("block")
    bBlq.setAttribute("id", str(id))
    bBlq.setAttribute("type","pin_digital")
    id += 1
    bCamp = doc.createElement("field")
    if nombre == "PIN":
        bCamp.setAttribute("name", nombre)
    else:
        bBlq.setAttribute("type", "math_number")
        bCamp.setAttribute("name", "NUM")
    texto = doc.createTextNode(valor)
    bCamp.appendChild(texto)
    bBlq.appendChild(bCamp)
    bVal.appendChild(bBlq)
    return bVal

def blqProcDefSinReturn(nombre, x, y):
    global id
    bloque = doc.createElement("block")
    bloque.setAttribute("type", "procedures_defnoreturn")
    bloque.setAttribute("id", str(id))
    id += 1

    bloque.setAttribute("x", x)
    bloque.setAttribute("y", y)
    doc.appendChild(bloque)
    muta = doc.createElement("mutation")
    bloque.appendChild(muta)
    campo = doc.createElement("field")
    campo.setAttribute("name", "NAME")
    bloque.appendChild(campo)
    texto = doc.createTextNode(nombre)
    campo.appendChild(texto)
    return bloque


def blqRetardo(ms):
    global id
    blq = doc.createElement("block")
    blq.setAttribute("inline", "false")
    blq.setAttribute("id", str(id))
    id += 1
    blq.setAttribute("type", "base_delay")
    blq.appendChild(blqValue("DELAY_TIME", ms))
    return blq

def blqCallProcSinReturn(nombre, x, y):
    global id
    bloque = doc.createElement("block")
    bloque.setAttribute("type", "procedures_callnoreturn")
    bloque.setAttribute("id", str(id))
    id += 1

    bloque.setAttribute("x", x)
    bloque.setAttribute("y", y)
#    doc.appendChild(bloque)
    muta = doc.createElement("mutation")
    bloque.appendChild(muta)
    campo = doc.createElement("field")
    campo.setAttribute("name", "PROCEDURES")
    bloque.appendChild(campo)
    texto = doc.createTextNode(nombre)
    campo.appendChild(texto)
    return bloque


def melodia(lista, pin):

    global id
#    print "En melodia: " + str(len(lista))

    tipo = lista[0][0]
    tono = str(lista[0][1])
    duracion = str(lista[0][2])
#    print tipo + " - " + tono + " - " + duracion
    if len(lista) > 1:
        if tipo == 't':
#            print "+1 tipo t"
            blq = doc.createElement("block")
            blq.setAttribute("inline", "false")
            blq.setAttribute("id", str(id))
            id += 1
            blq.setAttribute("type", "zum_piezo_buzzerav")
            blq.appendChild(blqValue("PIN", pin))
            blq.appendChild(blqValue("TONE", tono))
            blq.appendChild(blqValue("DURA", duracion))
            sig = doc.createElement("next")
            sig.appendChild(melodia(lista[1:], pin))
            blq.appendChild(sig)
        else:
#            print "+1 tipo s"
            blq = doc.createElement("block")
            blq.setAttribute("inline", "false")
            blq.setAttribute("id", str(id))
            id += 1
            blq.setAttribute("type", "base_delay")
            blq.appendChild(blqValue("DELAY_TIME", duracion))
            sig = doc.createElement("next")
            sig.appendChild(melodia(lista[1:], pin))
            blq.appendChild(sig)
    else:
        if tipo == 't':
#            print "1 tipo t"
            blq = doc.createElement("block")
            blq.setAttribute("inline", "false")
            blq.setAttribute("id", str(id))
            id += 1
            blq.setAttribute("type", "zum_piezo_buzzerav")
            blq.appendChild(blqValue("PIN", pin))
            blq.appendChild(blqValue("TONE", tono))
            blq.appendChild(blqValue("DURA", duracion))
        else:
#            print "1 tipo s"
            blq = doc.createElement("block")
            blq.setAttribute("inline", "false")
            blq.setAttribute("id", str(id))
            id += 1
            blq.setAttribute("type", "base_delay")
            blq.appendChild(blqValue("DELAY_TIME", duracion))
    return blq

def toBitbloq(nombre, tonos, ppin):

    bloque = blqProcDefSinReturn(nombre, "200", "10")
    sent = doc.createElement("statement")
    sent.setAttribute("name", "STACK")
    bloque.appendChild(sent)
    sent.appendChild(melodia(tonos, ppin))
#    print doc.toprettyxml(indent="   ")
#    return doc.toprettyxml(indent="   ")
    doc.appendChild(bloque)
    return doc