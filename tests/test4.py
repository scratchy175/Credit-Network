def draw_multigraph_edge_labels(G, pos, edge_labels=None, font_size=10, ax=None):
    """
    Draw edge labels for a MultiDiGraph, handling multiple edges between the same nodes.

    Parameters
    ----------
    G : MultiDiGraph
        A NetworkX MultiDiGraph
    pos : dict
        Node positions in a dictionary keyed by node.
    edge_labels : dict, optional
        Edge labels in a dictionary keyed by edge three-tuple (u, v, key).
    font_size : int, optional
        Font size for edge labels.
    ax : matplotlib Axes, optional
        The axes to draw on.

    """
    if ax is None:
        ax = plt.gca()

    if edge_labels is None:
        edge_labels = {(u, v, k): G[u][v][k] for u, v, k in G.edges(keys=True)}

    for (u, v, k), label in edge_labels.items():
        # Position for the edge label
        edge_midpoint = [(x + y) / 2 for x, y in zip(pos[u], pos[v])]
        label_pos = (edge_midpoint[0], edge_midpoint[1] + 0.1 * k)  # Offset based on the edge key

        # Draw the edge label
        ax.text(label_pos[0], label_pos[1], label, fontsize=font_size)



def animate_multigraph_removal(G, interval=1000, repeat=False):
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G)  # Layout of the nodes

    # Function to update the plot for each frame
    def update(num):
        if G.number_of_edges() > 0:
            edge_list = list(G.edges(keys=True, data=True))
            edge = edge_list[0]
            G.remove_edge(*edge[:3])
            ax.clear()
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=500)
            nx.draw_networkx_labels(G, pos, ax=ax)
            for u, v, k, data in edge_list:
                # Draw each edge
                draw_multigraph_edge_labels(G, pos)

                #nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v, k)],connectionstyle=f'arc3,rad={0.1*k}')
                # Position for the edge label
                edge_midpoint = [(x + y) / 2 for x, y in zip(pos[u], pos[v])]
                label_pos = (edge_midpoint[0], edge_midpoint[1] + 0.1*k)
                # Draw the edge label
                ax.text(label_pos[0], label_pos[1], data['label'], fontsize=8)
            ax.set_title(f"Frame {num} - Edges Remaining: {G.number_of_edges()}")
        else:
            anim.event_source.stop()

    # Create the animation
    anim = animation.FuncAnimation(fig, update, interval=interval, repeat=repeat)
    
    plt.show()

# Example usage
# G = your graph object
animate_multigraph_removal(G)