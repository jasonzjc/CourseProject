import math
import sys
import time
import metapy
import pytoml

class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """

        # sd.id_d: document id
        # sd.doc_term_count: number of times the term appears in the current doc, c(t,D)
        # sd.doc_size: total number of terms in the doc, |D|
        # sd.doc_unique_terms: number of unique terms in the doc
        # sd.avg_dl: average document length, avgdl
        # sd.num_docs: total number of documents, N
        # sd.total_terms: total number of terms in the index
        # sd.query_length: the total length of the query
        # sd.corpus_term_count: number of times t_id appears in corpus, c(t,C)
        # sd.query_term_weight: query term count (or weight in case of feedback), c(t,Q)
        tfn = sd.doc_term_count * math.log(1 + sd.avg_dl/sd.doc_size,2)
        tf_score = sd.query_term_weight * (tfn/(tfn+self.param)) * math.log((sd.num_docs+1) / (sd.corpus_term_count + 0.5),2)
        return tf_score


def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25(1.87,0.75,490)
    # return metapy.index.PivotedLength(.3478)
    # return metapy.index.AbsoluteDiscount(0.69)
    # return metapy.index.JelinekMercer(0.533)
    # return metapy.index.DirichletPrior(196)
    # return InL2Ranker(5.59)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries
            
    print("NDCG@{}: {}".format(top_k, ndcg))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
