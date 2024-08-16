import time
from collections import deque


class BrickMachine:
    def __init__(self, inpout_data: str) -> None:
        self.input = inpout_data
        self.bricks_falling = self._parse_input()
        self.fallen_bricks = self._make_bricks_fall(self.bricks_falling)
        self.supps = None
        self.is_supped = None

    def _parse_input(self) -> list[tuple[int, int, int, int, int, int]]:
        # view from top, aka z is vertical, y and x are horizontal
        # ground is at z = 0
        coordinates = [line.split("~") for line in self.input.strip().split("\n")]
        bricks = []
        for s, e in coordinates:
            x1, y1, z1 = [int(n) for n in s.split(",")]
            x2, y2, z2 = [int(n) for n in e.split(",")]
            assert z1 > 0 and z2 > 0, "Has to be above ground"
            assert z1 <= z2 and x1 <= x2 and y1 <= y2, "z1 has to be smaller than z2"
            bricks.append((x1, y1, z1, x2, y2, z2))
        return bricks

    def _make_bricks_fall(self, bricks) -> list[tuple[int, int, int, int, int, int]]:
        sorted_bricks = sorted(bricks, key=lambda x: x[2])
        d = deque(sorted_bricks)
        fallen_bricks = []
        while d:
            x1, y1, z1, x2, y2, z2 = d.popleft()
            if z1 == 1:
                fallen_bricks.append((x1, y1, z1, x2, y2, z2))
                continue
            min_z = 1
            for fx1, fy1, _, fx2, fy2, fz2 in fallen_bricks:
                overlaps = max(x1, fx1) <= min(x2, fx2) and max(y1, fy1) <= min(y2, fy2)
                if overlaps:
                    min_z = max(min_z, fz2 + 1)
            fallen_bricks.append((x1, y1, min_z, x2, y2, min_z + z2 - z1))
        fallen_bricks.sort(key=lambda x: x[2])
        return fallen_bricks

    def part_1(self) -> int:
        fallen_bricks = self.fallen_bricks
        assert fallen_bricks == self._make_bricks_fall(
            fallen_bricks
        ), "error in falling algorithm"
        brick_supports = {fb: set() for fb in fallen_bricks}
        supports_of_brick = {fb: set() for fb in fallen_bricks}
        for i, brick in enumerate(fallen_bricks):
            for support in fallen_bricks[:i]:
                assert brick[2] >= support[2], "support higher than brick"
                assert (
                    brick[2] > support[5]
                    or max(brick[0], support[0]) > min(brick[3], support[3])
                    or max(brick[1], support[1]) > min(brick[4], support[4])
                ), "collision of blocks"

                does_support = (
                    (support[5] == brick[2] - 1)
                    and max(brick[0], support[0]) <= min(brick[3], support[3])
                    and max(brick[1], support[1]) <= min(brick[4], support[4])
                )
                if does_support:
                    brick_supports[support].add(brick)
                    supports_of_brick[brick].add(support)
        self.supps = brick_supports
        self.is_supped = supports_of_brick
        can_remove = 0
        for brick in fallen_bricks:
            if all(len(supports_of_brick[sb]) > 1 for sb in brick_supports[brick]):
                can_remove += 1
        return can_remove

    def part_2(self) -> int:
        fallen_sum = 0
        for br in self.fallen_bricks:
            f = deque(b for b in self.supps[br] if len(self.is_supped[b]) == 1)
            falling = set(f)
            falling.add(br)

            while f:
                brick = f.popleft()
                for i in self.supps[brick] - falling:
                    if self.is_supped[i] <= falling:
                        f.append(i)
                        falling.add(i)
            fallen_sum += len(falling) - 1
        return fallen_sum


def main() -> None:
    with open("2023/Day_22_example.txt", "r") as file:
        input_example = file.read()

    with open("2023/Day_22.txt", "r") as file:
        input_real = file.read()

    bmex = BrickMachine(input_example)
    bm = BrickMachine(input_real)

    # Part 1
    print(f"Result 1 is: {bmex.part_1(), bm.part_1()}")

    # Part 2
    print(f"Result 2 is: {bmex.part_2(), bm.part_2()}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
