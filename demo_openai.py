import os
import json
import shutil
import numpy as np
import igraph as ig
from src.hipporag import HippoRAG
from pyvis.network import Network

def evaluate_graph(graph: ig.Graph, graph_info) -> dict:
    """Compute summary metrics for a directed graph."""
    non_synonym_edges = [e.index for e in graph.es if e["relation"] != ""]
    subgraph = graph.subgraph_edges(non_synonym_edges, delete_vertices=False)
    num_nodes = subgraph.vcount()
    num_edges = subgraph.ecount()

    if num_nodes == 0:
        return {
            "num_unique_nodes": 0,
            "num_unique_edges": 0,
            "num_unique_triples": 0,
            "num_synonymy_edges": 0,
            "avg_degree": 0,
            "density": 0,
            "wccR": 0,
        }
    degrees = subgraph.degree()
    density = subgraph.density(loops=False)
    wccR = len(subgraph.components(mode="weak")) / num_nodes

    return {
        "num_unique_nodes": num_nodes,
        "num_unique_edges": graph_info["num_unique_relations"],
        "num_unique_triples": graph_info["num_extracted_triples"],
        "num_synonymy_edges": graph_info["num_synonymy_triples"],
        "avg_degree": round(float(np.mean(degrees)), 4),
        "density": round(float(density), 6),
        "wccR": round(float(wccR), 6),
    }

def visualize_graph(graph, save_path):
    """Render and save graph visualization in PyVis."""
    print("VISUALIZE")
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
    
def build_incremental_kg(user_dir):
    """
    Build partition-wise KGs incrementally using HippoRAG.
    Each partition builds on the previous one, with each KG saved separately.
    """
    user_name = os.path.basename(user_dir)
    print(f"\n🧠 Building KGs for {user_name}")

    # ✅ Get partitions in correct order
    partitions = sorted(
        [f for f in os.listdir(user_dir)
         if f.startswith("KG_train_part_") or f == "KG_val.json"]
    )

    # ✅ Base output directory
    base_output_dir = os.path.join(user_dir, "partition_graphs")
    os.makedirs(base_output_dir, exist_ok=True)

    metrics = {}

    # === 1️⃣ Build KG_init ===
    kg_init_path = os.path.join(user_dir, "kg_init.json")
    with open(kg_init_path, "r", encoding="utf-8") as f:
        kg_init_docs = json.load(f)
    kg_init_texts = [d["text"] for d in kg_init_docs if "text" in d]

    kg_init_dir = os.path.join(base_output_dir, "KG_init")
    os.makedirs(kg_init_dir, exist_ok=True)

    # Always start fresh for KG_init
    hipporag = HippoRAG(
        save_dir=kg_init_dir,
        llm_model_name="gpt-4o-mini",
        embedding_model_name="text-embedding-3-small",
    )
    hipporag.index(docs=kg_init_texts)

    graph_info = hipporag.get_graph_info()
    metrics["KG_init"] = evaluate_graph(hipporag.graph, graph_info)
    print(f"✅ KG_init complete: {metrics['KG_init']}")

    visualize_graph(hipporag.graph, os.path.join(kg_init_dir, "graph.html"))

    prev_dir = kg_init_dir  # Used for incremental builds

    # === 2️⃣ Build incrementally for each partition ===
    for p_file in partitions:
        p_name = p_file.replace(".json", "")
        p_path = os.path.join(user_dir, p_file)

        print(f"\n🔁 Building {p_name} (from {os.path.basename(prev_dir)})")

        # Prepare new directory for this partition
        curr_dir = os.path.join(base_output_dir, p_name)
        if not os.path.exists(curr_dir):
            shutil.copytree(prev_dir, curr_dir)
        else:
            print(f"Directory '{curr_dir}' already exists. Skipping copy.")
            
        # Load docs for this partition
        with open(p_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
        docs_text = [d["text"] for d in docs if "text" in d]

        # Initialize HippoRAG from previous snapshot
        hipporag = HippoRAG(
            save_dir=curr_dir,
            llm_model_name="gpt-4o-mini",
            embedding_model_name="text-embedding-3-small",
        )

        # Incrementally index new docs
        hipporag.index(docs=docs_text)

        # Evaluate updated graph
        graph_info = hipporag.get_graph_info()
        metrics[p_name] = evaluate_graph(hipporag.graph, graph_info)
        print(f"✅ {user_name} | {p_name}: {metrics[p_name]}")

        visualize_graph(hipporag.graph, os.path.join(curr_dir, "graph.html"))

        prev_dir = curr_dir  # This becomes the input for the next partition

    # === 3️⃣ Save summary metrics ===
    summary_path = os.path.join(base_output_dir, "graph_metrics.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"📊 Saved metrics summary → {summary_path}")

def main():
    base_dir = "/Users/hannahfong/Desktop/[FINAL] GCompose/kg_construction"
    for user_folder in os.listdir(base_dir):
        user_path = os.path.join(base_dir, user_folder)
        if os.path.isdir(user_path) and user_folder.endswith("_chunks_sorted.json"):
            build_incremental_kg(user_path)

if __name__ == "__main__":
    main()

"""
def build_incremental_kg(user_dir):
    Build partition-wise KGs incrementally using HippoRAG.
    Each partition builds on the previous one, but a copy of each KG is saved separately.

    user_name = os.path.basename(user_dir)
    print(f"\n🧠 Building KGs for {user_name}")

    # Get partitions in order
    partitions = sorted(
        [f for f in os.listdir(user_dir)
         if f.startswith("KG_train_part_") or f == "KG_val.json"]
    )

    # Base output structure
    base_output_dir = os.path.join(user_dir, "partition_graphs")
    os.makedirs(base_output_dir, exist_ok=True)

    # 1️⃣ Initialize HippoRAG base directory (persistent one)
    persistent_dir = os.path.join(base_output_dir, "working_dir")
    os.makedirs(persistent_dir, exist_ok=True)

    # Load KG init
    kg_init_path = os.path.join(user_dir, "kg_init.json")
    with open(kg_init_path, "r", encoding="utf-8") as f:
        kg_init_docs = json.load(f)
    kg_init_texts = [d["text"] for d in kg_init_docs if "text" in d]

    # Initialize and build the KG init graph
    hipporag = HippoRAG(
        save_dir=persistent_dir,
        llm_model_name="gpt-4o-mini",
        embedding_model_name="text-embedding-3-small",
    )
    hipporag.index(docs=kg_init_texts)

    graph_info = hipporag.get_graph_info()
    metrics = {"KG_init": evaluate_graph(hipporag.graph, graph_info)}
    print(f"✅ KG_init complete: {metrics['KG_init']}")

    # Snapshot KG_init directory
    kg_init_snapshot = os.path.join(base_output_dir, "KG_init")
    shutil.copytree(persistent_dir, kg_init_snapshot, dirs_exist_ok=True)
    visualize_graph(hipporag.graph, os.path.join(kg_init_snapshot, "graph.html"))

    # 2️⃣ Incrementally add partitions
    for p_file in partitions:
        print("PUMASOK BA DITO?????")
        p_name = p_file.replace(".json", "")
        p_path = os.path.join(user_dir, p_file)

        # Load docs for this partition
        with open(p_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
        docs_text = [d["text"] for d in docs if "text" in d]

        # Continue building on same HippoRAG (persistent_dir)
        hipporag.index(docs=docs_text)

        # Evaluate and snapshot
        metrics[p_name] = evaluate_graph(hipporag.graph, graph_info)
        print(f"✅ {user_name} | {p_name}: {metrics[p_name]}")

        # Copy current state as snapshot
        snapshot_dir = os.path.join(base_output_dir, p_name)
        shutil.copytree(persistent_dir, snapshot_dir, dirs_exist_ok=True)
        visualize_graph(hipporag.graph, os.path.join(snapshot_dir, "graph.html"))
    print("I BELONG TO THE ZOO")
    # 3️⃣ Save final metrics summary
    summary_path = os.path.join(base_output_dir, "graph_metrics.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"📊 Saved metrics summary → {summary_path}")
"""