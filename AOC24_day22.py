def gen_sec(cur_sec, iterations):
    for _ in range(iterations):
        res = cur_sec * 64
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
        res = cur_sec//32
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
        res = cur_sec*2048
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
    return cur_sec

def sol1(buyer_secrets, iterations):
    res = 0
    for bs in buyer_secrets:
        res+=gen_sec(bs, iterations)
    return res

print(sol1([1, 10, 100, 2024], 2000))

def gen_sec_seq(cur_sec, iterations):
    seq = [cur_sec]
    for _ in range(iterations):
        res = cur_sec * 64
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
        res = cur_sec//32
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
        res = cur_sec*2048
        mix_res = cur_sec ^ res
        pru_res = mix_res%16777216
        cur_sec = pru_res
        seq.append(cur_sec)
    return tuple(seq)

from functools import lru_cache
from itertools import chain
@lru_cache(None)
def getIDifferenceSequence(seq, i):
    diffI = lambda x : seq[x]%10-seq[x-1]%10
    salePrice = seq[i]%10
    diffSequence = [diffI(i), diffI(i-1), diffI(i-2), diffI(i-3)]
    return tuple(diffSequence[::-1]), salePrice



def sol2_bruteforce(buyersStartSecrets, iterations):
    # Build all possible sequences for a buyer and the sale price for the sequence
    buyersSaleLog = {}
    for bss in buyersStartSecrets:
        bseq = gen_sec_seq(bss, iterations)
        bsaleLog = {}
        for i in range(4, iterations+1):
            diffSeq, salePrice = getIDifferenceSequence(bseq, i)
            if diffSeq not in bsaleLog:
                bsaleLog[diffSeq] = salePrice
        buyersSaleLog[bss] = bsaleLog
    allSeq = [list(d.keys()) for d in buyersSaleLog.values()]
    allSeq = set(chain(*allSeq))
    # Analyze all possible sequences and see which sequence gives the max number of bananas
    max_tot_bananas = -float('inf')
    max_seq = None
    for seq in allSeq:
        tot_bananas = 0
        for buyerSaleLog in buyersSaleLog.values():
            if seq in buyerSaleLog:
                tot_bananas += buyerSaleLog[seq]
        if tot_bananas > max_tot_bananas:
            max_tot_bananas = tot_bananas
            max_seq = seq
    return max_seq, max_tot_bananas

print(sol2_bruteforce([1, 2, 3, 2024], 2000))
