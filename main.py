from enum import Enum
import argparse

class Shape(Enum):
    Q = [[True, True], [True, True]]
    Z = [[True, True, False], [False, True, True]]
    S = [[False, True, True], [True, True, False]]
    T = [[True, True, True], [False, True, False]]
    I = [[True, True, True, True]]
    L = [[True, False], [True, False], [True, True]]
    J = [[False, True], [False, True], [True, True]]

class Grid:
    HEIGHT = 100
    WIDTH = 10

    def __init__(self):
        self.grid = [[False for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        
    def has_full_row(self) -> bool:
        for row in reversed(self.grid):
            if all(row): return True
        return False

    def clear_filled_rows(self):
        for row, i in [(row, i) for i, row in enumerate(self.grid) if all(row)]:
            self.grid.pop(i)
            self.grid.insert(0, [False for _ in range(self.WIDTH)])
        if self.has_full_row(): self.clear_filled_rows()

    def can_place_shape(self, shape_2d: list, row: int, col: int) -> bool:
        return not any(
            space and self.grid[row + i][col + j] for i, row_2d in enumerate(shape_2d) for j, space in enumerate(row_2d)
        )

    def drop_shape(self, shape: Shape, col: int):
        placement_row = None
        for row in range(self.HEIGHT - len(shape.value) + 1):
            if not self.can_place_shape(shape.value, row, col):
                placement_row = row - 1
                break
        if not placement_row: placement_row = self.HEIGHT - len(shape.value)

        for i, row in enumerate(shape.value):
            for j, space in enumerate(row):
                self.grid[placement_row + i][col + j] |= space
    
    def get_height(self) -> int:
        for i, row in enumerate(reversed(self.grid)):
            if all(not space for space in row): return i

    def __str__(self):
        return '\n'.join([''.join(['X' if space else '_' for space in row]) for row in self.grid])
    
        
def main(input_file: str, output_file: str):
    with open(input_file, 'r') as file:
        output = []
        for line in file:
            if not line: continue
            grid = Grid()
            split = line.strip().split(',')
            for segment in split:
                shape, i = Shape[segment[0]], segment[1:]
                grid.drop_shape(shape, int(i))
                grid.clear_filled_rows()
            output.append(grid.get_height())
        with open(output_file, 'w') as file:
            file.write('\n'.join(map(str, output)))
        print("\n".join(map(str, output)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tetris')
    parser.add_argument('--input', help='<input file path>')
    parser.add_argument('--output', help='<output file path>')
    args = parser.parse_args()
    args.input = args.input or "input.txt"
    args.output = args.output or "output.txt"

    main(args.input, args.output)