import difflib

def compare_texts(text1: str, text2: str):
    """
    Compare two texts line by line and highlight precise word-level differences,
    preserving neat line structure.
    """
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    result = []
    sm = difflib.SequenceMatcher(None, lines1, lines2)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                result.append({"type": "equal", "text": lines1[i]})
        elif tag == "replace":
            for old_line, new_line in zip(lines1[i1:i2], lines2[j1:j2]):
                result.append({
                    "type": "line_diff",
                    "parts": word_level_diff(old_line, new_line)
                })
        elif tag == "delete":
            for i in range(i1, i2):
                result.append({"type": "remove", "text": lines1[i]})
        elif tag == "insert":
            for j in range(j1, j2):
                result.append({"type": "add", "text": lines2[j]})
    return {"diff": result}


def word_level_diff(line1: str, line2: str):
    """
    Compare two lines word by word and return structured diff with spaces preserved.
    Ensures the output is easy to read and segmented by word-level change.
    """
    words1 = line1.split()
    words2 = line2.split()

    sm = difflib.SequenceMatcher(None, words1, words2)
    diff_parts = []

    def append_with_space(word_list, diff_type):
        if word_list:
            joined_text = ' '.join(word_list)
            diff_parts.append({"type": diff_type, "text": joined_text})

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            append_with_space(words1[i1:i2], "equal")
        elif tag == "delete":
            append_with_space(words1[i1:i2], "remove")
        elif tag == "insert":
            append_with_space(words2[j1:j2], "add")
        elif tag == "replace":
            append_with_space(words1[i1:i2], "remove")
            append_with_space(words2[j1:j2], "add")

    return diff_parts