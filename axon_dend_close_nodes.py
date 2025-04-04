# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:07:44 2025
The code aims to find synapse between axon and dendrite.
To do so, we plan to set a distance threshold and find the nodes distance between axon and dendrite.
@author: Songyang

Edit on Mar 23:
    Previous version only created nodes; this version will also add edges.
Edit on Mar 25:
    1. Save flattened groups information to a txt file.
    2. In find_nodes_closeby, catch errors in the loop and report which file caused the issue.
    3. Save the skeleton set after processing each axon.
"""
import os
from pathlib import Path
from webknossos import Skeleton
import numpy as np
import pandas as pd

def commenting_nodes(index_unique, original_tree, new_tree, commentid):
    coordinates_mat = []
    node_mat = []
    # Build the coordinate and node lists based on index_unique
    for index in index_unique:
        coordinates = original_tree.get_node_positions()[index].tolist()
        coordinates_mat.append(coordinates)
        node_mat.append(new_tree.add_node(position=coordinates))
    # For each edge, check if both endpoints exist in the coordinates_mat
    for edge in original_tree.edges:
        edge_position1 = edge[0].position
        edge_position2 = edge[1].position
        candidate1 = [edge_position1.x, edge_position1.y, edge_position1.z]
        candidate2 = [edge_position2.x, edge_position2.y, edge_position2.z]
        if candidate1 in coordinates_mat and candidate2 in coordinates_mat:
            index1 = coordinates_mat.index(candidate1)
            index2 = coordinates_mat.index(candidate2)
            new_tree.add_edge(node_mat[index1], node_mat[index2])

def distance_matrix(axon_skel_nodes, dend_skel_nodes):
    # Calculate pairwise distances between axon and dendrite nodes
    axon_skel_sq = np.sum(axon_skel_nodes**2, axis=1).reshape(-1, 1)
    dend_skel_sq = np.sum(dend_skel_nodes**2, axis=1).reshape(1, -1)
    dist_matrix = np.sqrt(axon_skel_sq + dend_skel_sq - 2 * np.dot(axon_skel_nodes, dend_skel_nodes.T))
    return dist_matrix

def find_nodes_closeby(axon_skel_set, dend_skel_set, max_distance, save_path):
    for axon_skel in axon_skel_set.flattened_trees():
        try:
            combined_name = axon_skel.name
            axon_nuc_id = combined_name.split("_")[0]
            axon_group = axon_skel_set.add_group(f"Axon{axon_nuc_id}")

            # Loop through the dendrites that do not belong to the same axon
            for dend_skel in dend_skel_set.flattened_trees():
                try:
                    if axon_nuc_id not in dend_skel.name:
                        dend_combined_name = dend_skel.name
                        dend_nuc_id = dend_combined_name.split("_")[0]
                        axon_skel_nodes = axon_skel.get_node_positions() * np.array([3.75, 3.75, 50]) / 1000  # convert to µm
                        dend_skel_nodes = dend_skel.get_node_positions() * np.array([3.75, 3.75, 50]) / 1000
                        dist_matrix_val = distance_matrix(axon_skel_nodes, dend_skel_nodes)
                        axon_index, dend_index = np.where(dist_matrix_val < max_distance)
                        axon_index_unique = np.unique(axon_index)
                        dend_index_unique = np.unique(dend_index)
                        if dend_index_unique.any():
                            dend_group = axon_group.add_group(f"with Dend {dend_nuc_id}")
                            newtree = dend_group.add_tree(dend_nuc_id)
                            commenting_nodes(axon_index_unique, axon_skel, newtree, dend_nuc_id)
                            print("Finished axon", axon_nuc_id, "dendrite", dend_nuc_id)
                except Exception as e:
                    print(f"Error processing dendrite file {dend_skel.name}: {e}")
            # Save the updated skeleton set after finishing processing the current axon
            axon_skel_set.save(save_path)
            print(f"Saved axon_skel_set after processing axon {axon_nuc_id}.")
        except Exception as e:
            print(f"Error processing axon file {axon_skel.name}: {e}")

# Define file names (update these with the actual filenames)
file_name_axon = "Consensus_AXON_032525.nml"  # replace with your axon file name
file_name_dend = "Consensus_Dend_032425.nml"    # replace with your dendrite file name
save_name = "Overlap_Axon_032525_2um.nml"

# main_path = "Z:\Dropbox\Dropbox\Chen Lab Team Folder\Projects\Connectomics\Animals\jc105\EM\webknossos_skeleton"
main_path = "/net/claustrum/mnt/data/Dropbox/Chen Lab Dropbox/Chen Lab Team Folder/Projects/Connectomics/Animals/jc105/EM/webknossos_skeleton/Consensus"
file_path_axon = Path(os.path.join(main_path, file_name_axon))
file_path_dend = Path(os.path.join(main_path, file_name_dend))

# Load the skeletons and their sets
axon_skel = Skeleton.load(file_path_axon)
dend_skel = Skeleton.load(file_path_dend)
axon_skel_set = Skeleton.load(file_path_axon)
dend_skel_set = Skeleton.load(file_path_dend)

# Set your max_distance (update this value as needed)
max_distance = 2  # example value in micrometers

# Call the function and pass in the save path so that each axon is saved after processing
find_nodes_closeby(axon_skel_set, dend_skel_set, max_distance, Path(os.path.join(main_path, save_name)))

# Save flattened groups information to a text file instead of printing to console
output_file = Path(os.path.join(main_path, "groups_output.txt"))
with open(output_file, "w") as f:
    for groups in axon_skel_set.flattened_groups():
        f.write(f"{groups.name}\n")
        for dendgroup in groups.flattened_groups():
            for tree in dendgroup.flattened_trees():
                f.write(f"{tree}\n")
