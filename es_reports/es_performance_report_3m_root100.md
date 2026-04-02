# ES Performance Report

- Generated: 2026-04-02T13:48:38Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-02T13:47:59Z .. 2026-04-02T13:47:59Z
- Range: 3m
- Root size: 100
- Sub multiplier: 2.0
- Sub size: 200
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 25.06
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 37de0d90-8ae1-4daa-9af9-b8f26a0e28d1: 

| Metric | Value |
| --- | --- |
| Runs | 990 |
| Root avg wall (ms) | 194.59 |
| Root min/max wall (ms) | 47.47 / 725.86 |
| Root p50 wall (ms) | 176.31 |
| Root p90 wall (ms) | 252.17 |
| Root p99 wall (ms) | 516.07 |
| Root avg TTFB (ms) | 177.10 |
| Root p50 TTFB (ms) | 163.40 |
| Root p90 TTFB (ms) | 208.51 |
| Root p99 TTFB (ms) | 469.61 |
| Root avg read (ms) | 17.50 |
| Root p50 read (ms) | 0.89 |
| Root p90 read (ms) | 51.65 |
| Root p99 read (ms) | 91.32 |
| Root avg decode (ms) | 0.16 |
| Root p50 decode (ms) | 0.08 |
| Root p90 decode (ms) | 0.36 |
| Root p99 decode (ms) | 1.22 |
| Sub avg wall (ms) | 241.51 |
| Sub min/max wall (ms) | 45.77 / 895.00 |
| Sub p50 wall (ms) | 219.05 |
| Sub p90 wall (ms) | 377.46 |
| Sub p99 wall (ms) | 591.68 |
| Sub avg TTFB (ms) | 182.71 |
| Sub p50 TTFB (ms) | 166.08 |
| Sub p90 TTFB (ms) | 223.07 |
| Sub p99 TTFB (ms) | 480.92 |
| Sub avg read (ms) | 58.80 |
| Sub p50 read (ms) | 40.49 |
| Sub p90 read (ms) | 139.49 |
| Sub p99 read (ms) | 238.63 |
| Sub avg decode (ms) | 0.50 |
| Sub p50 decode (ms) | 0.30 |
| Sub p90 decode (ms) | 1.35 |
| Sub p99 decode (ms) | 3.02 |
| Total avg wall (ms) | 436.80 |
| Total min/max (ms) | 94.04 / 1115.63 |
| Total p50 wall (ms) | 422.89 |
| Total p90 wall (ms) | 638.35 |
| Total p99 wall (ms) | 934.70 |
| Root avg ES took (ms) | 8.90 |
| Sub avg ES took (ms) | 8.54 |
| Root hits (unique) | 0, 1, 2, 4, 5, 7, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21, 23, 25, 28, 29, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 54, 55, 60, 62, 76, 77 |
| Root brand IDs (unique) | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 46, 47, 49, 51, 57, 63, 72 |
| Sub hits (unique) | 0, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 22, 28, 31, 35, 38, 45, 46, 47, 48, 52, 53, 54, 55, 61, 62, 63, 67, 68, 71, 72, 73, 75, 77, 78, 81, 84, 89, 90, 91, 93, 94, 95, 96, 99, 100, 102, 103, 111, 115, 117, 123, 125, 134, 140, 163, 172, 181, 201, 219, 237 |

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
              "gte": "2026-01-02T13:47:59Z",
              "lte": "2026-04-02T13:47:59Z"
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
              "gte": "2026-01-02T13:47:59Z",
              "lte": "2026-04-02T13:47:59Z"
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
