# ES Performance Report

- Generated: 2026-04-01T17:00:32Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-01T16:59:59Z .. 2026-04-01T16:59:59Z
- Range: 3m
- Root size: 100
- Sub multiplier: 2.0
- Sub size: 200
- Iterations: 10
- Request cache: false
- Routing: enabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 250 |
| Root avg wall (ms) | 62.83 |
| Root min/max wall (ms) | 49.25 / 655.37 |
| Sub avg wall (ms) | 64.28 |
| Sub min/max wall (ms) | 46.97 / 240.58 |
| Total avg wall (ms) | 129.31 |
| Total min/max (ms) | 97.04 / 703.24 |
| Root avg ES took (ms) | 8.44 |
| Sub avg ES took (ms) | 8.29 |
| Root hits (unique) | 0, 1, 2, 5, 7, 10, 11, 12, 16, 18, 19, 20, 29, 45, 46, 48, 60, 77 |
| Root brand IDs (unique) | 0, 1, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 25, 32, 37, 41, 57, 72 |
| Sub hits (unique) | 0, 5, 10, 15, 19, 22, 28, 38, 48, 52, 53, 54, 55, 61, 78, 90, 95, 111, 219, 237 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: routing=<REDACTED_ACCOUNT>

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
              "gte": "2026-01-01T16:59:59Z",
              "lte": "2026-04-01T16:59:59Z"
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
              "gte": "2026-01-01T16:59:59Z",
              "lte": "2026-04-01T16:59:59Z"
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
