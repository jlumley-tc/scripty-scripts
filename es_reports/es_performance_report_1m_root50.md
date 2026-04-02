# ES Performance Report

- Generated: 2026-04-02T13:46:18Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-03T13:46:05Z .. 2026-04-02T13:46:05Z
- Range: 1m
- Root size: 50
- Sub multiplier: 2.0
- Sub size: 100
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 78.20
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 1000 |
| Root avg wall (ms) | 62.67 |
| Root min/max wall (ms) | 45.97 / 495.63 |
| Root p50 wall (ms) | 52.91 |
| Root p90 wall (ms) | 77.51 |
| Root p99 wall (ms) | 234.01 |
| Root avg TTFB (ms) | 61.53 |
| Root p50 TTFB (ms) | 51.91 |
| Root p90 TTFB (ms) | 72.06 |
| Root p99 TTFB (ms) | 232.90 |
| Root avg read (ms) | 1.14 |
| Root p50 read (ms) | 0.86 |
| Root p90 read (ms) | 1.55 |
| Root p99 read (ms) | 5.43 |
| Root avg decode (ms) | 0.10 |
| Root p50 decode (ms) | 0.03 |
| Root p90 decode (ms) | 0.30 |
| Root p99 decode (ms) | 0.55 |
| Sub avg wall (ms) | 60.86 |
| Sub min/max wall (ms) | 44.71 / 513.44 |
| Sub p50 wall (ms) | 52.24 |
| Sub p90 wall (ms) | 91.46 |
| Sub p99 wall (ms) | 233.18 |
| Sub avg TTFB (ms) | 57.14 |
| Sub p50 TTFB (ms) | 51.15 |
| Sub p90 TTFB (ms) | 62.29 |
| Sub p99 TTFB (ms) | 231.54 |
| Sub avg read (ms) | 3.72 |
| Sub p50 read (ms) | 0.94 |
| Sub p90 read (ms) | 3.17 |
| Sub p99 read (ms) | 43.15 |
| Sub avg decode (ms) | 0.24 |
| Sub p50 decode (ms) | 0.03 |
| Sub p90 decode (ms) | 0.69 |
| Sub p99 decode (ms) | 2.54 |
| Total avg wall (ms) | 123.92 |
| Total min/max (ms) | 91.56 / 598.85 |
| Total p50 wall (ms) | 106.81 |
| Total p90 wall (ms) | 159.16 |
| Total p99 wall (ms) | 310.12 |
| Root avg ES took (ms) | 7.45 |
| Sub avg ES took (ms) | 6.08 |
| Root hits (unique) | 0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26 |
| Root brand IDs (unique) | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 23, 24 |
| Sub hits (unique) | 0, 7, 8, 9, 10, 11, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 35, 36, 38, 39, 41, 42, 43, 44, 51, 55, 56, 74 |

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
              "gte": "2026-03-03T13:46:05Z",
              "lte": "2026-04-02T13:46:05Z"
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
              "gte": "2026-03-03T13:46:05Z",
              "lte": "2026-04-02T13:46:05Z"
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
