# ES Performance Report

- Generated: 2026-04-02T13:45:26Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-02T13:44:45Z .. 2026-04-02T13:44:45Z
- Range: 3m
- Root size: 25
- Sub multiplier: 2.0
- Sub size: 50
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 24.09
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 1e86f823-ffdd-4068-bda9-eec03632e9f6: 

| Metric | Value |
| --- | --- |
| Runs | 990 |
| Root avg wall (ms) | 191.93 |
| Root min/max wall (ms) | 48.61 / 720.18 |
| Root p50 wall (ms) | 174.20 |
| Root p90 wall (ms) | 307.35 |
| Root p99 wall (ms) | 573.88 |
| Root avg TTFB (ms) | 187.43 |
| Root p50 TTFB (ms) | 163.06 |
| Root p90 TTFB (ms) | 307.03 |
| Root p99 TTFB (ms) | 569.43 |
| Root avg read (ms) | 4.50 |
| Root p50 read (ms) | 0.76 |
| Root p90 read (ms) | 14.07 |
| Root p99 read (ms) | 22.42 |
| Root avg decode (ms) | 0.12 |
| Root p50 decode (ms) | 0.10 |
| Root p90 decode (ms) | 0.20 |
| Root p99 decode (ms) | 0.49 |
| Sub avg wall (ms) | 212.53 |
| Sub min/max wall (ms) | 48.44 / 1017.88 |
| Sub p50 wall (ms) | 214.12 |
| Sub p90 wall (ms) | 293.29 |
| Sub p99 wall (ms) | 540.65 |
| Sub avg TTFB (ms) | 185.77 |
| Sub p50 TTFB (ms) | 164.74 |
| Sub p90 TTFB (ms) | 251.86 |
| Sub p99 TTFB (ms) | 504.82 |
| Sub avg read (ms) | 26.76 |
| Sub p50 read (ms) | 39.01 |
| Sub p90 read (ms) | 53.56 |
| Sub p99 read (ms) | 68.11 |
| Sub avg decode (ms) | 0.32 |
| Sub p50 decode (ms) | 0.27 |
| Sub p90 decode (ms) | 0.56 |
| Sub p99 decode (ms) | 2.33 |
| Total avg wall (ms) | 404.93 |
| Total min/max (ms) | 182.86 / 1196.45 |
| Total p50 wall (ms) | 391.28 |
| Total p90 wall (ms) | 599.62 |
| Total p99 wall (ms) | 899.01 |
| Root avg ES took (ms) | 15.69 |
| Sub avg ES took (ms) | 14.62 |
| Root hits (unique) | 0, 1, 2, 4, 5, 7, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21, 23, 25, 28, 29, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 54, 55, 60, 62, 76, 77 |
| Root brand IDs (unique) | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24 |
| Sub hits (unique) | 0, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 22, 26, 28, 31, 33, 34, 35, 38, 40, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 65, 67, 70, 71, 72, 73, 74, 78, 82, 95, 97 |

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
              "gte": "2026-01-02T13:44:45Z",
              "lte": "2026-04-02T13:44:45Z"
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
              "gte": "2026-01-02T13:44:45Z",
              "lte": "2026-04-02T13:44:45Z"
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
