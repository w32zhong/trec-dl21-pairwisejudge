import os
import json
import sys
import fire

sys.path.insert(0, '../../')

from pyserini import search
from pyserini.search.lucene import LuceneSearcher


def extract():
    qrels = search.get_qrels('dl21-passage')
    #print(qrels[508292]['msmarco_passage_04_731995205'])

    searcher = LuceneSearcher.from_prebuilt_index('msmarco-v2-passage')
    #searcher = LuceneSearcher.from_prebuilt_index('msmarco-v2-passage-full')
    def produce_file(name, j):
        output_file = f'./output/{name}.json'
        print(output_file)
        with open(output_file, 'w') as fh:
            json.dump(j, fh, indent=4)
        quit()

    for qid in qrels:
        for docid, rele in qrels[qid].items():
            rele = int(rele)
            if rele > 0:
                print(qid, docid, rele)
                doc = searcher.doc(docid)
                if doc is not None:
                    #print(doc.contents())
                    json_doc = json.loads(doc.raw())
                    produce_file(json_doc['pid'], json_doc)


if __name__ == "__main__":
        fire.Fire(extract)
