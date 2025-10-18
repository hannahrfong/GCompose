import os
from typing import List
import json
import argparse
import logging
import numpy as np

from src.hipporag import HippoRAG

def main():
    # Prepare datasets and evaluation
    dataset_name = "enron"
    corpus_path = f"reproduce/dataset/{dataset_name}_corpus.json"
    prefix_data_path = f"/Users/hannahfong/Desktop/GCompose_code/PQF/initial query vector output/allen-p_flattened.json"
    top_k = 100

    with open(prefix_data_path, "r") as f:
        user_record = json.load(f)

    with open(corpus_path, "r") as f:
        corpus = json.load(f)
    docs = [doc["text"] for doc in corpus]

    save_dir = 'outputs/openai'  # Define save directory for HippoRAG objects (each LLM/Embedding model combination will create a new subdirectory)
    llm_model_name = 'gpt-4o-mini'  # Any OpenAI model name
    embedding_model_name = 'text-embedding-3-small'  # Embedding model name (NV-Embed, GritLM or Contriever for now) nvidia/NV-Embed-v2 

    # Startup a HippoRAG instance
    hipporag = HippoRAG(save_dir=save_dir,
                        llm_model_name=llm_model_name,
                        embedding_model_name=embedding_model_name)

    # Run indexing
    hipporag.index(docs=docs)

   # -----------------------------
    # 3. Run retrieval for each prefix
    # -----------------------------
    all_results = []
    total_pairs = 0
    for email_idx, email in enumerate(user_record):
        sentences = email.get("sentences", []) or []
        
        for sent_idx, sent in enumerate(sentences):
            prefix_pairs = sent.get("prefix_completion_pairs", []) or []

            for pair_idx, pair in enumerate(prefix_pairs):
                total_pairs += 1
                prefix = pair.get("prefix", "")
                completion = pair.get("completion", "")
                query_vector = pair.get("query_vector", {})
                
                # Skip empty query_vector
                if not query_vector:
                    print(f"Skipping empty query_vector for doc {email_idx} sent {sent_idx} pair {pair_idx}")
                    continue

                prefix_entry = {"prefix": prefix, "query_vector": query_vector}

                try:
                    print("TRY 1")
                    sorted_node_ids, sorted_node_scores = hipporag.retrieve_gcompose(prefix_entry)
                    print("TRY 2")
                    # normalize return types (could be numpy arrays)
                    sorted_node_ids = np.asarray(sorted_node_ids)
                    sorted_node_scores = np.asarray(sorted_node_scores)
                    print("TRY 3")
                    top_node_ids = sorted_node_ids[:top_k]
                    top_scores = sorted_node_scores[:top_k]
                    print("TRY 4")
                    # map node ids to human-readable names (fallback to string id)
                    node_names = [
                        hipporag.idx_to_entity_text.get(int(nid), str(int(nid)))
                        for nid in top_node_ids
                    ]
                    print("TRY 5")

                    # Print nicely
                    print(f"\nEMAIL {email_idx} | SENT {sent_idx} | PAIR {pair_idx} | Prefix: '{prefix}'")
                    print("Top retrieved entities and scores:")
                    for rank, (name, score) in enumerate(zip(node_names, top_scores), start=1):
                        print(f"  {rank:2d}. {name:<50}  {float(score):.6f}")


                    # 4. Extract reasoning paths dynamically
                    top_paths = hipporag.extract_top_k_paths(sorted_node_ids, sorted_node_scores, prefix_entry)

                    print("=== SELECTED REASONING PATHS ===") # TODO: make direction correct
                    for path in top_paths:
                        node_names = [hipporag.idx_to_node_name[idx] for idx in path]
                        print(" → ".join(node_names))
                    
                except Exception as e:
                    print(f"Error retrieving for doc {email_idx} sent {sent_idx} pair {pair_idx}: {e}")

    print(f"Processed {total_pairs} prefix-completion pairs.")

if __name__ == "__main__":
    main()
