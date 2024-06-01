from __future__ import annotations

from .lib import Dahlia, Depth

TEST_STRING = "&R".join(f"&{c * 2}" for c in "0123456789abcdefhijklmno")

if __name__ == "__main__":
    if (max_depth := Dahlia().depth) is None:
        print("Disabled colors")
    else:
        print(f"Max depth: {max_depth.name} ({max_depth.value}-bit)")
        for depth in Depth.__members__.values():
            Dahlia(depth=depth).print(TEST_STRING)
            if depth is max_depth:
                break
