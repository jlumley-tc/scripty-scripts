# ES Performance Report

- Generated: 2026-04-01T16:54:39Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-01T16:54:03Z .. 2026-04-01T16:54:03Z
- Range: 3m
- Root size: 25
- Sub multiplier: 2.0
- Sub size: 50
- Iterations: 10
- Request cache: false
- Routing: enabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 250 |
| Root avg wall (ms) | 67.31 |
| Root min/max wall (ms) | 48.63 / 429.21 |
| Sub avg wall (ms) | 73.11 |
| Sub min/max wall (ms) | 47.00 / 1021.84 |
| Total avg wall (ms) | 141.97 |
| Total min/max (ms) | 97.74 / 1145.09 |
| Root avg ES took (ms) | 12.48 |
| Sub avg ES took (ms) | 10.94 |
| Root hits (unique) | 0, 1, 2, 5, 7, 10, 11, 12, 16, 18, 19, 20, 29, 45, 46, 48, 60, 77 |
| Root brand IDs (unique) | 0, 1, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 20, 22, 23, 24 |
| Sub hits (unique) | 0, 5, 10, 15, 19, 22, 26, 28, 33, 38, 47, 52, 53, 54, 55, 58, 60, 74, 78, 95 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: routing=<REDACTED_ACCOUNT>

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
              "gte": "2026-01-01T16:54:03Z",
              "lte": "2026-04-01T16:54:03Z"
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
              "gte": "2026-01-01T16:54:03Z",
              "lte": "2026-04-01T16:54:03Z"
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
