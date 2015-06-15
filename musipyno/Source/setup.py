# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(name="rtttyTobitbloq",
 version="1.0",
 description="Programa para codificar ficheros de audio 8bit en formato RTTTL a script de bitbloq (bq) para arduino",
 author="Jose Luis Villarejo",
 url="url del proyecto",
 license="tipo de licencia",
 console=["rtttyTobitbloq2.py"],
 options={"py2exe": {"bundle_files": 2}},
 zipfile=None,
)