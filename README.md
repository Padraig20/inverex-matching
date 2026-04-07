# Inverex Matching

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

## Text-Based Matching (NLP)

The implementation for this pipeline is taken and adapted from [patient-trial-matching](https://github.com/ProjectDossier/patient-trial-matching) and [clinical-trials](https://github.com/WojciechKusa/clinical-trials).

### Installation

This project is based on UV. Run following command to install all dependencies:

```{console}
$ uv sync
```

Furthermore, the workflow uses a custom NLP model for Named Entity Recognition. Make sure to run `uv run python -m src.nlp.setup` to download and unpack it in the designated folder.

Patients texts and QRels from the TREC Clinical Trials challenge are already downloaded in `data/patients` and `data/qrels`, respectively. Make sure to download and unpack clinical trial texts from [the official TREC website](http://trec-cds.org/2022.html)], which uses a snapshot of [ClinicalTrials.gov](ClinicalTrials.gov).

### Usage

Both the patient and clinical trial data are processed via NLP models before they are used for querying and ranking via BM25. Following scripts prepare JSONL files for both patients and clinical trials, respectively.

```{console}
$ uv run -m src.nlp.preprocessing.prepare_patients -i data/patients/ -o data/processed/patients
$ uv run -m src.nlp.preprocessing.prepare_trials -i data/clinical_trials/ -o data/processed/trials.jsonl
```

Afterwards, we can use the generated JSONL files to for querying and ranking. This script immediately launches several possible query configurations and grades them according to the QRels from the TREC Clinical Trials challenge (QRels available in `data/qrels`).

```{console}
$ uv run python -m src.nlp.matching.keyword_matching --trials data/processed/trials.jsonl --patients data/processed/patients/topics2021.jsonl -o output --graded_qrels data/qrels/qrels2021.txt
```
