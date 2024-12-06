import sys
from collections import deque

def parse_rule_line(line):
    before, after = line.split('|')
    return int(before), int(after)

def parse_update_line(line):
    parts = [p.strip() for p in line.split(',')]
    return list(map(int, parts))

def contains_page(pages, page):
    return page in pages

def check_order_for_update(pages, rules):
    # Check all relevant rules
    for (X, Y) in rules:
        if X in pages and Y in pages:
            posX = pages.index(X)
            posY = pages.index(Y)
            if posX > posY:
                return False
    return True

def find_middle_page(pages):
    return pages[len(pages)//2]

def topological_sort(pages, rules):
    # Filter rules to only those applicable
    applicable = [(X, Y) for (X, Y) in rules if X in pages and Y in pages]

    # Map page to index for convenience
    page_to_index = {p: i for i, p in enumerate(pages)}
    n = len(pages)

    # Build graph
    adj = [[] for _ in range(n)]
    in_degree = [0]*n

    for (X, Y) in applicable:
        x_idx = page_to_index[X]
        y_idx = page_to_index[Y]
        adj[x_idx].append(y_idx)
        in_degree[y_idx] += 1

    # Kahn's Algorithm
    q = deque(i for i in range(n) if in_degree[i] == 0)
    sorted_indices = []

    while q:
        u = q.popleft()
        sorted_indices.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)

    # Reorder pages
    sorted_pages = [pages[i] for i in sorted_indices]
    return sorted_pages

def main():
    with open("input.txt", "r") as f:
      lines = [l.strip() for l in f.readlines()]

    # Find blank line that separates rules from updates
    blank_index = None
    for i, line in enumerate(lines):
        if line == "":
            blank_index = i
            break

    rule_lines = lines[:blank_index] if blank_index is not None else lines
    update_lines = lines[blank_index+1:] if blank_index is not None else []

    rules = []
    for rl in rule_lines:
        if rl.strip():
            rules.append(parse_rule_line(rl))

    updates = []
    for ul in update_lines:
        if ul.strip():
            updates.append(parse_update_line(ul))

    # Part 1: Find sum of middle pages of correct updates
    sum_of_middles_correct = 0
    incorrect_updates = []

    for u in updates:
        if check_order_for_update(u, rules):
            sum_of_middles_correct += find_middle_page(u)
        else:
            incorrect_updates.append(u)

    # Part 2: For each incorrect update, sort it and sum the middles
    sum_of_middles_incorrect = 0
    for iu in incorrect_updates:
        sorted_u = topological_sort(iu, rules)
        sum_of_middles_incorrect += find_middle_page(sorted_u)

    print("Part 1: Sum of middle pages of correct updates:", sum_of_middles_correct)
    print("Part 2: Sum of middle pages of corrected (originally incorrect) updates:", sum_of_middles_incorrect)

if __name__ == "__main__":
    main()
