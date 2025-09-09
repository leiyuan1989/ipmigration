import argparse
from typing import Dict, List

import networkx as nx
import matplotlib.pyplot as plt

from read_layout import extract_layout_data


def rectangles_overlap(a: Dict, b: Dict, include_edge_touch: bool = False) -> bool:
	"""
	Return True if axis-aligned rectangles a and b overlap.
	Each dict must have keys: LLX, LLY, URX, URY.

	include_edge_touch=False requires positive-area overlap.
	If True, touching at edges/corners counts as overlap.
	"""
	ax1, ay1, ax2, ay2 = a["LLX"], a["LLY"], a["URX"], a["URY"]
	bx1, by1, bx2, by2 = b["LLX"], b["LLY"], b["URX"], b["URY"]

	if include_edge_touch:
		return not (ax2 < bx1 or bx2 < ax1 or ay2 < by1 or by2 < ay1)
	else:
		return not (ax2 <= bx1 or bx2 <= ax1 or ay2 <= by1 or by2 <= ay1)


def build_mos_overlap_graph(layout_data: Dict[str, List[Dict]], include_edge_touch: bool = False) -> nx.Graph:
	"""
	Build an undirected graph where nodes are MOS devices (PMOS+NMOS)
	and edges connect devices whose bounding boxes overlap.
	"""
	mos_devices: List[Dict] = (layout_data.get("pmos", []) or []) + (layout_data.get("nmos", []) or [])
	G = nx.Graph()

	# Add nodes with useful attributes
	for comp in mos_devices:
		G.add_node(
			comp["Comp_Name"],
			type=comp.get("Type", ""),
			llx=comp["LLX"],
			lly=comp["LLY"],
			urx=comp["URX"],
			ury=comp["URY"],
			x=comp.get("X"),
			y=comp.get("Y"),
			rotate=comp.get("Rotate"),
			length=comp.get("Length"),
			width=comp.get("Width"),
		)

	# Brute-force pairwise overlap check (sufficient for modest sizes)
	for i in range(len(mos_devices)):
		for j in range(i + 1, len(mos_devices)):
			if rectangles_overlap(mos_devices[i], mos_devices[j], include_edge_touch=include_edge_touch):
				G.add_edge(mos_devices[i]["Comp_Name"], mos_devices[j]["Comp_Name"])

	return G


def _compute_positions(layout_data: Dict[str, List[Dict]]) -> Dict[str, tuple]:
	"""Compute node positions from device centers (X,Y) or box centers."""
	positions: Dict[str, tuple] = {}
	for comp in (layout_data.get("pmos", []) or []) + (layout_data.get("nmos", []) or []):
		name = comp["Comp_Name"]
		x = comp.get("X")
		y = comp.get("Y")
		if x is None or y is None:
			x = (comp["LLX"] + comp["URX"]) / 2.0
			y = (comp["LLY"] + comp["URY"]) / 2.0
		positions[name] = (x, y)
	return positions


def visualize_mos_graph(G: nx.Graph, layout_data: Dict[str, List[Dict]], save_path: str = "mos_overlap_graph.png") -> None:
	"""Visualize the MOS overlap graph and save to file."""
	pos = _compute_positions(layout_data)

	plt.style.use('default')
	fig, ax = plt.subplots(figsize=(14, 10))

	# Node coloring by type
	node_colors = []
	for n in G.nodes:
		t = G.nodes[n].get("type", "")
		node_colors.append("#2E86AB" if t == "pmos3v" else ("#A23B72" if t == "nmos3v" else "#555555"))

	nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#999999", width=1.2, alpha=0.8)
	nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=220)
	nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

	ax.set_title("MOS Overlap Graph (PMOS/NMOS)")
	ax.set_axis_off()
	plt.tight_layout()
	plt.savefig(save_path, dpi=300, bbox_inches='tight')
	plt.close(fig)


# ---- Grouping and endpoint analysis ----

def compute_groups(G: nx.Graph) -> List[List[str]]:
	"""Return connected components as groups (list of node lists)."""
	return [sorted(list(comp)) for comp in nx.connected_components(G)]


def compute_endpoints(G: nx.Graph, groups: List[List[str]]) -> Dict[int, List[str]]:
	"""Return mapping group_index -> list of endpoint node names (degree==1)."""
	group_endpoints: Dict[int, List[str]] = {}
	for idx, nodes in enumerate(groups):
		ends = []
		for n in nodes:
			if G.degree[n] == 1:
				ends.append(n)
		group_endpoints[idx] = sorted(ends)
	return group_endpoints


def _edge_coords(G: nx.Graph, n: str) -> Dict[str, float]:
	"""Return bounding box edge coordinates for node n."""
	data = G.nodes[n]
	return {
		"left": data["llx"],
		"right": data["urx"],
		"bottom": data["lly"],
		"top": data["ury"],
	}


def _aligned(a: float, b: float, tol: float) -> bool:
	return abs(a - b) <= tol


def find_cross_group_endpoint_alignments(G: nx.Graph, groups: List[List[str]], tol: float) -> List[Dict]:
	"""
	For every pair of groups, check if any endpoint pairs have aligned edges.
	Return a list of matches with detail strings like "M1.right == M7.left".
	"""
	matches: List[Dict] = []
	# Precompute endpoints per group
	group_endpoints = compute_endpoints(G, groups)
	for i in range(len(groups)):
		for j in range(i + 1, len(groups)):
			for u in group_endpoints[i]:
				for v in group_endpoints[j]:
					ae = _edge_coords(G, u)
					be = _edge_coords(G, v)
					details: List[str] = []
					# Compare vertical edges (x): left/right vs left/right
					for da in ("left", "right"):
						for db in ("left", "right"):
							if _aligned(ae[da], be[db], tol):
								details.append(f"{u}.{da} == {v}.{db}")
					# Compare horizontal edges (y): top/bottom vs top/bottom
					for da in ("top", "bottom"):
						for db in ("top", "bottom"):
							if _aligned(ae[da], be[db], tol):
								details.append(f"{u}.{da} == {v}.{db}")
					if details:
						matches.append({
							"group_a": i,
							"node_a": u,
							"group_b": j,
							"node_b": v,
							"details": details,
						})
	return matches


# ---- Visualization of groups and alignments ----

def visualize_groups_and_alignments(
	G: nx.Graph,
	layout_data: Dict[str, List[Dict]],
	groups: List[List[str]],
	matches: List[Dict],
	save_path: str = "mos_groups_alignments.png",
) -> None:
	pos = _compute_positions(layout_data)
	plt.style.use('default')
	fig, ax = plt.subplots(figsize=(16, 12))

	# A palette of distinct colors; will cycle if groups > palette size
	palette = [
		"#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
		"#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
	]

	# Draw edges in light gray first
	nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc", width=1.0, alpha=0.7)

	# Draw nodes per group in group color
	for gi, nodes in enumerate(groups):
		color = palette[gi % len(palette)]
		nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color, node_size=240, ax=ax, label=f"Group {gi}")

	# Labels
	nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

	# Overlay alignment connectors in dashed red
	for m in matches:
		u = m["node_a"]
		v = m["node_b"]
		if u in pos and v in pos:
			ux, uy = pos[u]
			vx, vy = pos[v]
			ax.plot([ux, vx], [uy, vy], linestyle='--', color='red', linewidth=1.5, alpha=0.8)
			# Annotate first detail near midpoint
			if m["details"]:
				mx = (ux + vx) / 2.0
				my = (uy + vy) / 2.0
				ax.text(mx, my, m["details"][0], fontsize=7, color='red', ha='center', va='center',
					bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.6))

	ax.set_title("MOS Groups and Cross-Group Endpoint Alignments")
	ax.legend(loc='upper right', fontsize=9)
	ax.set_axis_off()
	plt.tight_layout()
	plt.savefig(save_path, dpi=300, bbox_inches='tight')
	plt.close(fig)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Build MOS overlap graph from layout data.")
	parser.add_argument(
		"-i", "--input", default="layout_data.txt", help="Path to layout data text file"
	)
	parser.add_argument(
		"--include-edge-touch", action="store_true", help="Count edge/corner touching as overlap"
	)
	parser.add_argument(
		"-o", "--output", default="", help="Optional path to save edge list ('.edgelist')"
	)
	parser.add_argument(
		"-p", "--plot", default="mos_overlap_graph.png", help="Path to save visualization image"
	)
	parser.add_argument(
		"--align-tol", type=float, default=0.0, help="Tolerance for edge alignment comparisons"
	)
	parser.add_argument(
		"--groups-plot", default="mos_groups_alignments.png", help="Path to save groups/alignment visualization"
	)
	args = parser.parse_args()

	layout_data = extract_layout_data(args.input)
	G = build_mos_overlap_graph(layout_data, include_edge_touch=args.include_edge_touch)

	print(f"MOS nodes: {G.number_of_nodes()} | Overlap edges: {G.number_of_edges()}")

	# Print a brief listing of edges
	for u, v in list(G.edges())[:50]:
		print(f"EDGE: {u} -- {v}")
	if G.number_of_edges() > 50:
		print(f"... ({G.number_of_edges() - 50} more edges)")

	# Grouping summary
	groups = compute_groups(G)
	print(f"Groups (connected components): {len(groups)}")
	for idx, nodes in enumerate(groups):
		print(f"  Group {idx}: size={len(nodes)}")

	# Endpoints per group
	group_endpoints = compute_endpoints(G, groups)
	for idx in range(len(groups)):
		ends = group_endpoints[idx]
		print(f"  Group {idx} endpoints ({len(ends)}): {', '.join(ends) if ends else 'None'}")

	# Cross-group endpoint edge alignments
	matches = find_cross_group_endpoint_alignments(G, groups, tol=args.align_tol)
	if matches:
		print("Cross-group endpoint edge alignments (within tolerance):")
		for m in matches:
			for d in m["details"]:
				print(f"  Group {m['group_a']}:{m['node_a']}  ||  Group {m['group_b']}:{m['node_b']}  =>  {d}")
	else:
		print("No cross-group endpoint edge alignments found.")

	# Optional save of edge list
	if args.output:
		nx.write_edgelist(G, args.output, data=False)
		print(f"Saved edge list to: {args.output}")

	# Always save visualizations
	visualize_mos_graph(G, layout_data, save_path=args.plot)
	print(f"Saved graph visualization to: {args.plot}")

	visualize_groups_and_alignments(G, layout_data, groups, matches, save_path=args.groups_plot)
	print(f"Saved groups/alignment visualization to: {args.groups_plot}")