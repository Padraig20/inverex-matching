import pickle
from typing import List, Dict

import numpy as np
from rank_bm25 import BM25Plus
from tqdm import tqdm

from src.nlp.CTnlp.clinical_trial import ClinicalTrial


class Indexer:
    """Wrapper around BM25Okapi class that indexes ClinicalTrials and allows for
    querying them with Topic data. input data must be preprocessed and tokenized."""

    index: BM25Plus
    lookup_table: Dict[int, str]

    def index_clinical_trials(self, clinical_trials: List[ClinicalTrial]):
        cts_tokenized = []

        for _clinical_trial in tqdm(clinical_trials):
            cts_tokenized.append(_clinical_trial.text_preprocessed)

        self.index = BM25Plus(cts_tokenized)
        self.lookup_table = {x_index: x.nct_id for x_index, x in enumerate(clinical_trials)}

    def index_text(self, text, lookup_table):
        self.index = BM25Plus(text)
        self.lookup_table = lookup_table

    def query_single(self, query: List[str], return_top_n: int) -> Dict[str, float]:
        """Query needs to be tokenized."""
        topic_scores = {}
        doc_scores = self.index.get_scores(query)
        for index, score in zip(
            np.argsort(doc_scores)[-return_top_n:], np.sort(doc_scores)[-return_top_n:]
        ):
            topic_scores[self.lookup_table[index]] = score

        return topic_scores

    def load_index(self, filename: str):
        """Loads index from a pickled file into index variable."""
        with open(filename, "rb") as _fp:
            self.index = pickle.load(_fp)

    def save_index(self, filename: str):
        """Saves index into a pickled file."""
        with open(filename, "wb") as _fp:
            pickle.dump(self.index, _fp)