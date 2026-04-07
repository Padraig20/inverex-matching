import json
from typing import List, Dict, Any


def load_jsonl(infile: str) -> List[Dict[str, Any]]:
    with open(infile) as f:
        data = [json.loads(line) for line in f]
    return data