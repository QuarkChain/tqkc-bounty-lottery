#!/usr/bin/env python3
import argparse
import random

from os import path


LOTTERY_NUM = 10
# 1st place gets 7000 QKC, 2nd / 3rd get 3000 QKC, others 1000 QKC.
LOTTERY_QKC = [7000] + [3000] * 2 + [1000] * 7


def get_address_and_score(score_file) -> [(str, float)]:
    dir_path = path.dirname(path.realpath(__file__))

    with open(path.join(dir_path, score_file)) as f:
        lines = f.readlines()
    ret = []
    # Skip header row.
    for line in lines[1:]:
        k, s = line.strip().split(",")
        ret.append((k, float(s)))
    return ret


class Candidate(object):
    def __init__(self, addr: str, score: float):
        self.addr = addr
        self.score = score
        # More in favor of higher scores.
        self.prob = score * score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "seed", type=str, help="Use the current date as the seed, like 2018-07-19"
    )
    parser.add_argument("--score_file", required=True, type=str)
    parser.add_argument("--output_file", required=True, type=str)

    args = parser.parse_args()
    random.seed(args.seed)

    candidates = [
        Candidate(addr, score) for addr, score in get_address_and_score(args.score_file)
    ]
    lottery = []

    assert len(candidates) > LOTTERY_NUM
    # Make sure the order is deterministic so it's reproducible.
    candidates.sort(key=lambda c: c.addr)
    for _ in range(LOTTERY_NUM):
        # Sampling. The higher the score, the greater the chance to get picked.
        total_prob = sum(c.prob for c in candidates)
        chosen = random.random() * total_prob
        for i, c in enumerate(candidates):
            if chosen <= c.prob:
                lottery.append(c)
                candidates.pop(i)
                break
            chosen -= c.prob

    assert len(lottery) == LOTTERY_NUM

    # Write the lottery result.
    dir_path = path.dirname(path.realpath(__file__))
    with open(path.join(dir_path, args.output_file), "w") as f:
        f.write("address,score,qkc\n")
        for c, qkc in zip(lottery, LOTTERY_QKC):
            f.write("%s,%d,%d\n" % (c.addr, c.score, qkc))


if __name__ == "__main__":
    main()
