# ES Performance Report

- Generated: 2026-04-02T13:49:34Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-03T13:49:21Z .. 2026-04-02T13:49:21Z
- Range: 1m
- Root size: 200
- Sub multiplier: 2.0
- Sub size: 400
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 78.76
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 1000 |
| Root avg wall (ms) | 62.74 |
| Root min/max wall (ms) | 46.38 / 3029.26 |
| Root p50 wall (ms) | 52.10 |
| Root p90 wall (ms) | 59.52 |
| Root p99 wall (ms) | 235.38 |
| Root avg TTFB (ms) | 61.65 |
| Root p50 TTFB (ms) | 51.26 |
| Root p90 TTFB (ms) | 58.04 |
| Root p99 TTFB (ms) | 234.24 |
| Root avg read (ms) | 1.09 |
| Root p50 read (ms) | 0.79 |
| Root p90 read (ms) | 1.30 |
| Root p99 read (ms) | 4.05 |
| Root avg decode (ms) | 0.13 |
| Root p50 decode (ms) | 0.04 |
| Root p90 decode (ms) | 0.34 |
| Root p99 decode (ms) | 0.56 |
| Sub avg wall (ms) | 61.55 |
| Sub min/max wall (ms) | 44.79 / 520.59 |
| Sub p50 wall (ms) | 51.44 |
| Sub p90 wall (ms) | 92.01 |
| Sub p99 wall (ms) | 232.80 |
| Sub avg TTFB (ms) | 57.34 |
| Sub p50 TTFB (ms) | 50.33 |
| Sub p90 TTFB (ms) | 56.94 |
| Sub p99 TTFB (ms) | 231.86 |
| Sub avg read (ms) | 4.21 |
| Sub p50 read (ms) | 0.91 |
| Sub p90 read (ms) | 3.67 |
| Sub p99 read (ms) | 42.18 |
| Sub avg decode (ms) | 0.29 |
| Sub p50 decode (ms) | 0.03 |
| Sub p90 decode (ms) | 0.83 |
| Sub p99 decode (ms) | 2.35 |
| Total avg wall (ms) | 124.75 |
| Total min/max (ms) | 92.59 / 3109.12 |
| Total p50 wall (ms) | 104.82 |
| Total p90 wall (ms) | 151.89 |
| Total p99 wall (ms) | 334.59 |
| Root avg ES took (ms) | 6.25 |
| Sub avg ES took (ms) | 5.03 |
| Root hits (unique) | 0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26 |
| Root brand IDs (unique) | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 23, 24 |
| Sub hits (unique) | 0, 7, 8, 9, 10, 11, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 35, 36, 38, 39, 41, 42, 43, 44, 51, 55, 56, 74 |

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
              "gte": "2026-03-03T13:49:21Z",
              "lte": "2026-04-02T13:49:21Z"
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
              "gte": "2026-03-03T13:49:21Z",
              "lte": "2026-04-02T13:49:21Z"
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
