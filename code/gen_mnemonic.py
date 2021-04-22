from mnemonic import Mnemonic

def gen_mnemonic(stre=128):
    mnemo=Mnemonic("english")
    words=mnemo.generate(strength=stre)
    return words
