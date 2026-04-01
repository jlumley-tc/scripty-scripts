# ES Performance Report

- Generated: 2026-04-01T16:57:34Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-01T16:57:04Z .. 2026-04-01T16:57:04Z
- Range: 3m
- Root size: 50
- Sub multiplier: 2.0
- Sub size: 100
- Iterations: 10
- Request cache: false
- Routing: enabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 250 |
| Root avg wall (ms) | 56.87 |
| Root min/max wall (ms) | 48.96 / 234.22 |
| Sub avg wall (ms) | 63.15 |
| Sub min/max wall (ms) | 47.06 / 237.17 |
| Total avg wall (ms) | 121.97 |
| Total min/max (ms) | 97.58 / 291.26 |
| Root avg ES took (ms) | 8.28 |
| Sub avg ES took (ms) | 8.50 |
| Root hits (unique) | 0, 1, 2, 5, 7, 10, 11, 12, 16, 18, 19, 20, 29, 45, 46, 48, 60, 77 |
| Root brand IDs (unique) | 0, 1, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 25, 32, 37, 41, 47, 48 |
| Sub hits (unique) | 0, 5, 10, 15, 19, 22, 28, 38, 48, 52, 53, 54, 55, 61, 78, 90, 95, 111, 148, 149 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: routing=<REDACTED_ACCOUNT>

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
              "gte": "2026-01-01T16:57:04Z",
              "lte": "2026-04-01T16:57:04Z"
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
          "terms": {
            "transaction_type": [
              "network_tax",
              "non_network_tax"
            ]
          }
        },
        {
          "range": {
            "transaction_date": {
              "gte": "2026-01-01T16:57:04Z",
              "lte": "2026-04-01T16:57:04Z"
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
