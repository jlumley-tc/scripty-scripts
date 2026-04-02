# ES Performance Report

- Generated: 2026-04-02T13:51:00Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-04T13:50:11Z .. 2026-04-02T13:50:11Z
- Range: 6m
- Root size: 200
- Sub multiplier: 2.0
- Sub size: 400
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 20.11
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 3c039bbe-f9d9-405d-b9a6-48ed3dedd5a0: 

| Metric | Value |
| --- | --- |
| Runs | 992 |
| Root avg wall (ms) | 1794.74 |
| Root min/max wall (ms) | 361.58 / 6430.50 |
| Root p50 wall (ms) | 710.70 |
| Root p90 wall (ms) | 5058.37 |
| Root p99 wall (ms) | 5952.41 |
| Root avg TTFB (ms) | 1430.64 |
| Root p50 TTFB (ms) | 454.94 |
| Root p90 TTFB (ms) | 4368.21 |
| Root p99 TTFB (ms) | 5468.80 |
| Root avg read (ms) | 364.10 |
| Root p50 read (ms) | 241.66 |
| Root p90 read (ms) | 777.62 |
| Root p99 read (ms) | 1156.55 |
| Root avg decode (ms) | 1.02 |
| Root p50 decode (ms) | 0.87 |
| Root p90 decode (ms) | 1.31 |
| Root p99 decode (ms) | 2.33 |
| Sub avg wall (ms) | 2218.06 |
| Sub min/max wall (ms) | 530.22 / 6338.45 |
| Sub p50 wall (ms) | 1112.62 |
| Sub p90 wall (ms) | 5089.38 |
| Sub p99 wall (ms) | 5943.84 |
| Sub avg TTFB (ms) | 1619.49 |
| Sub p50 TTFB (ms) | 593.51 |
| Sub p90 TTFB (ms) | 4411.19 |
| Sub p99 TTFB (ms) | 5282.83 |
| Sub avg read (ms) | 598.57 |
| Sub p50 read (ms) | 457.76 |
| Sub p90 read (ms) | 1093.71 |
| Sub p99 read (ms) | 1672.90 |
| Sub avg decode (ms) | 2.25 |
| Sub p50 decode (ms) | 2.04 |
| Sub p90 decode (ms) | 2.62 |
| Sub p99 decode (ms) | 8.41 |
| Total avg wall (ms) | 4016.22 |
| Total min/max (ms) | 908.99 / 10016.19 |
| Total p50 wall (ms) | 1813.80 |
| Total p90 wall (ms) | 8999.44 |
| Total p99 wall (ms) | 9436.51 |
| Root avg ES took (ms) | 33.36 |
| Sub avg ES took (ms) | 28.43 |
| Root hits (unique) | 675, 679, 779, 835, 843, 848, 850, 881, 885, 892, 895, 919, 920, 921, 930, 936, 942, 943, 957, 963, 973, 974, 985, 989, 1006, 1017, 1026, 1028, 1029, 1031, 1053, 1057, 1091, 1098, 1146, 1148, 1149, 1163, 1176, 1179, 1180, 1184, 1189, 1199, 1200, 1216, 1236, 1243, 1264, 1283, 1298, 1305, 1324, 1347, 1357, 1364, 1372, 1380, 1385, 1399, 1402, 1440, 1449, 1459, 1463, 1470, 1484, 1499, 1523, 1537, 1547, 1551, 1588, 1606, 1631, 1650, 1658, 1659, 1691, 1692, 1710, 1828, 1836, 1847, 1956, 1958, 2029, 2036, 2061, 2099, 2198, 2212, 2243, 2306, 2379, 2396, 2428, 2773 |
| Root brand IDs (unique) | 162, 172, 174, 177, 178, 181, 182, 184, 185, 186, 187, 188, 189, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200 |
| Sub hits (unique) | 394, 406, 482, 491, 505, 520, 544, 545, 552, 560, 572, 600, 613, 625, 638, 645, 648, 661, 662, 664, 673, 674, 680, 686, 693, 701, 714, 717, 720, 721, 722, 728, 730, 738, 741, 744, 754, 762, 763, 768, 769, 780, 782, 788, 800, 801, 802, 821, 832, 834, 835, 838, 844, 845, 847, 851, 861, 880, 899, 901, 909, 910, 913, 914, 916, 920, 923, 933, 934, 935, 937, 939, 943, 950, 957, 968, 971, 988, 993, 994, 1005, 1008, 1013, 1027, 1169, 1176, 1180, 1185, 1237, 1334, 1393, 1400, 1552, 1563, 1664, 1700 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

### Root Query

```json
{
  "size": 200,
  "_source": true,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "mse_account_uuid": "<REDACTED_ACCOUNT>"
          }
        },
        {
          "terms": {
            "status": [
              "completed",
              "draft"
            ]
          }
        },
        {
          "range": {
            "transaction_date": {
              "gte": "2025-10-04T13:50:11Z",
              "lte": "2026-04-02T13:50:11Z"
            }
          }
        }
      ],
      "must_not": [
        {
          "exists": {
            "field": "related_product_transaction_uuid"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "transaction_date": {
        "order": "desc"
      }
    },
    {
      "brand_transaction_id": {
        "order": "asc"
      }
    }
  ]
}
```

### Sub Query

```json
{
  "size": 400,
  "_source": true,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "mse_account_uuid": "<REDACTED_ACCOUNT>"
          }
        },
        {
          "terms": {
            "status": [
              "completed",
              "draft"
            ]
          }
        },
        {
          "range": {
            "transaction_date": {
              "gte": "2025-10-04T13:50:11Z",
              "lte": "2026-04-02T13:50:11Z"
            }
          }
        },
        {
          "terms": {
            "related_product_transaction_uuid": [
              "<REDACTED_TXN_1>",
              "<REDACTED_TXN_2>",
              "<REDACTED_TXN_3>",
              "<REDACTED_TXN_4>",
              "<REDACTED_TXN_5>",
              "<REDACTED_TXN_6>",
              "<REDACTED_TXN_7>",
              "<REDACTED_TXN_8>",
              "<REDACTED_TXN_9>",
              "<REDACTED_TXN_10>",
              "<REDACTED_TXN_MORE>"
            ]
          }
        }
      ]
    }
  },
  "sort": [
    {
      "transaction_date": {
        "order": "asc"
      }
    },
    {
      "related_product_transaction_uuid": {
        "order": "asc"
      }
    }
  ]
}
```
