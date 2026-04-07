"""Module containing class that preprocesses ClinicalTrial objects and builds features
for model predictions."""
import logging
from typing import List

import spacy
from src.nlp.CTnlp.clinical_trial import ClinicalTrial


def get_tokens(preprocessed_text, no_stopwords, no_punctuation, lemmatised):
    if no_stopwords and no_punctuation:
        tokens = [token.text for token in preprocessed_text if not token.is_stop and not token.is_punct]
    elif no_stopwords and not no_punctuation:
        tokens = [token.text for token in preprocessed_text if not token.is_stop]
    elif not no_stopwords and no_punctuation:
        tokens = [token.text for token in preprocessed_text if not token.is_punct]
    else:
        tokens = [token.text for token in preprocessed_text]

    if lemmatised:
        lemmas = [token.lemma_ for token in preprocessed_text if not token.is_stop and not token.is_punct]
        tokens.extend(lemmas)

    return tokens

class ClinicalTrialsFeatures:
    """Class wrapping nlp spacy language model that tokenizes and removes stopwords
    for ClinicalTrial objects"""

    def __init__(self, spacy_language_model_name: str = "en_core_sci_lg"):
        self.nlp = spacy.load(
            spacy_language_model_name,
            disable=[
                "ner",
                "tok2vec",
                "tagger",
                "parser",
                "attribute_ruler",
                "lemmatizer",
            ],
        )
        logging.info("loaded spacy language model for preprocessing Clinical Trials")

    def preprocess_clinical_trial(self, clinical_trial: ClinicalTrial, no_stopwords=True, no_punctuation=True, lemmatised=False) -> None:
        """Preprocesses a clinical trial text field using spacy tokenizer and removing
        stopwords. Preprocessed text is saved to a variable in the clinical_trial
        object."""
        preprocessed = self.nlp(clinical_trial.text)

        clinical_trial.text_preprocessed = get_tokens(preprocessed_text=preprocessed, no_stopwords=no_stopwords, no_punctuation=no_punctuation, lemmatised=lemmatised)
        # clinical_trial.text_preprocessed = [
        #     token.text for token in preprocessed if not token.is_stop and not token.is_punct
        # ]

    def preprocess_text(self, text: str, no_stopwords=True, no_punctuation=True, lemmatised=True) -> List[str]:
        """Preprocesses a custom text field using spacy tokenizer and removing
        stopwords. Preprocessed text is returned as a List of tokenized strings.

        This method can be used to obtain the same preprocessing for e.g. Topic data
        as for ClinicalTrial."""
        preprocessed = self.nlp(text)
        # return [token.text for token in preprocessed if not token.is_stop and not token.is_punct]
        return get_tokens(preprocessed_text=preprocessed, no_stopwords=no_stopwords, no_punctuation=no_punctuation, lemmatised=lemmatised)