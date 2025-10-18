import os
from typing import List
import json
import argparse
import logging
import numpy as np
from src.hipporag import HippoRAG
import igraph as ig
import numpy as np
from pyvis.network import Network
import igraph as ig
import csv
import subprocess
import json
import pandas as pd
import os

# ✅ Converts HippoRAG JSON to CaRB tabbed format
def convert_to_carb_tabbed(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as fout:
        for chunk in data["docs"]:
            chunk_id = str(chunk["idx"])
            triples = chunk.get("extracted_triples", [])
            for triple in triples:
                if len(triple) < 3:
                    continue
                subj, rel, obj = triple
                confidence = "1.0"
                fout.write(f"{chunk_id}\t{confidence}\t{rel}\t{subj}\t{obj}\n")
    print(f"✅ Converted to CaRB format: {output_file}")

# ✅ Runs CaRB evaluation via subprocess (like your CLI command)
def run_carb_evaluation(carb_dir, gold_path, tabbed_path, output_path, match_type="strictMatch"):
    """
    Run CaRB evaluation and parse the output.

    match_type can be one of:
    - 'exactMatch', 'predMatch', 'lexicalMatch', 'binaryMatch', 'simpleMatch', 'strictMatch'
    """

    carb_script = os.path.join(carb_dir, "carb.py")

    cmd = [
        "python3",
        carb_script,
        f"--gold={gold_path}",
        f"--out={output_path}",
        f"--tabbed={tabbed_path}"
    ]

    print(f"⚙️ Running CaRB: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=carb_dir, capture_output=True, text=True, check=True)

    # Parse the results from stdout
    auc, prec, rec, f1 = 0, 0, 0, 0
    for line in result.stdout.splitlines():
        if line.startswith("AUC:"):
            try:
                parts = line.replace("AUC:", "").strip().split()
                auc = float(parts[0])
                prec = float(parts[3].strip("(),"))
                rec = float(parts[4].strip("(),"))
                f1 = float(parts[5].strip("(),"))
            except Exception:
                pass

    print(result.stdout)
    return {"AUC": auc, "Precision": prec, "Recall": rec, "F1": f1}

def evaluate_directed_graph_quality(graph: ig.Graph) -> dict:
    """
    Evaluates key structural metrics for a directed knowledge graph:
    - average in-degree
    - average out-degree
    - density
    - weakly connected component ratio (wccR)
    """
    non_synonym_edges = [e.index for e in graph.es if e["relation"] != ""]
    subgraph = graph.subgraph_edges(non_synonym_edges, delete_vertices=False)

    num_nodes = subgraph.vcount()
    num_edges = subgraph.ecount()

    if num_nodes == 0:
        return {"error": "Empty graph."}

    # Degrees
    degrees = subgraph.degree()
    avg_degree = float(np.mean(degrees)) 

    # Density (directed definition)
    density = subgraph.density(loops=False)

    # Weakly connected components ratio (direction ignored)
    components = subgraph.components(mode="weak")
    wccR = len(components) / num_nodes

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "avg_degree": round(avg_degree, 4),
        "density": round(density, 6),
        "wccR": round(wccR, 6),
    }

def visualize_graph():

    # Load graph
    graph = ig.Graph.Read_Pickle(
        "/Users/hannahfong/Documents/GitHub/GCompose/outputs/openai/gpt-4o-mini_text-embedding-3-small/graph.pickle"
    )

    # Convert to PyVis
    net = Network(notebook=True, directed=graph.is_directed())

    # Add nodes
    for v in graph.vs:
        label = v["content"] if "content" in v.attributes() else v["name"]
        #print(label)
        net.add_node(v.index, label=label, title=str(v.attributes()))

    # Add edges (color depends on relation)
    for edge in graph.es:
        source = edge.source
        target = edge.target

        # Get relation label if exists
        relation = edge['relation'] if 'relation' in edge.attributes() else ""
        weight = edge['weight'] if 'weight' in edge.attributes() else 1.0

        # If relation is empty → different edge color
        if relation.strip() == "":
            edge_color = "red"   # color for missing relation
            label = str(weight)  # fall back to weight
        else:
            edge_color = "black" # normal color
            label = relation

        net.add_edge(
            source,
            target,
            label=label,
            title=str(edge.attributes()),
            color=edge_color
        )

    # Show graph
    net.show("/Users/hannahfong/Documents/GitHub/GCompose/outputs/graph.html")

def main2():
    # Prepare datasets and evaluation
    dataset_name = "enron"
    corpus_path = f"reproduce/dataset/{dataset_name}_corpus.json"
    prefix_data_path = f"/Users/hannahfong/Desktop/GCompose_code/PQF/query_vectors/allen-p_flattened.json"
    top_k = 5

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

                print("PREFIX: ", prefix)
                print("COMPLETION: ", completion)
                print("QUERY VECTOR", query_vector)
                print("\n\n")    

                # Skip empty query_vector
                if not query_vector:
                    #print(f"Skipping empty query_vector for doc {email_idx} sent {sent_idx} pair {pair_idx}")
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

                    # #print nicely
                    print(f"\nEMAIL {email_idx} | SENT {sent_idx} | PAIR {pair_idx} | Prefix: '{prefix}'")
                    print("Top retrieved entities and scores:")
                    for rank, (name, score) in enumerate(zip(node_names, top_scores), start=1):
                        print(f"  {rank:2d}. {name:<50}  {float(score):.6f}")


                    # 4. Extract reasoning paths dynamically
                    top_paths = hipporag.extract_top_k_paths(sorted_node_ids, sorted_node_scores, prefix_entry)

                    #print("=== SELECTED REASONING PATHS ===") # TODO: make direction correct
                    #for path in top_paths:
                    #    node_names = [hipporag.idx_to_node_name[idx] for idx in path]
                    #    print(" → ".join(node_names))
                    print("\n\n")    
                except Exception as e:
                    print(f"Error retrieving for doc {email_idx} sent {sent_idx} pair {pair_idx}: {e}")

    #print(f"Processed {total_pairs} prefix-completion pairs.")

def main():
    # Prepare datasets and evaluation
    dataset_name = "enron"
    corpus_path = f"reproduce/dataset/{dataset_name}_corpus.json"
    prefix_data_path = f"/Users/hannahfong/Desktop/GCompose_code/PQF/query_vectors/allen-p_flattened.json"
    top_k = 5

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

    # 1️⃣ Graph metrics
    graph_info = hipporag.get_graph_info()
    graph_results = evaluate_directed_graph_quality(hipporag.graph)
    print(graph_results)

    # 2️⃣ Save extracted triples JSON (for CaRB)
    pred_json = "/Users/hannahfong/Documents/GitHub/GCompose/outputs/openai/openie_results_ner_gpt-4o-mini.json"

    # 3️⃣ Convert JSON to CaRB tabbed format
    carb_dir = "/Users/hannahfong/Documents/GitHub/CaRB"
    gold_path = os.path.join(carb_dir, "data/gold/tab.txt")
    tabbed_path = os.path.join(carb_dir, "system_outputs/test/tab.txt")
    carb_output_path = os.path.join(carb_dir, "dump/output.dat")

    convert_to_carb_tabbed(pred_json, tabbed_path)

    # 4️⃣ Run CaRB evaluation
    carb_results = run_carb_evaluation(
        carb_dir=carb_dir,
        gold_path=gold_path,
        tabbed_path=tabbed_path,
        output_path=carb_output_path
    )
    print(carb_results)

    # 5️⃣ Append all results to CSV
    csv_path = "graph_and_carb_metrics.csv"
    prompt_name = "prompt_v1_run3"

    record = {
        "Prompt": prompt_name,
        "# of Unique Nodes": graph_results["num_nodes"],
        "# of Unique Edges": graph_results["num_edges"],
        "# of Unique Triples": graph_info["num_extracted_triples"],
        "# of Synonymy Edges": graph_info["num_synonymy_triples"],
        "Average Degree": graph_results["avg_degree"],
        "Density": graph_results["density"],
        "wccR": graph_results["wccR"],
        "AUC": carb_results["AUC"],
        "Precision": carb_results["Precision"],
        "Recall": carb_results["Recall"],
        "F1": carb_results["F1"]
    }

    df = pd.DataFrame([record])
    file_exists = os.path.exists(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=not file_exists, lineterminator='\n')
    print(f"✅ Logged metrics for {prompt_name} to {csv_path}")
    visualize_graph()

if __name__ == "__main__":
    main()
