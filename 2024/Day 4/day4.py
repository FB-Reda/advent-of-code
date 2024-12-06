def read_grid(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    # Lines now contains the puzzle input lines (no empty lines)
    # For this puzzle, each line should be a row of the word search
    grid = [list(line) for line in lines]
    return grid


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def find_all_xmas(grid):
    # Directions to search (dr, dc) for XMAS
    # We'll look for sequence X, M, A, S in each direction
    directions = [
        (-1, 0),  # up
        (1, 0),  # down
        (0, -1),  # left
        (0, 1),  # right
        (-1, -1),  # up-left diagonal
        (-1, 1),  # up-right diagonal
        (1, -1),  # down-left diagonal
        (1, 1)  # down-right diagonal
    ]

    target = "XMAS"
    length = len(target)
    count = 0

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == target[0]:
                # Check each direction
                for dr, dc in directions:
                    rr, cc = r, c
                    found = True
                    for k in range(length):
                        nr, nc = rr + dr * k, cc + dc * k
                        if not in_bounds(grid, nr, nc) or grid[nr][nc] != target[k]:
                            found = False
                            break
                    if found:
                        count += 1
    return count


def find_all_x_mas(grid):
    # For part 2, we want to find the "X-MAS" pattern, which is:
    #    M . S
    #    . A .
    #    M . S
    # or variations due to MAS or SAM being allowed on each diagonal.
    # Let's break down what we need:
    #
    # Let the center of the X be at (r, c) and that cell must be 'A'.
    # We consider the cells:
    # top-left (r-1, c-1), bottom-right (r+1, c+1)
    # top-right (r-1, c+1), bottom-left (r+1, c-1)
    #
    # Each diagonal must form either MAS or SAM with the center 'A' at (r, c).
    # That means:
    # On one diagonal: either (M at top-left and S at bottom-right) or (S at top-left and M at bottom-right)
    # On the other diagonal: same logic.
    #
    # We only check cells if they are in range.

    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] == 'A':
                # Coordinates of diagonals:
                tl = (r - 1, c - 1)
                br = (r + 1, c + 1)
                tr = (r - 1, c + 1)
                bl = (r + 1, c - 1)

                if (in_bounds(grid, tl[0], tl[1]) and in_bounds(grid, br[0], br[1]) and
                        in_bounds(grid, tr[0], tr[1]) and in_bounds(grid, bl[0], bl[1])):
                    # Check diagonal 1 (tl to br)
                    # Possible patterns: M-A-S or S-A-M
                    diag1 = (grid[tl[0]][tl[1]], 'A', grid[br[0]][br[1]])
                    # diag1 should contain 'A' as the center, which it is by definition
                    # we only check ends: (M,S) or (S,M)
                    valid_diag1 = (diag1[0] == 'M' and diag1[2] == 'S') or (diag1[0] == 'S' and diag1[2] == 'M')

                    # Check diagonal 2 (tr to bl)
                    diag2 = (grid[tr[0]][tr[1]], 'A', grid[bl[0]][bl[1]])
                    valid_diag2 = (diag2[0] == 'M' and diag2[2] == 'S') or (diag2[0] == 'S' and diag2[2] == 'M')

                    if valid_diag1 and valid_diag2:
                        count += 1
    return count


def main():
    grid = read_grid("input.txt")

    # Part 1: Count occurrences of "XMAS"
    part_1_count = find_all_xmas(grid)
    print("Part 1: Number of XMAS occurrences =", part_1_count)

    # Part 2: Count occurrences of "X-MAS"
    part_2_count = find_all_x_mas(grid)
    print("Part 2: Number of X-MAS occurrences =", part_2_count)


if __name__ == "__main__":
    main()
