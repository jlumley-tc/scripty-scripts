# ES Performance Report

- Generated: 2026-04-01T16:59:59Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2026-03-02T16:59:31Z .. 2026-04-01T16:59:31Z
- Range: 1m
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
| Root avg wall (ms) | 57.40 |
| Root min/max wall (ms) | 48.41 / 234.85 |
| Sub avg wall (ms) | 55.17 |
| Sub min/max wall (ms) | 46.13 / 241.39 |
| Total avg wall (ms) | 113.42 |
| Total min/max (ms) | 94.74 / 298.04 |
| Root avg ES took (ms) | 7.42 |
| Sub avg ES took (ms) | 5.80 |
| Root hits (unique) | 0, 1, 5, 10, 11, 13, 14, 16, 20, 22, 26 |
| Root brand IDs (unique) | 0, 4, 9, 10, 12, 13, 15, 19, 24 |
| Sub hits (unique) | 0, 16, 19, 22, 24, 28, 33, 43, 74 |

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
              "gte": "2026-03-02T16:59:31Z",
              "lte": "2026-04-01T16:59:31Z"
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
              "gte": "2026-03-02T16:59:31Z",
              "lte": "2026-04-01T16:59:31Z"
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
