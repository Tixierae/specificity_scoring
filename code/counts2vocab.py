from collections import Counter

from representations.matrix_serializer import save_count_vocabulary

def counts2vocab(counts_path):
    """
    Usage:
        counts2pmi.py <counts>
    """
    
    words = Counter()
    contexts = Counter()
    with open(counts_path) as f:
        for line in f:
            word, context, count = line.strip().split()
            count = int(count)
            words[word] += count
            contexts[context] += count

    words = sorted(words.items(), key=lambda (x, y): y, reverse=True)
    contexts = sorted(contexts.items(), key=lambda (x, y): y, reverse=True)
    save_count_vocabulary(counts_path + '.words.vocab', words)
    save_count_vocabulary(counts_path + '.contexts.vocab', contexts)

