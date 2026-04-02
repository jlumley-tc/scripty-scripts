# ES Performance Report

- Generated: 2026-04-02T13:47:58Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-03T13:47:43Z .. 2026-04-02T13:47:43Z
- Range: 1m
- Root size: 100
- Sub multiplier: 2.0
- Sub size: 200
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 64.58
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 1000 |
| Root avg wall (ms) | 75.40 |
| Root min/max wall (ms) | 46.58 / 11660.76 |
| Root p50 wall (ms) | 52.54 |
| Root p90 wall (ms) | 91.64 |
| Root p99 wall (ms) | 235.03 |
| Root avg TTFB (ms) | 73.33 |
| Root p50 TTFB (ms) | 51.60 |
| Root p90 TTFB (ms) | 88.92 |
| Root p99 TTFB (ms) | 234.21 |
| Root avg read (ms) | 2.07 |
| Root p50 read (ms) | 0.81 |
| Root p90 read (ms) | 1.55 |
| Root p99 read (ms) | 39.93 |
| Root avg decode (ms) | 0.12 |
| Root p50 decode (ms) | 0.04 |
| Root p90 decode (ms) | 0.32 |
| Root p99 decode (ms) | 0.53 |
| Sub avg wall (ms) | 67.70 |
| Sub min/max wall (ms) | 44.82 / 493.64 |
| Sub p50 wall (ms) | 52.23 |
| Sub p90 wall (ms) | 98.07 |
| Sub p99 wall (ms) | 233.08 |
| Sub avg TTFB (ms) | 56.55 |
| Sub p50 TTFB (ms) | 50.91 |
| Sub p90 TTFB (ms) | 61.41 |
| Sub p99 TTFB (ms) | 231.08 |
| Sub avg read (ms) | 11.15 |
| Sub p50 read (ms) | 0.93 |
| Sub p90 read (ms) | 40.56 |
| Sub p99 read (ms) | 118.93 |
| Sub avg decode (ms) | 0.29 |
| Sub p50 decode (ms) | 0.02 |
| Sub p90 decode (ms) | 0.75 |
| Sub p99 decode (ms) | 2.77 |
| Total avg wall (ms) | 143.55 |
| Total min/max (ms) | 91.91 / 11758.17 |
| Total p50 wall (ms) | 106.43 |
| Total p90 wall (ms) | 196.32 |
| Total p99 wall (ms) | 359.16 |
| Root avg ES took (ms) | 6.25 |
| Sub avg ES took (ms) | 5.12 |
| Root hits (unique) | 0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26 |
| Root brand IDs (unique) | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 23, 24 |
| Sub hits (unique) | 0, 7, 8, 9, 10, 11, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 35, 36, 38, 39, 41, 42, 43, 44, 51, 55, 56, 74 |

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
              "gte": "2026-03-03T13:47:43Z",
              "lte": "2026-04-02T13:47:43Z"
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
              "gte": "2026-03-03T13:47:43Z",
              "lte": "2026-04-02T13:47:43Z"
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
