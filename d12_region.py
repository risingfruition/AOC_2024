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


class Region:
    def __init__(self, data, r, c):
        self.plant = data[r][c]
        self.plots = {}
        self.lines = {}
        self.corners = {}
        # self.add(r, c)
        self.slurp(data, r, c)

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
                        check.append((rr,cc))
                        # self.add(rr, cc)
                        # print(f"slurping {rr},{cc}")

    def is_touching(self, r, c):
        for dr, dc in directions:
            rr = r + dr
            cc = c + dc
            # print(rr, cc)
            if (rr, cc) in self.plots:
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


