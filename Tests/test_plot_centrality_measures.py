import pytest
import networkx as nx
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, box

def test_plot_centrality_measures():

    # A simple square polygon
    poly = box(0, 0, 10, 10)
    gdf = gpd.GeoDataFrame({"name": ["bg"], "geometry": [poly]}, crs="EPSG:4326")


    G= nx.Graph()
    G.add_edges_from([
        (1, 2), (2, 3), (3, 1), (3, 4), (4, 5)])
    

    pos = {
            1: (2, 2),
            2: (4, 3),
            3: (3, 5),
            4: (6, 6),
            5: (8, 7),
        }

    def plot_centrality_measures(G, pos, borough_gdf):

    # Always safe centrality measures
        deg = nx.degree_centrality(G)
        close = nx.closeness_centrality(G)
        bet = nx.betweenness_centrality(G)
        eig = nx.eigenvector_centrality(G)
        pagerank = nx.pagerank(G)

        measures = [deg, close, bet, eig, pagerank]
        measure_names = [
            'Degree Centrality',
            'Closeness Centrality',
            'Betweenness Centrality',
            'Eigenvector Centrality',
            'PageRank',
        ]

        # Try eccentricity only if graph is connected
        try:
            if nx.is_connected(G.to_undirected()):
                ecc = nx.eccentricity(G)
                measures.append(ecc)
                measure_names.append('Eccentricity')
        except nx.NetworkXError:
            print("⚠️ Graph is not connected — skipping eccentricity.")

    plot_centrality_measures(G, pos, gdf)