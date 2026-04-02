# ES Performance Report

- Generated: 2026-04-02T13:50:11Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-02T13:49:34Z .. 2026-04-02T13:49:34Z
- Range: 3m
- Root size: 200
- Sub multiplier: 2.0
- Sub size: 400
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 27.32
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account a5a1c1b9-a9d3-470d-b922-fa8a37c42829: 

| Metric | Value |
| --- | --- |
| Runs | 994 |
| Root avg wall (ms) | 380.96 |
| Root min/max wall (ms) | 48.92 / 14272.13 |
| Root p50 wall (ms) | 177.24 |
| Root p90 wall (ms) | 294.40 |
| Root p99 wall (ms) | 3113.14 |
| Root avg TTFB (ms) | 362.82 |
| Root p50 TTFB (ms) | 163.90 |
| Root p90 TTFB (ms) | 215.41 |
| Root p99 TTFB (ms) | 3077.10 |
| Root avg read (ms) | 18.14 |
| Root p50 read (ms) | 0.97 |
| Root p90 read (ms) | 51.87 |
| Root p99 read (ms) | 106.77 |
| Root avg decode (ms) | 0.17 |
| Root p50 decode (ms) | 0.09 |
| Root p90 decode (ms) | 0.35 |
| Root p99 decode (ms) | 1.48 |
| Sub avg wall (ms) | 538.68 |
| Sub min/max wall (ms) | 44.84 / 15921.60 |
| Sub p50 wall (ms) | 224.44 |
| Sub p90 wall (ms) | 830.62 |
| Sub p99 wall (ms) | 3710.05 |
| Sub avg TTFB (ms) | 479.38 |
| Sub p50 TTFB (ms) | 167.77 |
| Sub p90 TTFB (ms) | 791.91 |
| Sub p99 TTFB (ms) | 3669.95 |
| Sub avg read (ms) | 59.29 |
| Sub p50 read (ms) | 40.63 |
| Sub p90 read (ms) | 140.52 |
| Sub p99 read (ms) | 297.53 |
| Sub avg decode (ms) | 0.55 |
| Sub p50 decode (ms) | 0.31 |
| Sub p90 decode (ms) | 1.44 |
| Sub p99 decode (ms) | 4.15 |
| Total avg wall (ms) | 920.39 |
| Total min/max (ms) | 142.78 / 16076.27 |
| Total p50 wall (ms) | 434.19 |
| Total p90 wall (ms) | 3168.16 |
| Total p99 wall (ms) | 13071.11 |
| Root avg ES took (ms) | 8.33 |
| Sub avg ES took (ms) | 8.22 |
| Root hits (unique) | 0, 1, 2, 4, 5, 7, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21, 23, 25, 28, 29, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 54, 55, 60, 62, 76, 77 |
| Root brand IDs (unique) | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 46, 47, 49, 51, 57, 63, 72 |
| Sub hits (unique) | 0, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 22, 28, 31, 35, 38, 45, 46, 47, 48, 52, 53, 54, 55, 61, 62, 63, 67, 68, 71, 72, 73, 75, 77, 78, 81, 84, 89, 90, 91, 93, 94, 95, 96, 99, 100, 102, 103, 111, 115, 117, 123, 125, 134, 140, 163, 172, 181, 201, 219, 237 |

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
              "gte": "2026-01-02T13:49:34Z",
              "lte": "2026-04-02T13:49:34Z"
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
              "gte": "2026-01-02T13:49:34Z",
              "lte": "2026-04-02T13:49:34Z"
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
