def mergeAlternately(word1: str, word2: str) -> str:
    res = []
    n1, n2 = len(word1), len(word2)
    # Iterate through both strings up to the maximum length
    for i in range(max(n1, n2)):
        if i < n1:
            res.append(word1[i])
        if i < n2:
            res.append(word2[i])
    return "".join(res)

# Test cases
if __name__ == "__main__":
    test_cases = [
        ("abc", "pqr"),
        ("ab", "pqrs"),
        ("abcd", "pq")
    ]
    
    for w1, w2 in test_cases:
        result = mergeAlternately(w1, w2)
        print(f"word1: '{w1}', word2: '{w2}' -> result: '{result}'")
