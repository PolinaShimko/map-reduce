from pyhive import hive
import sys
def word2ngrams(text, n=3, exact=True):
	return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]
if __name__ == "__main__":
    if len (sys.argv) > 1:
        print ("Query: {}".format (sys.argv[1] ) )
    else:
        print ("Write a query!")
    query = sys.argv[1]
    query_norm = query.replace("*", "")
    query = query_norm + '$'
    gramm_3 = word2ngrams(query)
    print ("3_gram of query: {}".format (gramm_3))

    cursor = hive.Connection('192.168.0.108', port = 10000).cursor() 
    result_terms = []
    for gram in gramm_3:
            #print gram
	    sel = 'SELECT terms FROM kgramm_index where kramm=\'' + gram + '\''
	    #print sel
	    cursor.execute(sel)  
	    results = cursor.fetchall()
	    terms_k = list(results[0])
	    s = terms_k[0].replace("\"","")
	    s = s.replace("\'","")
	    s = s.replace("]","")
	    s = s.replace("[","")
	    mylist = s.split(',')
	    #print mylist
            query_term = [term for term in mylist if term.endswith(query_norm)]
            #print ("Count: {count_t}".format(count_t=len(query_term)))   
   	    #print (query_term)
            result_terms = result_terms + query_term
    
    result_terms = list(set(result_terms))
    #print ("Count: {count_t}".format(count_t=len(result_terms)))   
    print ("Result terms for query: {}".format(result_terms))

    for term in result_terms:
    	sel = 'select docs from inver_index where term = \'' + term + '\''
        #print sel
        cursor.execute(sel)
        results = cursor.fetchall()
        docs = list(results[0])
        s = docs[0]
        s = s.replace("]","")
	s = s.replace("[","")
        docs = s.split(',')
	print ("Docs for: {}".format(term))
	print docs
