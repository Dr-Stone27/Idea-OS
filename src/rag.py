import os
import json
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMEWORKS_DIR = os.path.join(BASE_DIR, "knowledge_base", "frameworks")

def get_frameworks_from_bucket(bucket_name: str, top_k: int = 5) -> List[Dict]:
    """Retrieve up to top_k frameworks from a given bucket."""
    bucket_dir = os.path.join(FRAMEWORKS_DIR, bucket_name)
    if not os.path.exists(bucket_dir):
        return []
        
    frameworks = []
    
    # Simple semantic search placeholder for Phase 2: just read the JSON files in the bucket.
    # In a full production build, this would hit ChromaDB using semantic embedding.
    # Since we have roughly 4-6 per bucket, reading all files natively scales for this phase.
    for filename in os.listdir(bucket_dir):
        if filename.endswith(".json"):
            with open(os.path.join(bucket_dir, filename), "r") as f:
                fw = json.load(f)
                frameworks.append(fw)
                if len(frameworks) >= top_k:
                    break
                    
    return frameworks

def search(query: str, bucket: str, top_k: int = 5) -> List[Dict]:
    """
    Search for relevant frameworks based on the query and router tags.
    Pulls top_k from the target bucket, and ALWAYS top_2 from the cross-domain bucket.
    """
    results = []
    
    # Fetch from the specified primary bucket
    if bucket:
        results.extend(get_frameworks_from_bucket(bucket, top_k=top_k))
        
    # Always pull from cross-domain
    if bucket != "cross-domain":
        results.extend(get_frameworks_from_bucket("cross-domain", top_k=2))
        
    return results
