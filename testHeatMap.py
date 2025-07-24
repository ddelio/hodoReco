#!/usr/bin/env python3
"""
gen_gauss_coords.py – sample N points from a rotated 2D Gaussian and
write integer (x y) pairs in [0,63] to coords.txt, discarding
any points that fall outside the grid.
"""

import argparse
import math
import numpy as np
from tqdm import tqdm

def main():
    p = argparse.ArgumentParser(
        description="Sample N points from a rotated 2D Gaussian into a 64×64 grid"
    )
    p.add_argument("-N", "--num",     type=int,   default=10_000_000,
                   help="number of samples to draw")
    p.add_argument("--mu-x",          type=float, default=32.0,
                   help="Gaussian center X (grid units)")
    p.add_argument("--mu-y",          type=float, default=32.0,
                   help="Gaussian center Y (grid units)")
    p.add_argument("--sigma-x",       type=float, default=11.0,
                   help="Gaussian σ in X")
    p.add_argument("--sigma-y",       type=float, default=8.0,
                   help="Gaussian σ in Y")
    p.add_argument("--theta",         type=float, default=32.0,
                   help="Rotation angle (degrees) CCW about (mu-x,mu-y)")
    p.add_argument("-o", "--output",  type=str,   default="coords.txt",
                   help="output filename")
    args = p.parse_args()

    # precompute rotation
    theta_rad = math.radians(args.theta)
    cos_t, sin_t = math.cos(theta_rad), math.sin(theta_rad)

    # sample unrotated
    xs = np.random.normal(loc=args.mu_x, scale=args.sigma_x, size=args.num)
    ys = np.random.normal(loc=args.mu_y, scale=args.sigma_y, size=args.num)

    coords = []
    for x, y in tqdm(zip(xs, ys), total=args.num, desc="Sampling & filtering"):
        # translate to origin, rotate, translate back
        dx, dy = x - args.mu_x, y - args.mu_y
        xr =  dx * cos_t - dy * sin_t + args.mu_x
        yr =  dx * sin_t + dy * cos_t + args.mu_y

        xi, yi = int(round(xr)), int(round(yr))
        if 0 <= xi < 64 and 0 <= yi < 64:
            coords.append((xi, yi))

    with open(args.output, "w") as f:
        for xi, yi in tqdm(coords, desc="Writing coords"):
            f.write(f"{xi} {yi}\n")

    print(
        f"Wrote {len(coords):,} rotated Gaussian coords to '{args.output}' "
        f"(from {args.num:,} samples, θ={args.theta}°)"
    )

if __name__ == "__main__":
    main()
