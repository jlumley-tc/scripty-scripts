# ES Performance Report

- Generated: 2026-04-01T16:55:49Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-06T16:55:15Z .. 2026-04-01T16:55:15Z
- Range: 12m
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
| Root avg wall (ms) | 69.91 |
| Root min/max wall (ms) | 54.73 / 253.76 |
| Sub avg wall (ms) | 61.34 |
| Sub min/max wall (ms) | 51.95 / 152.42 |
| Total avg wall (ms) | 133.69 |
| Total min/max (ms) | 110.26 / 407.90 |
| Root avg ES took (ms) | 17.80 |
| Sub avg ES took (ms) | 10.52 |
| Root hits (unique) | 1123, 1214, 1227, 1366, 1520, 1530, 1606, 1653, 1742, 1762, 1870, 1888, 1985, 2046, 2070, 2113, 2122, 2229, 2273, 2355, 2394, 2432, 2457, 2812 |
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
              "gte": "2025-04-06T16:55:15Z",
              "lte": "2026-04-01T16:55:15Z"
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
              "gte": "2025-04-06T16:55:15Z",
              "lte": "2026-04-01T16:55:15Z"
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
