# ES Performance Report

- Generated: 2026-04-02T13:47:43Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-04T13:47:00Z .. 2026-04-02T13:47:00Z
- Range: 6m
- Root size: 50
- Sub multiplier: 2.0
- Sub size: 100
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.51
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 91fb6007-ed43-443e-b913-1de31d1c9ca4: 

| Metric | Value |
| --- | --- |
| Runs | 996 |
| Root avg wall (ms) | 337.59 |
| Root min/max wall (ms) | 221.87 / 976.83 |
| Root p50 wall (ms) | 308.78 |
| Root p90 wall (ms) | 401.13 |
| Root p99 wall (ms) | 676.02 |
| Root avg TTFB (ms) | 218.88 |
| Root p50 TTFB (ms) | 189.03 |
| Root p90 TTFB (ms) | 277.36 |
| Root p99 TTFB (ms) | 519.63 |
| Root avg read (ms) | 118.72 |
| Root p50 read (ms) | 118.17 |
| Root p90 read (ms) | 133.03 |
| Root p99 read (ms) | 163.52 |
| Root avg decode (ms) | 0.29 |
| Root p50 decode (ms) | 0.26 |
| Root p90 decode (ms) | 0.35 |
| Root p99 decode (ms) | 1.07 |
| Sub avg wall (ms) | 491.04 |
| Sub min/max wall (ms) | 289.54 / 979.78 |
| Sub p50 wall (ms) | 463.22 |
| Sub p90 wall (ms) | 568.80 |
| Sub p99 wall (ms) | 795.43 |
| Sub avg TTFB (ms) | 217.74 |
| Sub p50 TTFB (ms) | 184.38 |
| Sub p90 TTFB (ms) | 280.09 |
| Sub p99 TTFB (ms) | 533.67 |
| Sub avg read (ms) | 273.30 |
| Sub p50 read (ms) | 274.89 |
| Sub p90 read (ms) | 306.99 |
| Sub p99 read (ms) | 346.85 |
| Sub avg decode (ms) | 0.71 |
| Sub p50 decode (ms) | 0.59 |
| Sub p90 decode (ms) | 1.17 |
| Sub p99 decode (ms) | 1.88 |
| Total avg wall (ms) | 829.68 |
| Total min/max (ms) | 529.47 / 1504.66 |
| Total p50 wall (ms) | 790.73 |
| Total p90 wall (ms) | 1010.13 |
| Total p99 wall (ms) | 1216.30 |
| Root avg ES took (ms) | 23.33 |
| Sub avg ES took (ms) | 20.73 |
| Root hits (unique) | 675, 679, 779, 835, 843, 848, 850, 881, 885, 892, 895, 919, 920, 921, 930, 936, 942, 943, 957, 963, 973, 974, 985, 989, 1006, 1017, 1026, 1028, 1029, 1031, 1053, 1057, 1091, 1098, 1146, 1148, 1149, 1163, 1176, 1179, 1180, 1184, 1189, 1199, 1200, 1216, 1236, 1243, 1264, 1283, 1298, 1305, 1324, 1347, 1357, 1364, 1372, 1380, 1385, 1399, 1402, 1440, 1449, 1459, 1463, 1470, 1484, 1499, 1523, 1537, 1547, 1551, 1588, 1606, 1631, 1650, 1658, 1659, 1691, 1692, 1710, 1828, 1836, 1847, 1956, 1958, 2029, 2036, 2061, 2099, 2198, 2212, 2243, 2306, 2379, 2396, 2428, 2773 |
| Root brand IDs (unique) | 24, 28, 31, 32, 34, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 |
| Sub hits (unique) | 69, 89, 94, 97, 100, 104, 108, 112, 114, 115, 121, 122, 123, 124, 125, 127, 128, 129, 130, 131, 133, 134, 135, 136, 140, 141, 144, 148, 149, 152, 156, 158, 162, 166, 167, 170, 171, 172, 178, 180, 181, 182, 183, 186, 187, 188, 192, 198, 200, 201, 203, 205, 211, 214, 217, 219, 224, 225, 226, 228, 230, 233, 234, 235, 236, 240, 243, 245, 250, 252, 276, 280, 299, 313, 318, 332, 343, 350, 364, 426 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

### Root Query

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
              "gte": "2025-10-04T13:47:00Z",
              "lte": "2026-04-02T13:47:00Z"
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
              "gte": "2025-10-04T13:47:00Z",
              "lte": "2026-04-02T13:47:00Z"
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
