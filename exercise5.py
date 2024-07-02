import numpy as np

from typing import List


def get_cell_list_1d(particle_pos: List[list], l_bound: int, u_bound: int, cell_side: int):
    num_cells = int(np.floor((u_bound - l_bound) / cell_side)) + 1
    cell_ids = np.array(((particle_pos - l_bound) // cell_side).astype(int))
    particle_matrix = [
        [idx, pos, cell]
        for idx, (pos, cell) in enumerate(zip(particle_pos, cell_ids))
    ]
    cell_list = [[] for _ in range(num_cells)]
    for i, cell in enumerate(cell_ids):
        cell_list[cell].append(i)
    return particle_matrix, cell_list, num_cells


def get_cell_list_2d(particle_pos: List[list], l_bound: int, u_bound: int, cell_side: int):
    num_cells = int(np.floor((u_bound - l_bound) / cell_side)) + 1
    cell_ids = np.array(((particle_pos - l_bound) // cell_side).astype(int))
    particle_matrix = [
        [idx, pos, cell[0], cell[1]] 
        for idx, (pos, cell) in enumerate(zip(particle_pos, cell_ids))
    ]
    cell_list = [[] for _ in range(num_cells**2)]
    for i, cell in enumerate(cell_ids):
        index = cell[0]*num_cells + cell[1]
        cell_list[index].append(i)
    return particle_matrix, cell_list, num_cells


def get_neighbors_2d(cell_list, particle_matrix, num_cells):
    neighbors = [[] for _ in range(len(particle_matrix))]
    
    for i, _, cell_x, cell_y in particle_matrix:
        neighbor_cells = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= cell_x + dx < num_cells and 0 <= cell_y + dy < num_cells:
                    neighbor_cells.append((cell_x + dx) * num_cells + (cell_y + dy))
        # Collect the particle indices from the neighboring cells
        for cell_index in neighbor_cells:
            for neighbor_index in cell_list[cell_index]:
                if neighbor_index != i:
                    neighbors[i].append(neighbor_index)
    
    return neighbors


def get_neighbors_1d(cell_list, particle_matrix, num_cells):
    neighbors = [[] for _ in range(len(particle_matrix))]
    
    for i, _, cell in particle_matrix:
        neighbor_cells = []
        for dx in [-1, 0, 1]:
            if 0 <= cell + dx < num_cells:
                neighbor_cells.append(cell + dx)
        for cell_index in neighbor_cells:
            for neighbor_index in cell_list[cell_index]:
                if neighbor_index != i:
                    neighbors[i].append(neighbor_index)
    
    return neighbors


def distance_2d(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def distance_1d(pos1, pos2):
    return pos1 - pos2


def get_verlet_list_2d(cell_list, particle_matrix, num_cells, cutoff):
    cell_neighbours = get_neighbors_2d(cell_list, particle_matrix, num_cells)
    verlet = [[] for _ in range(len(particle_matrix))]
    for cell, neighbourhood in enumerate(cell_neighbours):
        for neighbour in neighbourhood:
            if distance_2d(particle_matrix[cell][1], particle_matrix[neighbour][1]) <= cutoff:
                verlet[cell].append(neighbour)
    return verlet


def get_verlet_list_1d(cell_list, particle_matrix, num_cells, cutoff):
    cell_neighbours = get_neighbors_1d(cell_list, particle_matrix, num_cells)
    verlet = [[] for _ in range(len(particle_matrix))]
    for cell, neighbourhood in enumerate(cell_neighbours):
        for neighbour in neighbourhood:
            if distance_1d(particle_matrix[cell][1], particle_matrix[neighbour][1]) <= cutoff:
                verlet[cell].append(neighbour)
    return verlet
