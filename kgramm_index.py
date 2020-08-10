import ngram
from ngram import NGram

def build_k_gramm_index(indexed_terms):
    n = NGram()
    terms = []
    kgramms = []
    kgramm_index = []
    for indexed_term in indexed_terms:
        indexed_term_new = n.pad(indexed_term)
        list_indexed_terms = list(n.split(indexed_term_new))
        for kgramm in list_indexed_terms:
            lst = []
            if (kgramm in kgramms):
                i = kgramms.index(kgramm)
                lst = terms[i]
                if (indexed_term in lst):
                    continue
                else:
                    lst.append(indexed_term)
            else:
                kgramms.append(kgramm)
                i = kgramms.index(kgramm)
                if (indexed_term in lst):
                    continue
                else:
                    lst.append(indexed_term)
                    terms.insert(i, lst)
    i = 0
    for kgramm in kgramms:
        kgramm_index.append({
            'kgramm': kgramms[i],
            'term': terms[i]
        })
        i += 1
    return kgramm_index
