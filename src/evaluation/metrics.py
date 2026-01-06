def binary_metrics(y_true, y_pred):
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = (2 * precision * recall) / (precision + recall) if precision + recall else 0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if tp + tn + fp + fn else 0

    return precision, recall, f1, accuracy

def precision_at_k(results, k):
    relevant = sum(r["ground_truth"] for r in results[:k])
    return relevant / k
