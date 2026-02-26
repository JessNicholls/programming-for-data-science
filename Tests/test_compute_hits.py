import pandas as pd
import networkx as nx
import numpy as np

def compute_hits(hourly_graphs, zones_man):
    valid_nodes = set(zones_man["objectid"].astype(int))
    zone_name_lookup = zones_man.set_index("objectid")["zone"].to_dict()

    records = []
    for h, G_h in hourly_graphs.items():
        G_clean = nx.DiGraph()
        for u, v, data in G_h.edges(data=True):
            if u in valid_nodes and v in valid_nodes:
                G_clean.add_edge(u, v, **data)

        if len(G_clean.nodes()) == 0:
            continue

        hubs, auths = nx.hits(G_clean, max_iter=500, normalized=True)

        for node in G_clean.nodes():
            records.append({
                "hour": h,
                "zone_id": node,
                "zone_name": zone_name_lookup[node],
                "hub_score": hubs.get(node, 0),
                "authority_score": auths.get(node, 0)
            })
    return pd.DataFrame(records)

# Creating synthetic inputs
def _make_zones_man():
    return pd.DataFrame({
        "objectid": [101, 102, 103],
        "zone": ["Midtown", "Chelsea", "SoHo"],
    })

def _make_hourly_graphs():
    G10 = nx.DiGraph()
    G10.add_edge(101, 102)
    G10.add_edge(102, 103)
    G10.add_edge(103, 101)

    G11 = nx.DiGraph()
    G11.add_edge(101, 103)
    G11.add_edge(103, 102)
    G11.add_edge(999, 101)  # invalid node, should be filtered

    G12 = nx.DiGraph()
    G12.add_edge(900, 901)  # all invalid, hour skipped

    return {10: G10, 11: G11, 12: G12}

# The actual test
def test_compute_hits_runs_and_filters():
    zones_man = _make_zones_man()
    hourly_graphs = _make_hourly_graphs()

    df = compute_hits(hourly_graphs, zones_man)

    # Only hours 10 and 11 contribute (12 skipped)
    assert set(df["hour"]) == {10, 11}
    # 3 nodes per contributing hour
    assert len(df) == 6

    # Columns present
    expected_cols = {"hour", "zone_id", "zone_name", "hub_score", "authority_score"}
    assert expected_cols.issubset(df.columns)

    # Only valid nodes included
    assert set(df["zone_id"]).issubset({101, 102, 103})

    # Scores should be finite real numbers (not NaN, not inf)
    assert np.isfinite(df["hub_score"]).all()
    assert np.isfinite(df["authority_score"]).all()

    assert df["hub_score"].abs().sum() > 0
    assert df["authority_score"].abs().sum() > 0