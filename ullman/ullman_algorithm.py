import networkx as nx
import numpy as np
from typing import List


class UllmanAlgorithm:
    """
    A class to perform the Ullman's subgraph isomorphism test.

    This algorithm checks whether graph `g1` is subgraph isomorphic to graph `g2`.

    Attributes:
    -----------
    g1 : nx.Graph
        The source graph.
    g2 : nx.Graph
        The target raph.
    
    Methods:
    --------
    init_feature_matching_table : np.ndarray
    update_F : None
    is_F_valid_isomorphism : bool
    check_constraint : None
    _ullman_recursive : bool
    is_subgraph_isomorphic : bool
    """

    def __init__(self,
                 g1: nx.Graph,
                 g2: nx.Graph) -> None:
        """
        Initializes the UllmanAlgorithm with two graphs.

        Parameters:
        -----------
        g1 : nx.Graph
            The source graph.
        g2 : nx.Graph
             The target graph.
        """
        self.g1 = g1
        self.g2 = g2
        self.A1 = nx.adjacency_matrix(g1, nodelist=sorted(g1.nodes())).todense()
        self.A2 = nx.adjacency_matrix(g2, nodelist=sorted(g2.nodes())).todense()
        self.num_nodes_g1 = g1.number_of_nodes()
        self.num_nodes_g2 = g2.number_of_nodes()
    
    def init_future_matching_table(self) -> np.ndarray:
        """
        Initializes the future matching table `F` based on degree constraints.

        A node in `g1` can only be mapped to a node in `g2` if the degree of 
        the `g1` node is less than or equal to that of the `g2` node.

        Returns:
        --------
        np.ndarray
            A binary matrix representing initial feasible mappings.
        """
        degrees_g1 = np.array([deg for (_, deg) in sorted(self.g1.degree())])
        degrees_g2 = np.array([deg for (_, deg) in sorted(self.g2.degree())])
        return np.repeat(degrees_g1, self.num_nodes_g2).reshape(self.num_nodes_g1, self.num_nodes_g2) <= degrees_g2.T
    
    def update_F(self,
                 F: np.ndarray,
                 row: int,
                 col: int) -> None:
        """
        Updates the future matching table `F` by mapping `row -> col`.

        This sets the entire `row` and `col` to zero except for `F[row, col] = 1`,
        ensuring that `row` is mapped exclusively to `col`.

        Parameters:
        -----------
        F : np.ndarray
            The current future matching table.
        row : int
            The row (node in `g1`) being mapped.
        col : int
            The column (node in `g2`) being assigned.
        """
        F[row, :] = 0
        F[:, col] = 0
        F[row, col] = 1
    
    def is_F_valid_isomorphism(self,
                               F: np.ndarray) -> bool:
        """
        Checks if the future matching table `F` represents a valid isomorphism.

        Conditions:
        -----------
        - Each row must contain exactly one `1` (each node in `g1` is mapped once).
        - Each column must contain at most one `1` (each node in `g2` is mapped at most once).

        Parameters:
        -----------
        F : np.ndarray
            The current future matching table.

        Returns:
        --------
        bool
            True if `F` is a valid isomorphism, False otherwise.
        """
        return np.all(F.sum(axis=1) == 1) and np.all(F.sum(axis=0) <= 1)
    
    def check_constraint(self,
                         F: np.ndarray,
                         row: int,
                         col: int,
                         unmapped_rows: List[int],
                         unmapped_cols: List[int]) -> None:
        """
        Prunes invalid mappings based on adjacency constraints.

        If `row` is mapped to `col`, then for any unmapped nodes `wi` in `g1` 
        and `wj` in `g2`, if `F[wi, wj] == 1`, then `A1[row, wi]` must match `A2[col, wj]`.
        If the constraint is violated, `F[wi, wj]` is set to 0.

        Parameters:
        -----------
        F : np.ndarray
            The current future matching table.
        row : int
            The row (node in `g1`) being mapped.
        col : int
            The column (node in `g2`) being assigned.
        unmapped_rows : List[int]
            Indices of unmapped rows in `g1`.
        unmapped_cols : List[int]
            Indices of unmapped columns in `g2`.
        """
        for wi in unmapped_rows:
            for wj in unmapped_cols:
                if F[wi, wj] == 1 and (self.A1[row, wi] != self.A2[col, wj]):
                    F[wi, wj] = 0
    
    def _ullman_recursive(self,
                         F: np.ndarray, 
                         row: int) -> bool:
        """
        Recursive function implementing the Ullman subgraph isomorphism test.

        This function attempts to map `row` from `g1` to columns in `g2`, 
        applying constraints and backtracking when necessary.

        Parameters:
        -----------
        F : np.ndarray
            The current future matching table.
        row : int
            The row (node in `g1`) being mapped.

        Returns:
        --------
        bool
            True if an isomorphic subgraph is found, False otherwise.
        """
        
        if row == self.num_nodes_g1:
            return self.is_F_valid_isomorphism(F)
        
        available_columns = np.where(F[row, :] == 1)[0]

        for col in available_columns:
            F_tmp = np.copy(F)
            
            self.update_F(F_tmp, row, col)
            
            unmapped_rows = list(range(row + 1, len(F_tmp)))
            unmapped_cols = list(np.setdiff1d(list(range(F_tmp.shape[1])), [col]))

            self.check_constraint(F_tmp, row, col, unmapped_rows, unmapped_cols)

            if np.any(np.sum(F_tmp, axis=1) == 0):
                # backtrack
                continue
            
            if self._ullman_recursive(F_tmp, row + 1):
                return True
        
        return False

    def is_subgraph_isomorphic(self) -> bool:
        """
        Determines whether `g1` is subgraph isomorphic to `g2`.

        This function initializes the mapping matrix `F` and starts 
        the recursive Ullman search.

        Returns:
        --------
        bool
            True if `g1` is a subgraph of `g2`, False otherwise.
        """
        if self.num_nodes_g1 > self.num_nodes_g2:
            return False
        
        F = self.init_future_matching_table()

        if self._ullman_recursive(F, 0):
            return True
    
        return False