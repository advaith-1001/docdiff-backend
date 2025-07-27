from app.models.schemas import ComparisonResult

def compare_texts(text1: str, text2: str) -> ComparisonResult:
    set1 = set(text1.split())
    set2 = set(text2.split())

    common = set1 & set2
    only_in_1 = set1 - set2
    only_in_2 = set2 - set1

    return ComparisonResult(
        common_words=list(common),
        only_in_file1=list(only_in_1),
        only_in_file2=list(only_in_2)
    )
