# ES Performance Report

- Generated: 2026-04-01T16:58:44Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-06T16:58:04Z .. 2026-04-01T16:58:04Z
- Range: 12m
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
| Root avg wall (ms) | 68.60 |
| Root min/max wall (ms) | 53.84 / 273.32 |
| Sub avg wall (ms) | 84.18 |
| Sub min/max wall (ms) | 54.44 / 1962.49 |
| Total avg wall (ms) | 156.55 |
| Total min/max (ms) | 114.75 / 2035.18 |
| Root avg ES took (ms) | 18.09 |
| Sub avg ES took (ms) | 12.58 |
| Root hits (unique) | 1123, 1214, 1227, 1366, 1520, 1530, 1606, 1653, 1742, 1762, 1870, 1888, 1985, 2046, 2070, 2113, 2122, 2229, 2273, 2355, 2394, 2432, 2457, 2812 |
| Root brand IDs (unique) | 34, 37, 38, 41, 42, 45, 46, 47, 48, 49, 50 |
| Sub hits (unique) | 69, 97, 121, 133, 140, 148, 149, 170, 172, 178, 182, 187, 192, 201, 211, 217, 226, 233, 235, 240, 252, 299, 332, 364 |

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
              "gte": "2025-04-06T16:58:04Z",
              "lte": "2026-04-01T16:58:04Z"
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
              "gte": "2025-04-06T16:58:04Z",
              "lte": "2026-04-01T16:58:04Z"
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
