def tim_dna(dna, pattern):
    n, m = len(dna), len(pattern)
    for i in range(n - m + 1):
        if dna[i:i+m] == pattern:
            return True
    return False
dna = "ACGTACGTGAC"
pattern = "GTGA"
print("Có xuất hiện:", tim_dna(dna, pattern))
