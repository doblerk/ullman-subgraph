import networkx as nx
import numpy as np
from typing import List


class UllmanAlgorithm:

    def __init__(self,
                 g1: nx.Graph,
                 g2: nx.Graph) -> None:
        self.g1 = g1
        self.g2 = g2
        self.A1 = nx.adjacency_matrix(g1, nodelist=sorted(g1.nodes())).todense()
        self.A2 = nx.adjacency_matrix(g2, nodelist=sorted(g2.nodes())).todense()
        self.num_nodes_g1 = g1.number_of_nodes()
        self.num_nodes_g2 = g2.number_of_nodes()
    
    def init_future_matching_table(self) -> np.ndarray:
        degrees_g1 = np.array([deg for (_, deg) in sorted(self.g1.degree())])
        degrees_g2 = np.array([deg for (_, deg) in sorted(self.g2.degree())])
        return np.repeat(degrees_g1, self.num_nodes_g2).reshape(self.num_nodes_g1, self.num_nodes_g2) <= degrees_g2.T
    
    def update_F(self,
                 F: np.ndarray,
                 row: int,
                 col: int) -> None:
        F[row, :] = 0
        F[:, col] = 0
        F[row, col] = 1
    
    def is_F_valid_isomorphism(self,
                               F: np.ndarray) -> bool:
        return np.all(F.sum(axis=1) == 1) and np.all(F.sum(axis=0) <= 1)
    
    def check_constraint(self,
                         F: np.ndarray,
                         row: int,
                         col: int,
                         unmapped_rows: List[int],
                         unmapped_cols: List[int]) -> None:
        for wi in unmapped_rows:
            for wj in unmapped_cols:
                if F[wi, wj] == 1 and (self.A1[row, wi] != self.A2[col, wj]):
                    F[wi, wj] = 0
    
    def ullman_recursive(self,
                         F: np.ndarray, 
                         row: int, 
                         col: int) -> bool:
        
        if row == self.num_nodes_g1:
            return self.is_F_valid_isomorphism(F)
        
        available_columns = [col] if row == 0 else np.argwhere(F[row, :] == 1).flatten()

        for v in available_columns:
            F_tmp = np.copy(F)
            
            self.update_F(F_tmp, row, v)
            
            unmapped_rows = list(range(row + 1, len(F_tmp)))
            unmapped_cols = list(np.setdiff1d(list(range(F_tmp.shape[1])), [v]))

            self.check_constraint(F_tmp, row, v, unmapped_rows, unmapped_cols)

            if np.any(np.sum(F_tmp, axis=1) == 0):
                # backtrack
                continue
            
            if self.ullman_recursive(F_tmp, row + 1, v):
                return True
        
        return False

    def is_subgraph_isomorphic(self) -> bool:
        if self.num_nodes_g1 > self.num_nodes_g2:
            return False
        
        F = self.init_future_matching_table()

        available_columns = np.argwhere(F[0, :] == 1)

        for col in available_columns:
            if self.ullman_recursive(F, 0, col):
                return True
    
        return False