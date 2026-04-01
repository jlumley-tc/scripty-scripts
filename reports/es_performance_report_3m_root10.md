# ES Performance Report

- Generated: 2026-04-01T16:49:50Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-01-01T16:49:15Z .. 2026-04-01T16:49:15Z
- Range: 3m
- Root size: 10
- Sub multiplier: 2.0
- Sub size: 20
- Iterations: 10
- Request cache: false
- Routing: disabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 250 |
| Root avg wall (ms) | 71.25 |
| Root min/max wall (ms) | 49.40 / 820.69 |
| Sub avg wall (ms) | 69.23 |
| Sub min/max wall (ms) | 46.65 / 859.20 |
| Total avg wall (ms) | 141.47 |
| Total min/max (ms) | 97.72 / 918.22 |
| Root avg ES took (ms) | 22.35 |
| Sub avg ES took (ms) | 9.96 |
| Root hits (unique) | 0, 1, 2, 5, 7, 10, 11, 12, 16, 18, 19, 20, 29, 45, 46, 48, 60, 77 |
| Root brand IDs (unique) | 0, 1, 3, 5, 6, 7, 8, 9, 10 |
| Sub hits (unique) | 0, 5, 10, 12, 15, 18, 19, 21, 22, 23, 24, 25, 28, 32, 36, 40, 51, 52, 55 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

### Root Query

```json
{
  "size": 10,
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
              "gte": "2026-01-01T16:49:15Z",
              "lte": "2026-04-01T16:49:15Z"
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
  "size": 20,
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
              "gte": "2026-01-01T16:49:15Z",
              "lte": "2026-04-01T16:49:15Z"
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
