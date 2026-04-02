# ES Performance Report

- Generated: 2026-04-02T14:24:05Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-07T14:23:22Z .. 2026-04-02T14:23:22Z
- Range: 12m
- Root size: 100
- Sub multiplier: 2.0
- Sub size: 200
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.38
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account d4158e22-4b3b-44d4-958b-ef50e010dd2e: 

| Metric | Value |
| --- | --- |
| Runs | 989 |
| Root avg wall (ms) | 298.88 |
| Root min/max wall (ms) | 256.94 / 714.53 |
| Root p50 wall (ms) | 276.10 |
| Root p90 wall (ms) | 342.23 |
| Root p99 wall (ms) | 548.68 |
| Root avg TTFB (ms) | 202.24 |
| Root p50 TTFB (ms) | 184.72 |
| Root p90 TTFB (ms) | 243.89 |
| Root p99 TTFB (ms) | 474.42 |
| Root avg read (ms) | 96.64 |
| Root p50 read (ms) | 97.63 |
| Root p90 read (ms) | 117.66 |
| Root p99 read (ms) | 141.94 |
| Root avg decode (ms) | 0.56 |
| Root p50 decode (ms) | 0.48 |
| Root p90 decode (ms) | 0.88 |
| Root p99 decode (ms) | 1.61 |
| Sub avg wall (ms) | 409.85 |
| Sub min/max wall (ms) | 322.96 / 1003.80 |
| Sub p50 wall (ms) | 389.46 |
| Sub p90 wall (ms) | 457.22 |
| Sub p99 wall (ms) | 685.90 |
| Sub avg TTFB (ms) | 206.67 |
| Sub p50 TTFB (ms) | 184.37 |
| Sub p90 TTFB (ms) | 254.09 |
| Sub p99 TTFB (ms) | 488.44 |
| Sub avg read (ms) | 203.18 |
| Sub p50 read (ms) | 200.14 |
| Sub p90 read (ms) | 233.73 |
| Sub p99 read (ms) | 251.88 |
| Sub avg decode (ms) | 1.35 |
| Sub p50 decode (ms) | 1.20 |
| Sub p90 decode (ms) | 1.83 |
| Sub p99 decode (ms) | 2.98 |
| Total avg wall (ms) | 710.72 |
| Total min/max (ms) | 601.29 / 1276.42 |
| Total p50 wall (ms) | 679.91 |
| Total p90 wall (ms) | 873.06 |
| Total p99 wall (ms) | 1051.73 |
| Root avg ES took (ms) | 19.10 |
| Sub avg ES took (ms) | 16.17 |
| Root hits (unique) | 684, 817, 838, 853, 879, 886, 895, 914, 936, 937, 950, 954, 955, 958, 972, 974, 994, 999, 1018, 1019, 1030, 1032, 1039, 1040, 1058, 1062, 1078, 1082, 1084, 1089, 1109, 1123, 1164, 1185, 1194, 1200, 1202, 1214, 1217, 1219, 1220, 1227, 1228, 1271, 1282, 1286, 1302, 1331, 1334, 1338, 1346, 1356, 1364, 1366, 1381, 1421, 1426, 1427, 1433, 1442, 1444, 1461, 1485, 1497, 1512, 1515, 1520, 1530, 1560, 1572, 1585, 1606, 1613, 1623, 1653, 1673, 1688, 1691, 1742, 1762, 1765, 1870, 1885, 1888, 1985, 2046, 2070, 2113, 2122, 2229, 2273, 2355, 2391, 2394, 2432, 2457, 2812 |
| Root brand IDs (unique) | 62, 72, 75, 77, 79, 81, 82, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100 |
| Sub hits (unique) | 179, 199, 221, 225, 231, 236, 247, 257, 260, 261, 266, 268, 280, 281, 286, 293, 295, 296, 297, 299, 300, 308, 313, 315, 317, 320, 321, 328, 329, 330, 339, 340, 341, 342, 344, 348, 360, 361, 362, 364, 365, 368, 369, 371, 379, 380, 382, 383, 384, 386, 392, 394, 402, 405, 409, 410, 412, 414, 415, 424, 425, 430, 431, 433, 451, 453, 454, 456, 460, 462, 463, 466, 467, 471, 472, 476, 480, 485, 486, 488, 491, 493, 495, 501, 523, 577, 580, 612, 664, 693, 700, 727, 732, 798, 850 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

### Root Query

```json
{
  "size": 100,
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
              "gte": "2025-04-07T14:23:22Z",
              "lte": "2026-04-02T14:23:22Z"
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
              "gte": "2025-04-07T14:23:22Z",
              "lte": "2026-04-02T14:23:22Z"
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
