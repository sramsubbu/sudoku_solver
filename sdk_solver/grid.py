from typing import List, Dict, Optional

from collections import Counter


class GridPos:
    def __init__(self, row: int, col: int):
        self.check_grid_vals(row, col)
        self.row = row
        self.col = col

    def __hash__(self):
        return hash((self.row, self.col))

    @staticmethod
    def is_grid_vals(row: int, col: int):
        if row not in range(9):
            return False
        if col not in range(9):
            return False
        return True

    @property
    def box(self):
        r = self.row // 3
        c = self.col // 3
        ret = (r*3) + c
        return ret

    @staticmethod
    def check_grid_vals(row: int, col: int):
        if not GridPos.is_grid_vals(row, col):
            raise ValueError("Invalid grid cell values: '{row},{col}'")

    def __eq__(self, other) -> bool:
        assert isinstance(other, GridPos), f"Required a GridPos instance. Provided '{type(other)}': {other}"
        return (self.row, self.col) == (other.row, other.col)

    def __lt__(self, other) -> bool:
        assert isinstance(other, GridPos), f"Required a GridPos instance. Provied '{type(other)}': {other}"
        return (self.row, self.col) < (other.row, other.col)

    def __repr__(self) -> str:
        return f"GridPos({self.row, self.col})"


class Grid:
    def __init__(self):
        self.grid = self._get_empty_grid()
        self._puzzle = []
        self._puzzle_set= False

    def _get_empty_grid(self):
        grid = [None]*9
        for i in range(9):
            grid[i] = [None]*9
        return grid

    def _get_stats(self):
        stats = {}
        total = len(self.grid) * len(self.grid[0])
        all_values = len(self._puzzle)
        filled = [item for row in self.grid for item in row if item is not None]
        num_counts = Counter(self._puzzle)
        stats['total'] = total
        stats['all_values'] = all_values
        stats['num_counts'] = num_counts
        stats['filled'] = len(filled)
        return stats        

    def __str__(self):
        ret = []
        for row in self.grid:
            row_s = [str(item) if item else '_' for item in row]
            row_s.insert(6, '|')
            row_s.insert(3, '|')
            row_s.append('|')
            row_s = ' '.join(row_s)
            ret.append(row_s)
        row_sep = '-'*23
        ret.insert(6, row_sep)
        ret.insert(3, row_sep)
        return '\n'.join(ret)

    def __getitem__(self, idx: GridPos):
        self.is_valid_grid_cell(idx)
        row, col = idx.row, idx.col
        return self.grid[row][col]

    def __setitem__(self, idx: GridPos, value: int):
        self.is_valid_grid_cell(idx)
        if value not in range(1, 10):
            raise ValueError("given value is not in range 1 and 9")
        if idx in self._puzzle:
            raise ValueError("cell part of the puzzle")
        row, col = idx.row, idx.col
        old_val = self.grid[row][col]
        self.grid[row][col] = value
        if not self._is_valid_grid():
            self.grid[row][col] = old_val
            raise ValueError("constraint error. cannot set value at pos")

    def is_valid_grid_cell(self, idx):
        if not isinstance(idx, GridPos):
            raise ValueError("given index is not a valid grid pos")

    def check_index(self, index: int):
        if index not in range(9):
            raise ValueError("Given index is not valid")    

    def get_row(self, row: int) -> List[int]:
        self.check_index(row)
        indices = [GridPos(row, i) for i in range(9)]
        row_view = View(self, indices)
        return row_view.as_immutable_object()

    def get_col(self, col: int) -> List[int]:
        self.check_index(col)
        indices = [GridPos(i, col) for i in range(9)]
        col_view = View(self, indices)
        return col_view.as_immutable_object()

    def get_box(self, box: int) -> List[int]:
        self.check_index(box)
        
        def start_index(box):
            box_lookup = [(0, 0), (0, 3), (0, 6),
                          (3, 0), (3, 3), (3, 6), 
                          (6, 0), (6, 3), (6, 6)]
            return box_lookup[box]
        
        start_r, start_c = start_index(box)
        indices = [GridPos(i, j) for i in range(start_r, start_r+3)
                   for j in range(start_c, start_c+3)]
        view = View(self, indices)
        return view.as_immutable_object()

    @classmethod
    def from_sparce_matrix(cls, sparce_matrix):
        obj = cls()
        for pos, value in sparce_matrix.items():
            pos = GridPos(*pos)
            obj[pos] = value
        indices = [GridPos(i,j) for i in range(9) for j in range(9)]
        puzzle = [item for item in indices if obj[item] is not None]
        obj._puzzle = puzzle
        obj._puzzle_set = True
        return obj
           
    def is_solved(self) -> bool:
        for row in self.grid:
            for item in row:
                if item is None:
                    return False
        return True

    def _is_valid_grid(self) -> bool:
        rows = [self.get_row(i) for i in range(9)]
        cols = [self.get_col(i) for i in range(9)]
        boxes = [self.get_box(i) for i in range(9)]
        for row in rows:
            cr = [item for item in row if item]
            if len(cr) != len(set(cr)):
                return False
        for col in cols:
            cc = [item for item in col if item]
            if len(cc) != len(set(cc)):
                return False
        
        for box in boxes:
            cb = [item for item in box if item]
            if len(cb) != len(set(cb)):
                return False
        return True

    
class View:
    def __init__(self, grid: Grid, indices: List[GridPos]):
        self._grid = grid
        self._indices = indices

    def __getitem__(self, idx: int):
        index = self._indices[idx]
        return self._grid[index]

    def __setitem__(self, idx: int, value: int):
        index = self._indices[idx]
        self._grid[index] = value

    def __len__(self):
        return len(self._indices)

    def as_immutable_object(self) -> List[int]:
        return [item for item in self]


def parse_puzzle_file(filepath: str):
    with open(filepath) as fp:
        lines = [line for line in fp]
    puzzle_lines = [line for line in lines if not line.startswith('-')]
    puzzle_rows = [line.split() for line in puzzle_lines]
    cleaned_rows = []
    for row in puzzle_rows:
        new_row = [item for item in row if item != '|' ]
        cleaned_rows.append(new_row)

    sparce_matrix = {}
    for i, row in enumerate(cleaned_rows):
        for j, val in enumerate(row):
            if val != '_':
                sparce_matrix[(i, j)] = int(val)
          
    return sparce_matrix


def grid_from_puzzle_file(filepath: str):
    sparce_matrix = parse_puzzle_file(filepath)
    return Grid.from_sparce_matrix(sparce_matrix)

