# ES Performance Report

- Generated: 2026-04-02T13:49:21Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-04T13:48:38Z .. 2026-04-02T13:48:38Z
- Range: 6m
- Root size: 100
- Sub multiplier: 2.0
- Sub size: 200
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.10
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account eb677892-ecea-4d6a-89f0-a0b0bc9d4e32: 

| Metric | Value |
| --- | --- |
| Runs | 989 |
| Root avg wall (ms) | 456.84 |
| Root min/max wall (ms) | 257.81 / 3858.48 |
| Root p50 wall (ms) | 280.50 |
| Root p90 wall (ms) | 379.78 |
| Root p99 wall (ms) | 3167.88 |
| Root avg TTFB (ms) | 360.66 |
| Root p50 TTFB (ms) | 186.89 |
| Root p90 TTFB (ms) | 298.56 |
| Root p99 TTFB (ms) | 3088.90 |
| Root avg read (ms) | 96.18 |
| Root p50 read (ms) | 96.59 |
| Root p90 read (ms) | 117.67 |
| Root p99 read (ms) | 141.84 |
| Root avg decode (ms) | 0.56 |
| Root p50 decode (ms) | 0.47 |
| Root p90 decode (ms) | 0.86 |
| Root p99 decode (ms) | 2.21 |
| Sub avg wall (ms) | 571.81 |
| Sub min/max wall (ms) | 203.46 / 5360.57 |
| Sub p50 wall (ms) | 388.83 |
| Sub p90 wall (ms) | 666.54 |
| Sub p99 wall (ms) | 3337.02 |
| Sub avg TTFB (ms) | 371.17 |
| Sub p50 TTFB (ms) | 185.31 |
| Sub p90 TTFB (ms) | 447.62 |
| Sub p99 TTFB (ms) | 3138.75 |
| Sub avg read (ms) | 200.63 |
| Sub p50 read (ms) | 199.32 |
| Sub p90 read (ms) | 233.07 |
| Sub p99 read (ms) | 258.88 |
| Sub avg decode (ms) | 1.42 |
| Sub p50 decode (ms) | 1.20 |
| Sub p90 decode (ms) | 1.72 |
| Sub p99 decode (ms) | 6.54 |
| Total avg wall (ms) | 1030.71 |
| Total min/max (ms) | 600.93 / 8499.45 |
| Total p50 wall (ms) | 686.49 |
| Total p90 wall (ms) | 2467.69 |
| Total p99 wall (ms) | 3649.80 |
| Root avg ES took (ms) | 22.94 |
| Sub avg ES took (ms) | 21.08 |
| Root hits (unique) | 675, 679, 779, 835, 843, 848, 850, 881, 885, 892, 895, 919, 920, 921, 930, 936, 942, 943, 957, 963, 973, 974, 985, 989, 1006, 1017, 1026, 1028, 1029, 1031, 1053, 1057, 1091, 1098, 1146, 1148, 1149, 1163, 1176, 1179, 1180, 1184, 1189, 1199, 1200, 1216, 1236, 1243, 1264, 1283, 1298, 1305, 1324, 1347, 1357, 1364, 1372, 1380, 1385, 1399, 1402, 1440, 1449, 1459, 1463, 1470, 1484, 1499, 1523, 1537, 1547, 1551, 1588, 1606, 1631, 1650, 1658, 1659, 1691, 1692, 1710, 1828, 1836, 1847, 1956, 1958, 2029, 2036, 2061, 2099, 2198, 2212, 2243, 2306, 2379, 2396, 2428, 2773 |
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
              "gte": "2025-10-04T13:48:38Z",
              "lte": "2026-04-02T13:48:38Z"
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
              "gte": "2025-10-04T13:48:38Z",
              "lte": "2026-04-02T13:48:38Z"
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
