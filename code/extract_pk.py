from coincurve import PublicKey


def extract_pk(hx):
    q=bytes.fromhex(hx)
    return PublicKey(q)






if __name__=="__main__":
    pk=extract_pk("030808635882a4f0b071d37e1e28c1d538a2ac17b0cc12da2bcca421350cba8c22")



