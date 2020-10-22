import pytest
from sdk_solver.grid import *


def test_grid_pos():
    cell = GridPos(1,1)
    assert cell.row, cell.col == (1,1)

    with pytest.raises(ValueError):
        cell = GridPos(1,9)

    with pytest.raises(ValueError):
        cell = GridPos(-1, 1)

    # eqs
    cells = [(1,1), (2,2), (0,1), (4,5), (3,3)]
    cells = [GridPos(*item) for item in cells]
    cells.sort()


def test_grid_view():
    grid = Grid()
    indices = [(1,1), (2,2), (3,3)]
    indices = [GridPos(*idx) for idx in indices]
    view = View(grid, indices)
    item = view[0]
    assert item is grid[indices[0]]


def test_grid():
    grid = Grid()
    assert grid._is_valid_grid()
