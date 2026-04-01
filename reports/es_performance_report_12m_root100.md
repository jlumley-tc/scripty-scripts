# ES Performance Report

- Generated: 2026-04-01T17:02:18Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-06T17:01:33Z .. 2026-04-01T17:01:33Z
- Range: 12m
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
| Root avg wall (ms) | 75.21 |
| Root min/max wall (ms) | 57.33 / 307.30 |
| Sub avg wall (ms) | 97.91 |
| Sub min/max wall (ms) | 58.74 / 451.28 |
| Total avg wall (ms) | 179.01 |
| Total min/max (ms) | 122.84 / 735.08 |
| Root avg ES took (ms) | 21.00 |
| Sub avg ES took (ms) | 20.00 |
| Root hits (unique) | 1123, 1214, 1227, 1366, 1520, 1530, 1606, 1653, 1742, 1762, 1870, 1888, 1985, 2046, 2070, 2113, 2122, 2229, 2273, 2355, 2394, 2432, 2457, 2812 |
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
              "gte": "2025-04-06T17:01:33Z",
              "lte": "2026-04-01T17:01:33Z"
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
              "gte": "2025-04-06T17:01:33Z",
              "lte": "2026-04-01T17:01:33Z"
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
