# ES Performance Report

- Generated: 2026-04-02T13:46:05Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-04T13:45:26Z .. 2026-04-02T13:45:26Z
- Range: 6m
- Root size: 25
- Sub multiplier: 2.0
- Sub size: 50
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 25.44
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 466132f4-682a-4345-89f2-0c9f731dcb02: 

| Metric | Value |
| --- | --- |
| Runs | 986 |
| Root avg wall (ms) | 276.40 |
| Root min/max wall (ms) | 172.37 / 2532.22 |
| Root p50 wall (ms) | 187.77 |
| Root p90 wall (ms) | 487.40 |
| Root p99 wall (ms) | 963.76 |
| Root avg TTFB (ms) | 267.08 |
| Root p50 TTFB (ms) | 182.15 |
| Root p90 TTFB (ms) | 479.57 |
| Root p99 TTFB (ms) | 963.24 |
| Root avg read (ms) | 9.32 |
| Root p50 read (ms) | 1.96 |
| Root p90 read (ms) | 22.50 |
| Root p99 read (ms) | 32.73 |
| Root avg decode (ms) | 0.18 |
| Root p50 decode (ms) | 0.15 |
| Root p90 decode (ms) | 0.20 |
| Root p99 decode (ms) | 0.90 |
| Sub avg wall (ms) | 269.07 |
| Sub min/max wall (ms) | 85.20 / 1853.39 |
| Sub p50 wall (ms) | 220.16 |
| Sub p90 wall (ms) | 450.58 |
| Sub p99 wall (ms) | 610.39 |
| Sub avg TTFB (ms) | 223.45 |
| Sub p50 TTFB (ms) | 176.44 |
| Sub p90 TTFB (ms) | 417.16 |
| Sub p99 TTFB (ms) | 578.19 |
| Sub avg read (ms) | 45.61 |
| Sub p50 read (ms) | 41.25 |
| Sub p90 read (ms) | 55.36 |
| Sub p99 read (ms) | 73.66 |
| Sub avg decode (ms) | 0.41 |
| Sub p50 decode (ms) | 0.32 |
| Sub p90 decode (ms) | 0.44 |
| Sub p99 decode (ms) | 2.19 |
| Total avg wall (ms) | 546.08 |
| Total min/max (ms) | 359.89 / 2749.81 |
| Total p50 wall (ms) | 436.92 |
| Total p90 wall (ms) | 826.09 |
| Total p99 wall (ms) | 1537.49 |
| Root avg ES took (ms) | 85.35 |
| Sub avg ES took (ms) | 38.96 |
| Root hits (unique) | 675, 679, 779, 835, 843, 848, 850, 881, 885, 892, 895, 919, 920, 921, 930, 936, 942, 943, 957, 963, 973, 974, 985, 989, 1006, 1017, 1026, 1028, 1029, 1031, 1053, 1057, 1091, 1098, 1146, 1148, 1149, 1163, 1176, 1179, 1180, 1184, 1189, 1199, 1200, 1216, 1236, 1243, 1264, 1283, 1298, 1305, 1324, 1347, 1357, 1364, 1372, 1380, 1385, 1399, 1402, 1440, 1449, 1459, 1463, 1470, 1484, 1499, 1523, 1537, 1547, 1551, 1588, 1606, 1631, 1650, 1658, 1659, 1691, 1692, 1710, 1828, 1836, 1847, 1956, 1958, 2029, 2036, 2061, 2099, 2198, 2212, 2243, 2306, 2379, 2396, 2428, 2773 |
| Root brand IDs (unique) | 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 |
| Sub hits (unique) | 26, 33, 34, 40, 42, 44, 45, 46, 47, 49, 50, 51, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 65, 67, 68, 70, 71, 72, 74, 76, 80, 82, 84, 85, 87, 90, 91, 93, 94, 95, 96, 97, 100, 102, 106, 107, 108, 111, 112, 113, 114, 115, 116, 118, 119, 123, 126, 130, 132, 143, 147, 163, 168, 175, 213 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

### Root Query

```json
{
  "size": 25,
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
              "gte": "2025-10-04T13:45:26Z",
              "lte": "2026-04-02T13:45:26Z"
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
  "size": 50,
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
              "gte": "2025-10-04T13:45:26Z",
              "lte": "2026-04-02T13:45:26Z"
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
