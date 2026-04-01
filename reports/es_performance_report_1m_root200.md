# ES Performance Report

- Generated: 2026-04-01T17:03:37Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-02T17:03:09Z .. 2026-04-01T17:03:09Z
- Range: 1m
- Root size: 200
- Sub multiplier: 2.0
- Sub size: 400
- Iterations: 10
- Request cache: false
- Routing: enabled

## Results Summary

| Metric | Value |
| --- | --- |
| Runs | 250 |
| Root avg wall (ms) | 58.87 |
| Root min/max wall (ms) | 49.59 / 527.35 |
| Sub avg wall (ms) | 54.92 |
| Sub min/max wall (ms) | 46.59 / 240.90 |
| Total avg wall (ms) | 114.66 |
| Total min/max (ms) | 98.20 / 576.95 |
| Root avg ES took (ms) | 7.18 |
| Sub avg ES took (ms) | 5.86 |
| Root hits (unique) | 0, 1, 5, 10, 11, 13, 14, 16, 20, 22, 26 |
| Root brand IDs (unique) | 0, 4, 9, 10, 12, 13, 15, 19, 24 |
| Sub hits (unique) | 0, 16, 19, 22, 24, 28, 33, 43, 74 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: routing=<REDACTED_ACCOUNT>

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
              "gte": "2026-03-02T17:03:09Z",
              "lte": "2026-04-01T17:03:09Z"
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
              "gte": "2026-03-02T17:03:09Z",
              "lte": "2026-04-01T17:03:09Z"
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
