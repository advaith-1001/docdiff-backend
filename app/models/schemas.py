from pydantic import BaseModel
from typing import List

class ComparisonResult(BaseModel):
    common_words: List[str]
    only_in_file1: List[str]
    only_in_file2: List[str]