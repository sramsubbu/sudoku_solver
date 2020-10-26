from . import grid


class Solver:
    def __init__(self, grd):
        self.grid = grd
        self.probs = self._get_probs()

    def infer_stats(self, stats):
        puzzle = stats['all_values']
        filled = stats['filled']
        solved = filled - puzzle
        unsolved_capacity = 81 - puzzle
        solved_percent = (solved / unsolved_capacity ) * 100
        solved_percent = round(solved_percent, 3)
        print('Solved: ', solved)
        print('Solved percent: ', solved_percent)      

    def solve(self, strategy='solve_single_probs'):
        singles = 81
        while singles > 0:
            singles = self._solve_single_probs()
            self.probs = self._get_probs()
            stats = self.grid._get_stats()
            self.infer_stats(stats)
            
        if self.grid.is_solved():
            print("Solved")
        else:
            print("Puzzle is unsolved")
            
    def _solve_single_probs(self):
        singles = [(idx, value) for idx, value in self.probs.items() if len(value) == 1]
        for key, value in singles:
            v = value.copy()
            val = v.pop()
            self.grid[key] = val
        print(singles)
        return len(singles)

    def _get_probs(self):
        grd = self.grid
        probs = {}
        indices = [grid.GridPos(i, j) for i in range(9) for j in range(9)]
        for index in indices:
            if grd[index] is not None:
                continue
            probs[index] = set(range(1, 10))

        for index, value in probs.items():
            row = grd.get_row(index.row)
            for item in row:
                try:
                    value.remove(item)
                except KeyError:
                    pass
                
            col = grd.get_col(index.col)
            for item in col:
                try:
                    value.remove(item)
                except KeyError:
                    pass
                
            box = grd.get_box(index.box)
            for item in box:
                try:
                    value.remove(item)
                except KeyError:
                    pass

        return probs

            
    
    
        
