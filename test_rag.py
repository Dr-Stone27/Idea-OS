from src.rag import search

def test_rag_retrieval():
    # Test 1: Search product bucket
    res = search("test query", "product", top_k=2)
    # Target 2 from product + 2 cross-domain
    assert len(res) == 4, f"Expected 4 results, got {len(res)}"
    
    # Check that at least one result has 'cross-domain'
    cross_domain_count = sum(1 for fw in res if "cross-domain" in fw["bucket"])
    assert cross_domain_count == 2, f"Expected 2 cross-domain, got {cross_domain_count}"
    
    # Test 2: Search cross-domain specifically
    res_cd = search("test query", "cross-domain", top_k=5)
    # Should only return up to 5 from cross-domain, no duplicates
    assert len(res_cd) <= 5, f"Expected up to 5 results, got {len(res_cd)}"
    cross_domain_count_only = sum(1 for fw in res_cd if "cross-domain" in fw["bucket"])
    assert cross_domain_count_only == len(res_cd)

    print("All RAG tests passed successfully!")

if __name__ == "__main__":
    test_rag_retrieval()
