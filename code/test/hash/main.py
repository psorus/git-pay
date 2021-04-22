from mnemonic import Mnemonic
mnemo = Mnemonic("english")


words = mnemo.generate(strength=128)

seed = mnemo.to_seed(words, passphrase="")


#print(seed)



from coincurve import PrivateKey,PublicKey
from bip44 import Wallet
from bip44.utils import get_eth_addr
mnemonic = "purity tunnel grid error scout long fruit false embody caught skin gate"
w = Wallet(mnemonic)
sk, pk = w.derive_account("eth", account=0)
sk = PrivateKey(sk)
print(sk.public_key.format() == pk)

pk=PublicKey(pk)



print(pk)






