import numpy as np
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.preprocessing import normalize


def run_clustering(embeddings, eps=0.25, min_samples=2):
    
    if len(embeddings) < 2:
        return [-1] * len(embeddings)

    X = np.array(embeddings)
    X_normalized = normalize(X, norm='l2')

    print(f"📊 Embedding matrix shape: {X.shape}")
    print(f"🎯 User requested eps={eps}")

    # First try: DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    labels = dbscan.fit_predict(X_normalized)

    unique = set(labels)
    n_clusters = len([l for l in unique if l != -1])
    n_noise = list(labels).count(-1)

    print(f"✅ DBSCAN: {n_clusters} clusters, {n_noise} noise")

    # If DBSCAN gives us too many clusters (>6), use hierarchical clustering
    if n_clusters > 6:
        print(f"⚠️ Too many clusters ({n_clusters}), using hierarchical clustering...")
        
        # Hierarchical clustering naturally merges similar groups
        n = len(embeddings)
        target_k = max(3, min(5, n // 4))  # Target 3-5 clusters
        
        hierarchical = AgglomerativeClustering(
            n_clusters=target_k,
            linkage='average',
            metric='cosine'
        )
        labels = hierarchical.fit_predict(X_normalized)
        
        print(f"✅ Hierarchical: {target_k} clusters")
        return labels.tolist()
    
    # If DBSCAN gave good results, use them
    if n_clusters >= 2:
        print(f"🎉 Using {n_clusters} clusters from DBSCAN")
        return labels.tolist()

    # Fallback: KMeans
    print(f"⚠️ DBSCAN failed, using KMeans...")
    n = len(embeddings)
    k = max(2, min(5, n // 4))
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_normalized)
    
    print(f"✅ KMeans: {k} clusters")
    return labels.tolist() 