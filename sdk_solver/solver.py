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
        def optimal_strategy():
            solved = 0
            solved += self._solve_single_probs()
            solved += self._fix_single_pos_values()
            return solved
        singles = 81
        if strategy == 'solve_single_probs':
            func = self._solve_single_probs
        elif strategy == 'fix_single_possibs':
            func = self._fix_single_pos_values
        elif strategy == 'optimal':
            func = optimal_strategy
        else:
            func = optimal_strategy
        while singles > 0:
            singles = func()
            self.probs = self._get_probs()
            stats = self.grid._get_stats()
            self.infer_stats(stats)
            
        if self.grid.is_solved():
            print("Solved")
        else:
            print("Puzzle is unsolved")

    def _fix_single_pos_values(self):
        def calc_prob_histogram(row=None, col=None, box=None):
            if row is not None:
                filter_func = lambda pos: pos.row == row
            elif col is not None:
                filter_func = lambda pos: pos.col == col
            elif box is not None:
                filter_func = lambda pos: pos.box == box
            else:
                raise ValueError("Require a value for either row, col or box")
            required_values = [item for item in self.probs.items() if filter_func(item[0])]
            required_values = dict(required_values)
            all_values = range(1,10)
            prob_histogram = {}
            for value in all_values:
                hist = [pos for pos, prob in required_values.items() if value in prob ]
                prob_histogram[value] = hist
            return prob_histogram

        # calc histograms for all rows
        row_histogram = [calc_prob_histogram(i) for i in range(9)]
        solved_count = 0 
        for hist in row_histogram:
            for value, cells in hist.items():
                if len(cells) == 1:
                    self.grid[cells[0]] = value
                    solved_count += 1
        self.probs = self._get_probs()
        return solved_count
                
        
            
    def _solve_single_probs(self):
        singles = [(idx, value) for idx, value in self.probs.items() if len(value) == 1]
        for key, value in singles:
            v = value.copy()
            val = v.pop()
            self.grid[key] = val
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

            
    
    
        
