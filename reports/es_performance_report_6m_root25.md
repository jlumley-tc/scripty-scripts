# ES Performance Report

- Generated: 2026-04-01T16:55:15Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-03T16:54:39Z .. 2026-04-01T16:54:39Z
- Range: 6m
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
| Root avg wall (ms) | 74.27 |
| Root min/max wall (ms) | 53.08 / 448.49 |
| Sub avg wall (ms) | 67.99 |
| Sub min/max wall (ms) | 52.51 / 526.36 |
| Total avg wall (ms) | 144.72 |
| Total min/max (ms) | 111.52 / 604.19 |
| Root avg ES took (ms) | 21.42 |
| Sub avg ES took (ms) | 11.36 |
| Root hits (unique) | 1098, 1189, 1347, 1449, 1459, 1547, 1631, 1691, 1692, 1828, 1847, 1958, 1962, 2029, 2036, 2070, 2099, 2198, 2212, 2308, 2379, 2396, 2428, 2774 |
| Root brand IDs (unique) | 16, 17, 19, 20, 21, 22, 23, 24, 25 |
| Sub hits (unique) | 26, 33, 47, 58, 60, 61, 74, 80, 84, 85, 87, 94, 95, 102, 111, 112, 115, 116, 126, 143, 147, 163 |

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
              "gte": "2025-10-03T16:54:39Z",
              "lte": "2026-04-01T16:54:39Z"
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
              "gte": "2025-10-03T16:54:39Z",
              "lte": "2026-04-01T16:54:39Z"
            }
          }
        },
        {
          "terms": {
            "related_product_transaction_uuid": [
              "<REDACTED_TXN_1>",
              "<REDACTED_TXN_2>",
              "<REDACTED_TXN_3>",
              "<REDACTED_TXN_4>",
              "<REDACTED_TXN_5>",
              "<REDACTED_TXN_6>",
              "<REDACTED_TXN_7>",
              "<REDACTED_TXN_8>",
              "<REDACTED_TXN_9>",
              "<REDACTED_TXN_10>",
              "<REDACTED_TXN_MORE>"
            ]
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
