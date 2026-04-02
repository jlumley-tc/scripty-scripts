# ES Performance Report

- Generated: 2026-04-02T13:44:44Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-03T13:44:03Z .. 2026-04-02T13:44:03Z
- Range: 1m
- Root size: 25
- Sub multiplier: 2.0
- Sub size: 50
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.91
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account 6bd997a0-387c-4bea-9b58-6000dc953aac: 

| Metric | Value |
| --- | --- |
| Runs | 991 |
| Root avg wall (ms) | 177.17 |
| Root min/max wall (ms) | 130.56 / 640.60 |
| Root p50 wall (ms) | 144.87 |
| Root p90 wall (ms) | 236.91 |
| Root p99 wall (ms) | 472.74 |
| Root avg TTFB (ms) | 174.75 |
| Root p50 TTFB (ms) | 144.11 |
| Root p90 TTFB (ms) | 235.81 |
| Root p99 TTFB (ms) | 463.58 |
| Root avg read (ms) | 2.42 |
| Root p50 read (ms) | 0.51 |
| Root p90 read (ms) | 12.18 |
| Root p99 read (ms) | 24.06 |
| Root avg decode (ms) | 0.07 |
| Root p50 decode (ms) | 0.02 |
| Root p90 decode (ms) | 0.16 |
| Root p99 decode (ms) | 0.32 |
| Sub avg wall (ms) | 182.59 |
| Sub min/max wall (ms) | 49.43 / 1068.71 |
| Sub p50 wall (ms) | 144.81 |
| Sub p90 wall (ms) | 243.60 |
| Sub p99 wall (ms) | 502.82 |
| Sub avg TTFB (ms) | 172.50 |
| Sub p50 TTFB (ms) | 143.27 |
| Sub p90 TTFB (ms) | 220.12 |
| Sub p99 TTFB (ms) | 475.43 |
| Sub avg read (ms) | 10.09 |
| Sub p50 read (ms) | 0.68 |
| Sub p90 read (ms) | 39.88 |
| Sub p99 read (ms) | 57.98 |
| Sub avg decode (ms) | 0.16 |
| Sub p50 decode (ms) | 0.02 |
| Sub p90 decode (ms) | 0.37 |
| Sub p99 decode (ms) | 2.15 |
| Total avg wall (ms) | 360.02 |
| Total min/max (ms) | 262.40 / 1356.99 |
| Total p50 wall (ms) | 315.79 |
| Total p90 wall (ms) | 531.85 |
| Total p99 wall (ms) | 808.75 |
| Root avg ES took (ms) | 15.79 |
| Sub avg ES took (ms) | 11.98 |
| Root hits (unique) | 0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26 |
| Root brand IDs (unique) | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 23, 24 |
| Sub hits (unique) | 0, 7, 8, 9, 10, 11, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 35, 36, 38, 39, 41, 42, 43, 44, 51, 55, 56, 74 |

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
              "gte": "2026-03-03T13:44:03Z",
              "lte": "2026-04-02T13:44:03Z"
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
              "gte": "2026-03-03T13:44:03Z",
              "lte": "2026-04-02T13:44:03Z"
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
