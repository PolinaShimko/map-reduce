#!/usr/bin/python3
from argparse import ArgumentParser
from BTrees.OOBTree import OOBTree

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

from os import getcwd, listdir
from os.path import join, exists

from stop_words import get_stop_words

import json
import time
import os
import re
import ngram
from ngram import NGram


headline_fn = {}

p_stemmer = PorterStemmer()
stop_words = get_stop_words('en')
tokenizer = RegexpTokenizer(r'\w+')


def parse(name_of_file):
	frequency = {}
	document_text = open(name_of_file, 'r', encoding='utf8')
	#print(name_of_file)
	text_string = document_text.read().lower()
    #first = text_string.find("repost_text")+12
    ##print(text_string[first+12])
    #last=text_string.find("links")
	#print(text_string)
	sub = text_string[9:]
	last = sub.find("\"")
	sub = sub[:last]
	#print(sub)
	match_pattern = re.findall(r'\b[а-яёa-z]{3,15}\b', sub)
	#print(match_pattern)
	return sub, match_pattern

def make_index(required_directory):
    #work_dir = getcwd()
    #news_headlines_dir = join(work_dir, required_directory)
    news_headlines_dir = required_directory
    work_dir = required_directory
    if not exists(news_headlines_dir):
        print("[x] ERROR: Entered directory {required_directory} doesn't exist".format(
            required_directory=required_directory)
        )
        exit(-1)

    #news_headlines_file_names = listdir(news_headlines_dir)
    news_headlines_file_names = [os.path.join(news_headlines_dir, f)
                  for f in os.listdir(news_headlines_dir)
                  if f.endswith(".txt")]
    for news_headlines_file_name in news_headlines_file_names:
        headline, match_pattern1 = parse(news_headlines_file_name)
        #timestamp, headline = line.split(",")
        headline_fn[headline] = news_headlines_file_name

    collection = list(headline_fn.keys())
    terms = set()

    for collection_element in collection:
        base_terms = tokenizer.tokenize(collection_element)
        not_stopped_terms = [base_term for base_term in base_terms if base_term not in stop_words]
        stemmed_terms = [p_stemmer.stem(not_stopped_term) for not_stopped_term in not_stopped_terms]

        [terms.add(correct_term) for correct_term in stemmed_terms]

    #print(terms)
    #print("[*] Count of correct terms: {terms_count}".format(terms_count=len(terms)))

    index = {}
    for term in terms:
        count = 0
        in_collection_elements = []

        for collection_element in collection:
            if term in collection_element:
                count += 1
                in_collection_elements.append(headline_fn[collection_element])

        index[term] = {
            'count': count,
            'collection': in_collection_elements
        }

    indexed_terms = []
    sorted_indexed_terms = index #sorted(index.keys())
    for sorted_indexed_term in sorted_indexed_terms:
        indexed_terms.append({
            'term': sorted_indexed_term,
            'count': index[sorted_indexed_term]['count'],
            'collection': index[sorted_indexed_term]['collection']
        })

    #n = NGram()

    for sorted_indexed_term in sorted_indexed_terms:
        #sorted_indexed_term_new = n.pad(sorted_indexed_term)
        #list_indexed_terms = list(n.split(sorted_indexed_term_new))
        indexed_terms.append({
            'term': sorted_indexed_term,
            'count': index[sorted_indexed_term]['count'],
            #'k-gramm index': list_indexed_terms,
            'collection': index[sorted_indexed_term]['collection']
        })

    indexed_terms_dir = join(work_dir, 'indexed-terms')
    indexed_terms_file = open(join(indexed_terms_dir, 'indexed-terms.json'), 'w')
    json.dump(indexed_terms, indexed_terms_file, ensure_ascii=False, indent=2)

    return indexed_terms, sorted_indexed_terms


def build_k_gramm_index(indexed_terms):
#def build_k_gramm_index():
    n = NGram()
    #indexed_terms = ['polina', 'hello']
    terms = []
    kgramms = []
    kgramm_index = []


    for indexed_term in indexed_terms:
        #print('NEW TERM')
        indexed_term_new = n.pad(indexed_term)
        list_indexed_terms = list(n.split(indexed_term_new))
        #print(list_indexed_terms)
        for kgramm in list_indexed_terms:
            lst = []
            if (kgramm in kgramms):
                i = kgramms.index(kgramm)
                #print(i)
                lst = terms[i]
                if (indexed_term in lst):
                    continue
                else:
                    lst.append(indexed_term)
                    ##print(terms)
                    ##terms.insert(i, lst)
                #print(kgramms)
                #print('TERMS',terms)
            else:
                kgramms.append(kgramm)
                i = kgramms.index(kgramm)
                ##lst = terms[i]
                #print(i)
                if (indexed_term in lst):
                    continue
                else:
                    lst.append(indexed_term)
                    terms.insert(i, lst)
                #print (kgramms)
                #print(terms)
    i = 0
    for kgramm in kgramms:
        kgramm_index.append({
            'kgramm': kgramms[i],
            'term': terms[i]
        })
        i += 1
    print('COUNT',i)
    #indexed_kgramms_file = open('kgramm_index.json', 'w')
    #indexed_terms_file = open('terms_index.json', 'w')
    #json.dump(kgramms, indexed_kgramms_file, ensure_ascii=False, indent=2)
    #json.dump(terms, indexed_terms_file, ensure_ascii=False, indent=2)
    kgramm_file = open('kgramm_index.json', 'w')
    json.dump(kgramm_index, kgramm_file, ensure_ascii=False, indent=2)


    with open('C:\\Users\\Полина\\Documents\\laba1_2sem\\indexed-terms\\kgramm_index.txt', 'w') as out:
        for kgramm_i in kgramm_index:
            kgramm = kgramm_i['kgramm']
            out.write('{};{}\n'.format(kgramm, kgramm_i['term']))

    return kgramm_index


if __name__ == "__main__":
	parser = ArgumentParser()
	i = 16598
	parser.add_argument("-d", "--dir")
	args = parser.parse_args()
	choise=True
	while choise:
		print ("""
		1.Delete doc
		2.Insert doc
		3.Modify doc
		4.Exit
		""")
		choise=input() 
		if choise=="1":
			print ("\nEnter name of doc")
			name_doc = input()
			start1 = time.time()
			os.remove(name_doc)
			print("\nDoc deleted") 
			_invert_index, _indexed_terms = make_index(args.dir)
			_kgramms_index = build_k_gramm_index(_indexed_terms)
			stop1 = time.time()
			print("[*] Elapsed time: {:10.4f} sec".format(stop1 - start1))
		elif choise=="2":
			print ("\nEnter name of doc")
			name_doc = input()
			start2 = time.time()
			doc_text = open(name_doc, 'r', encoding='utf8')
			text = doc_text.read()
			name_new_doc = "C:\\Users\\Полина\\Documents\\laba1_2sem\\{}.txt".format(i)
			i = i + 1
			with open(name_new_doc, 'w') as out:
				out.write(text)
			print("\nDoc inserted") 
			_invert_index, _indexed_terms = make_index(args.dir)
			_kgramms_index = build_k_gramm_index(_indexed_terms)
			stop2 = time.time()
			print("[*] Elapsed time: {:10.4f} sec".format(stop2 - start2))
		elif choise=="3":
			print ("\nEnter name of doc")
			name_doc = input()
			print ("\nEnter doc content")
			content_doc = input()
			start3 = time.time()
			with open(name_doc, 'w') as out:
				out.write(content)
			print("\nDoc modified") 
			_invert_index, _indexed_terms = make_index(args.dir)
			_kgramms_index = build_k_gramm_index(_indexed_terms)
			stop3 = time.time()
			print("[*] Elapsed time: {:10.4f} sec".format(stop3 - start3))
		elif choise=="4":
			break;
		elif choise !="":
			print("\nTry again") 