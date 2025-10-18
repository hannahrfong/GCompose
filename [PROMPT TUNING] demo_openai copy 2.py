import os
from typing import Dict, Any
import json
import subprocess
import csv
import numpy as np
import igraph as ig
from pyvis.network import Network
from src.hipporag import HippoRAG

# ============================================
# === CSV LOGGING HELPERS
# ============================================

CSV_FIELDNAMES = [
    "Prompt",
    "# of Unique Nodes",
    "# of Unique Edges",
    "# of Unique Triples",
    "# of Synonymy Edges",
    "Average Degree",
    "Density",
    "wccR",
    "AUC",
    "Precision",
    "Recall",
    "F1",
]

def append_row_to_csv(csv_path: str, row: Dict[str, Any], fieldnames=CSV_FIELDNAMES):
    """Append a single row (dict) to csv_path safely."""
    file_exists = os.path.exists(csv_path)
    row_to_write = {k: row.get(k, "") for k in fieldnames}
    with open(csv_path, "a", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_to_write)
        fout.flush()

# ============================================
# === CARB HELPERS
# ============================================

def convert_to_carb_tabbed(json_file, output_file):
    """Convert HippoRAG JSON output to CaRB tabbed format."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, "w", encoding="utf-8") as fout:
        for chunk in data["docs"]:
            chunk_id = str(chunk["idx"])
            for triple in chunk.get("extracted_triples", []):
                if len(triple) < 3:
                    continue
                subj, rel, obj = triple
                fout.write(f"{chunk_id}\t1.0\t{rel}\t{subj}\t{obj}\n")

    print(f"✅ Converted to CaRB format: {output_file}")

def run_carb_evaluation(carb_dir, gold_path, tabbed_path, output_path):
    """Run CaRB and parse its results."""
    carb_script = os.path.join(carb_dir, "carb.py")
    cmd = [
        "python3",
        carb_script,
        f"--gold={gold_path}",
        f"--out={output_path}",
        f"--tabbed={tabbed_path}"    
    ]

    result = subprocess.run(cmd, cwd=carb_dir, capture_output=True, text=True)
    print("=== CaRB STDOUT ===")
    print(result.stdout)
    print("=== CaRB STDERR ===")
    print(result.stderr)

    # Parse the results from stdout
    auc, prec, rec, f1 = 0, 0, 0, 0
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("AUC:"):
            try:
                # Split AUC and Optimal part
                auc_part, opt_part = line.split("Optimal")
                auc = float(auc_part.replace("AUC:", "").strip())
                
                # Extract numbers inside brackets
                import re
                match = re.search(r"\[([0-9.eE\s]+)\]", opt_part)
                if match:
                    numbers = match.group(1).strip().split()
                    prec, rec, f1 = map(float, numbers)
            except Exception as e:
                print("⚠️ Failed to parse CaRB output:", e)
                
    return {"AUC": auc, "Precision": prec, "Recall": rec, "F1": f1}

# ============================================
# === GRAPH HELPERS
# ============================================

def evaluate_directed_graph_quality(graph: ig.Graph) -> dict:
    """Compute key graph metrics."""
    non_synonym_edges = [e.index for e in graph.es if e["relation"] != ""]
    subgraph = graph.subgraph_edges(non_synonym_edges, delete_vertices=False)
    num_nodes = subgraph.vcount()
    num_edges = subgraph.ecount()

    if num_nodes == 0:
        return {"error": "Empty graph."}

    degrees = subgraph.degree()
    avg_degree = float(np.mean(degrees))
    density = subgraph.density(loops=False)
    components = subgraph.components(mode="weak")
    wccR = len(components) / num_nodes

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "avg_degree": round(avg_degree, 4),
        "density": round(density, 6),
        "wccR": round(wccR, 6),
    }

def visualize_graph(graph, save_path):
    """Render and save graph visualization in PyVis."""
    net = Network(notebook=True, directed=graph.is_directed())
    for v in graph.vs:
        label = v["content"] if "content" in v.attributes() else v["name"]
        net.add_node(v.index, label=label, title=str(v.attributes()))
    for edge in graph.es:
        source, target = edge.source, edge.target
        rel = edge["relation"] if "relation" in edge.attributes() else ""
        color = "black" if rel else "red"
        net.add_edge(source, target, label=rel, color=color)
    net.show(save_path)
    print(f"🌐 Graph visualization saved at: {save_path}")

# ============================================
# === MAIN PIPELINE
# ============================================

def run_experiment(run_id: int, prompt_prefix: str, base_output_dir: str, csv_path: str):
    dataset_name = "enron"
    corpus_path = f"reproduce/dataset/{dataset_name}_corpus.json"
    prefix_data_path = "/Users/hannahfong/Desktop/GCompose_code/PQF/query_vectors/allen-p_flattened.json"
    llm_model_name = "gpt-4o-mini"
    embedding_model_name = "text-embedding-3-small"

    # Create unique output dir per run
    run_output_dir = os.path.join(base_output_dir, f"run{run_id}")
    os.makedirs(run_output_dir, exist_ok=True)

    # Load corpus and queries
    with open(prefix_data_path, "r") as f:
        user_record = json.load(f)
    with open(corpus_path, "r") as f:
        corpus = json.load(f)
    docs = [doc["text"] for doc in corpus]

    # Initialize HippoRAG for this run
    hipporag = HippoRAG(
        save_dir=run_output_dir,
        llm_model_name=llm_model_name,
        embedding_model_name=embedding_model_name,
    )
    hipporag.index(docs=docs)

    # Graph metrics
    graph_info = hipporag.get_graph_info()
    graph_results = evaluate_directed_graph_quality(hipporag.graph)

    # Save graph visualization
    graph_html_path = os.path.join(run_output_dir, "graph.html")
    visualize_graph(hipporag.graph, graph_html_path)

    # Convert to CaRB
    carb_dir = "/Users/hannahfong/Documents/GitHub/CaRB"
    pred_json = os.path.join(run_output_dir, "openie_results_ner_gpt-4o-mini.json")
    gold_path = os.path.join(carb_dir, "data/gold/tab.txt")
    tabbed_path = os.path.join(carb_dir, f"system_outputs/test/tab.txt")
    carb_output_path = os.path.join(carb_dir, f"dump/output_run{run_id}.dat")

    convert_to_carb_tabbed(pred_json, tabbed_path)
    carb_results = run_carb_evaluation(carb_dir, gold_path, tabbed_path, carb_output_path)

    # Log metrics
    prompt_name = f"{prompt_prefix}_run{run_id}"
    record = {
        "Prompt": prompt_name,
        "# of Unique Nodes": graph_results["num_nodes"],
        "# of Unique Edges": graph_info["num_unique_relations"],
        "# of Unique Triples": graph_info["num_extracted_triples"],
        "# of Synonymy Edges": graph_info["num_synonymy_triples"],
        "Average Degree": graph_results["avg_degree"],
        "Density": graph_results["density"],
        "wccR": graph_results["wccR"],
        "AUC": carb_results["AUC"],
        "Precision": carb_results["Precision"],
        "Recall": carb_results["Recall"],
        "F1": carb_results["F1"],
    }
    append_row_to_csv(csv_path, record)
    print(f"✅ Logged metrics for {prompt_name} to {csv_path}")

# ============================================
# === ENTRY POINT
# ============================================

def main():
    csv_path = "graph_and_carb_metrics.csv"
    base_output_dir = "outputs/openai"
    prompt_prefix = "prompt_v2_10shot(w/ gold)"

    for run_id in range(1, 4):  # Run 3 times
        print(f"\n🚀 Starting experiment {run_id}...")
        run_experiment(run_id, prompt_prefix, base_output_dir, csv_path)
        print(f"✅ Completed run {run_id}\n{'-'*50}")

if __name__ == "__main__":
    main()