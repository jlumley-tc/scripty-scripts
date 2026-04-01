# ES Performance Report

- Generated: 2026-04-01T17:01:33Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-03T17:00:32Z .. 2026-04-01T17:00:32Z
- Range: 6m
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
| Root avg wall (ms) | 98.74 |
| Root min/max wall (ms) | 57.58 / 1433.26 |
| Sub avg wall (ms) | 138.77 |
| Sub min/max wall (ms) | 59.51 / 997.41 |
| Total avg wall (ms) | 243.38 |
| Total min/max (ms) | 123.96 / 2101.67 |
| Root avg ES took (ms) | 42.25 |
| Sub avg ES took (ms) | 41.72 |
| Root hits (unique) | 1098, 1189, 1347, 1449, 1459, 1547, 1631, 1691, 1692, 1828, 1847, 1958, 1962, 2029, 2036, 2070, 2099, 2198, 2212, 2308, 2379, 2396, 2428, 2774 |
| Root brand IDs (unique) | 79, 81, 87, 89, 92, 95, 96, 98, 99, 100 |
| Sub hits (unique) | 179, 261, 280, 293, 299, 313, 342, 364, 380, 384, 386, 394, 412, 431, 451, 453, 456, 466, 485, 488, 493, 501, 612, 664, 798 |

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
              "gte": "2025-10-03T17:00:32Z",
              "lte": "2026-04-01T17:00:32Z"
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
              "gte": "2025-10-03T17:00:32Z",
              "lte": "2026-04-01T17:00:32Z"
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
