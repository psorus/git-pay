
from coincurve import PrivateKey,PublicKey
from bip44 import Wallet

def gen_keys(mnemonic):

    w = Wallet(mnemonic)
    sk, opk = w.derive_account("eth", account=0)
    sk = PrivateKey(sk)
    pk = PublicKey(opk)

    return sk,pk,opk
