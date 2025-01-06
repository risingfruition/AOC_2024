DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3
NUM_DIRECTIONS = 4
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
opposite_directions = [directions[UP], directions[DOWN], directions[LEFT], directions[RIGHT]]
opposite_compass = [UP, DOWN, LEFT, RIGHT]


def all_neighbors(r, c):
    for dr, dc in directions:
        yield r + dr, c + dc


CORNERS = {
    # CCW, DIAG, CW
    (False, False, False),  # Plot is on the inside of a corner.
    (False, True, False),  # Plot is on the inside of a corner.
    (True, False, True)  # Plot is on the outside of a corner.
}

corner_directions = [
    # Dir, then diag clockwise, then again clockwise.
    ((-1, 0), (-1, 1), (0, 1)),  # Up, Up Right, Right
    ((0, 1), (1, 1), (1, 0)),  # Right, Down Right, Down
    ((1, 0), (1, -1), (0, -1)),  # Down, Down Left, Left
    ((0, -1), (-1, -1), (-1, 0))  # Left, Up Left, Up
]


def corner_neighbors(r, c, offsets):
    # Offsets must be in Dir, Diag CW, CW order
    aa, bb, cc = offsets
    return (r + aa[0], c + aa[1]), (r + bb[0], c + bb[1]), (r + cc[0], c + cc[1])


def in_plots(plots, neighbors):
    # neighbors must be in Dir, Diag CW, CW order
    return neighbors[0] in plots, neighbors[1] in plots, neighbors[2] in plots


def corners(plots):
    count = 0
    for r, c in plots.keys():
        for dir_offsets in corner_directions:
            neighbors = corner_neighbors(r, c, dir_offsets)
            goober = in_plots(plots, neighbors)

            if goober in CORNERS:
                count += 1
    return count


class Region:
    def __init__(self, data, r, c):
        self.plant = data[r][c]
        self.plots = {}
        self.lines = {}
        self.corners = {}
        # self.add(r, c)
        self.slurp(data, r, c)
        print(f"{self.plots=}")

    def __repr__(self):
        return f"Plant {self.plant}, {self.plots.keys()}"

    def has(self, r, c):
        return (r, c) in self.plots

    def slurp(self, data, r, c):
        # print(f"slurp {r},{c} begin:")
        check = []
        checked = []
        check.append((r, c))

        while check:
            r, c = check.pop(0)
            if (r, c) in self.plots:
                continue
            checked.append((r, c))
            self.add(r, c)
            # print(f"ADD {r},{c}")
            for rr, cc in all_neighbors(r, c):
                if rr < 0 or cc < 0 or rr >= len(data) or cc >= len(data[0]):
                    continue
                if data[rr][cc] == self.plant:
                    if not (rr, cc) in self.plots:
                        check.append((rr, cc))
                        # self.add(rr, cc)
                        # print(f"slurping {rr},{cc}")

    def is_touching(self, r, c):
        """Return True if r,c is touching any square in self.plots."""
        print(f"{r=} {c=}")
        for dr, dc in directions:
            rr = r + dr
            cc = c + dc
            print(f"{rr=}, {cc=}")
            if (rr, cc) in self.plots:
                print(f"-------> {rr=}, {cc=}")
                return True
        return False

    def add(self, r, c):
        self.plots[(r, c)] = self.plant

    def area(self):
        return len(self.plots.keys())

    def make_line(self, dir, r, c):
        rr = r * 2 + 1
        cc = c * 2 + 1
        down_right = (rr+1, cc+1)
        down_left = (rr+1, cc-1)
        up_left = (rr-1, cc-1)
        up_right = (rr-1, cc+1)
        rc = (rr, cc)
        if dir == DOWN:
            lyst = self.lines.get(rc, [])
            self.lines[rc] = lyst
            lyst.append((UP, down_right, down_left))

            lyst = self.corners.get(down_right, [])
            lyst.append((rr, cc))
            self.corners[down_right] = lyst

            lyst = self.corners.get(down_left, [])
            lyst.append((rr, cc))
            self.corners[down_left] = lyst
        if dir == UP:
            lyst = self.lines.get(rc, [])
            self.lines[rc] = lyst
            lyst.append((DOWN, up_left, up_right))

            lyst = self.corners.get(down_right, [])
            lyst.append((rr, cc))
            self.corners[down_right] = lyst

            lyst = self.corners.get(down_left, [])
            lyst.append((rr, cc))
            self.corners[down_left] = lyst
        if dir == LEFT:
            lyst = self.lines.get(rc, [])
            self.lines[rc] = lyst
            lyst.append((RIGHT, down_left, up_left))

            lyst = self.corners.get(down_left, [])
            lyst.append((rr, cc))
            self.corners[down_left] = lyst

            lyst = self.corners.get(up_left, [])
            lyst.append((rr, cc))
            self.corners[up_left] = lyst
        if dir == RIGHT:
            lyst = self.lines.get(rc, [])
            self.lines[rc] = lyst
            lyst.append((LEFT, up_right, down_right))

            lyst = self.corners.get(up_right, [])
            lyst.append((rr, cc))
            self.corners[up_right] = lyst

            lyst = self.corners.get(down_right, [])
            lyst.append((rr, cc))
            self.corners[down_right] = lyst

    def count_borders_self(self, r, c):
        count = 0
        for dir in range(NUM_DIRECTIONS):
            dr, dc = directions[dir]
            if (r + dr, c + dc) in self.plots:
                count += 1
            # else:
            #     self.make_line(dir, r, c)
        # for rr, cc in all_neighbors(r, c):
        #     if (rr, cc) in self.plots:
        #         count += 1
        return count

    def perimeter(self):
        border = 4 * self.area()
        for r, c in self.plots.keys():
            border -= self.count_borders_self(r, c)
        print(f"Plant: {self.plant}  Area={self.area()}  Perimeter={border}")
        print(f"plots {self.plots}")
        print(f"lines {self.lines}")
        print(f"corners {self.corners}")
        # self.perimeter = border
        return border

    def sides(self):
        return corners(self.plots)


class Regions:
    def __init__(self):
        self.regs = []

    def has_reg_with(self, r, c):
        for reg in self.regs:
            if reg.has(r, c):
                return True
        return False

    def add_plot(self, data, r, c):
        if self.has_reg_with(r, c):
            return
        reg = Region(data, r, c)
        self.regs.append(reg)

    def fence_cost(self):
        total = 0
        for reg in self.regs:
            total += reg.area() * reg.perimeter()
        return total


