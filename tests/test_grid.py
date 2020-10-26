import pytest
# from sdk_solver.grid import *

from sdk_solver import grid as grd


def test_grid_pos():
    cell = grd.GridPos(1, 1)
    assert cell.row, cell.col == (1, 1)

    with pytest.raises(ValueError):
        cell = grd.GridPos(1, 9)

    with pytest.raises(ValueError):
        cell = grd.GridPos(-1, 1)

    # eqs
    cells = [(1, 1), (2, 2), (0, 1), (4, 5), (3, 3)]
    cells = [grd.GridPos(*item) for item in cells]
    assert cells[0] != cells[1]
    assert not (cells[0] == cells[1])
    cells.sort()


def test_grid_view():
    grid = grd.Grid()
    indices = [(1, 1), (2, 2), (3, 3)]
    indices = [grd.GridPos(*idx) for idx in indices]
    view = grd.View(grid, indices)
    item = view[0]
    assert item is grid[indices[0]]


def test_grid():
    grid = grd.Grid()
    assert grid._is_valid_grid()
