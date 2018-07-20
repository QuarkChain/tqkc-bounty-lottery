# tQKC Bounty Lottery

For details and the scoring rubric, check the [official announcement](https://steemit.com/quarkchain/@quarkchain/load-test-schedule-testnet-token-distribution-and-lottery-plan).

Scores with corresponding addresses are public in this repo. For example, `score-07-19.csv` contains the scores for addresses which are counted before 07/19.

We will use the date as the random seed. To run the lottery:

```
python3 lottery.py '2018-07-19' --score_file score-07-19.csv --output_file lottery-07-19.csv
```

Results are written into `lottery-07-19.csv`.

Note that during the sampling, we use the square of a candidate's score as the source for sampling probability, thus higher scores are further more likely to be picked.
