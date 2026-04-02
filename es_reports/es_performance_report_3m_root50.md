# ES Performance Report

- Generated: 2026-04-02T13:47:00Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-02T13:46:18Z .. 2026-04-02T13:46:18Z
- Range: 3m
- Root size: 50
- Sub multiplier: 2.0
- Sub size: 100
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.48
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 760a118f-721f-44bd-934c-f82d77251f73: 

| Metric | Value |
| --- | --- |
| Runs | 990 |
| Root avg wall (ms) | 222.15 |
| Root min/max wall (ms) | 50.12 / 936.84 |
| Root p50 wall (ms) | 194.89 |
| Root p90 wall (ms) | 327.03 |
| Root p99 wall (ms) | 567.17 |
| Root avg TTFB (ms) | 201.46 |
| Root p50 TTFB (ms) | 177.79 |
| Root p90 TTFB (ms) | 272.08 |
| Root p99 TTFB (ms) | 522.43 |
| Root avg read (ms) | 20.70 |
| Root p50 read (ms) | 0.83 |
| Root p90 read (ms) | 56.69 |
| Root p99 read (ms) | 130.54 |
| Root avg decode (ms) | 0.15 |
| Root p50 decode (ms) | 0.08 |
| Root p90 decode (ms) | 0.31 |
| Root p99 decode (ms) | 1.23 |
| Sub avg wall (ms) | 271.47 |
| Sub min/max wall (ms) | 45.26 / 2173.28 |
| Sub p50 wall (ms) | 243.81 |
| Sub p90 wall (ms) | 462.37 |
| Sub p99 wall (ms) | 840.53 |
| Sub avg TTFB (ms) | 207.82 |
| Sub p50 TTFB (ms) | 183.00 |
| Sub p90 TTFB (ms) | 268.35 |
| Sub p99 TTFB (ms) | 563.22 |
| Sub avg read (ms) | 63.64 |
| Sub p50 read (ms) | 43.22 |
| Sub p90 read (ms) | 137.19 |
| Sub p99 read (ms) | 356.01 |
| Sub avg decode (ms) | 0.45 |
| Sub p50 decode (ms) | 0.31 |
| Sub p90 decode (ms) | 1.18 |
| Sub p99 decode (ms) | 2.54 |
| Total avg wall (ms) | 494.26 |
| Total min/max (ms) | 146.59 / 2418.14 |
| Total p50 wall (ms) | 467.83 |
| Total p90 wall (ms) | 755.74 |
| Total p99 wall (ms) | 1154.07 |
| Root avg ES took (ms) | 8.94 |
| Sub avg ES took (ms) | 12.78 |
| Root hits (unique) | 0, 1, 2, 4, 5, 7, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21, 23, 25, 28, 29, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 54, 55, 60, 62, 76, 77 |
| Root brand IDs (unique) | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48 |
| Sub hits (unique) | 0, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 22, 28, 31, 35, 38, 45, 46, 47, 48, 52, 53, 54, 55, 61, 62, 63, 67, 68, 71, 72, 73, 75, 77, 78, 81, 84, 89, 90, 91, 93, 94, 95, 96, 99, 100, 102, 103, 111, 112, 115, 117, 123, 125, 127, 134, 148, 149, 152, 156 |

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
              "gte": "2026-01-02T13:46:18Z",
              "lte": "2026-04-02T13:46:18Z"
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
              "gte": "2026-01-02T13:46:18Z",
              "lte": "2026-04-02T13:46:18Z"
            }
          }
        },
        {
          "terms": {
            "related_product_transaction_uuid": []
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
