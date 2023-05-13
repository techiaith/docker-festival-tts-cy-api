#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata

ACCENT_MAPPING = tuple(zip(u"âêîôûŵŷáéíóúẃýàèìòùẁỳäëïöüẅÿÂÊÎÔÛŴŶÁÉÍÓÚẂÝÀÈÌÒÙẀỲÄËÏÖÜẄŸçÇñÑśŚćĆ", (u"a+", u"e+", u"i+", u"o+", u"u+", u"w+", u"y+", u"a/", u"e/", u"i/", u"o/", u"u/", u"w/", u"y/", u"a\\", u"e\\", u"i\\", u"o\\", u"u\\", u"w\\", u"y\\", u"a:", u"e:", u"i:", u"o:", u"u:", u"w:", u"y:")))

ACCENT_MAPPING = ACCENT_MAPPING + tuple((a.upper(), b.upper()) for a,b in ACCENT_MAPPING)

UNACCENTED = dict(ACCENT_MAPPING)

def de_accent(text):
    """Deaccents 'text'
    Text *must* already be unicode
    """
    # first replace known 'good' accents
    text = u"".join(UNACCENTED.get(x, x) for x in text)
    # next remove any other accented characters
    text = u"".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

