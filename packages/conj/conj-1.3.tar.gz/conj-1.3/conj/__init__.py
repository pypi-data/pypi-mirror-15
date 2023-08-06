#!/usr/bin/env python
#-*- coding: UTF-8 -*-

VOWEL_LETTERS = [
    'a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü'
]
VOWELS = {}
VOWELS['dative'] = \
VOWELS['adessive'] = \
VOWELS['ablative'] = {
    'a': 'a', 'e': 'e', 'ı': 'a', 'i': 'e',
    'o': 'a', 'ö': 'e', 'u': 'a', 'ü': 'e'
}
VOWELS['accusative'] = {
    'a': 'ı', 'e': 'i', 'ı': 'ı', 'i': 'i',
    'o': 'u', 'ö': 'ü', 'u': 'u', 'ü': 'ü'
}
SOFTENINGS = {}
SOFTENINGS['dative'] = \
SOFTENINGS['accusative'] = {
    'k': 'ğ'
}
SOFTENINGS['adessive'] = \
SOFTENINGS['ablative'] = {
    'k': 'k'
}
EXCEPTIONS = {}
EXCEPTIONS['dative'] = {
    'ben': 'bana',
    'sen': 'sana',
    'o': 'ona'
}
EXCEPTIONS['accusative'] = {
    'o': 'onu'
}
EXCEPTIONS['adessive'] = {
    'o': 'onda'
}
EXCEPTIONS['ablative'] = {
    'o': 'ondan'
}
HANDLERS = {
    # 0: infix for words ending with a vowel
    # 1: infix for words ending with not a vowel
    # 2: infix if last letter in SOFTENINGS
    # 3: extra last letter if needed
    'dative':     ['y', '', '', ''],
    'accusative': ['y', '', '', ''],
    'adessive':   ['d', 'd', 't', ''],
    'ablative':   ['d', 'd', 't', 'n']
}
HANDLER_SHORTCUTS = {
    'e': 'dative',
    'i': 'accusative',
    'de': 'adessive',
    'den': 'ablative',
}

class Conj(object):

    def getLastLetter(self, word):
        return word[-1].lower()

    def getLastVowel(self, word):
        for letter in reversed(word.lower()):
            if letter in VOWEL_LETTERS:
                return letter

    def getSuffix(self, word, conjType):
        lv = self.getLastVowel(word)
        if lv:
            return VOWELS[conjType][lv]

    def conjugate(self, word, properName=False, conjType='dative'):
        if conjType in HANDLER_SHORTCUTS:
            conjType = HANDLER_SHORTCUTS[conjType]
        if not properName and word in EXCEPTIONS[conjType]:
            return EXCEPTIONS[conjType][word]
        ll = self.getLastLetter(word)
        suffix = self.getSuffix(word, conjType)
        if suffix:
            if ll in VOWEL_LETTERS:
                infix = HANDLERS[conjType][0]
            elif ll in SOFTENINGS[conjType]:
                infix = HANDLERS[conjType][2]
            else:
                infix = HANDLERS[conjType][1]
            lastLetter = HANDLERS[conjType][3]
            if properName:
                return '%s\'%s%s%s' % (word, infix, suffix, lastLetter)
            else:
                if ll in SOFTENINGS[conjType]:
                    word = '%s%s' % (word[:-1], SOFTENINGS[conjType][ll])
                return '%s%s%s%s' % (word, infix, suffix, lastLetter)
        return word

    __call__ = conjugate

conj = Conj()
