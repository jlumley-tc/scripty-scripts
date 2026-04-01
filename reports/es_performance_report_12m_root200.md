# ES Performance Report

- Generated: 2026-04-01T17:06:57Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-06T17:05:55Z .. 2026-04-01T17:05:55Z
- Range: 12m
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
| Root avg wall (ms) | 78.02 |
| Root min/max wall (ms) | 61.15 / 525.12 |
| Sub avg wall (ms) | 157.71 |
| Sub min/max wall (ms) | 67.99 / 1139.09 |
| Total avg wall (ms) | 245.34 |
| Total min/max (ms) | 140.75 / 1223.61 |
| Root avg ES took (ms) | 23.57 |
| Sub avg ES took (ms) | 19.86 |
| Root hits (unique) | 1123, 1214, 1227, 1366, 1520, 1530, 1606, 1653, 1742, 1762, 1870, 1888, 1985, 2046, 2070, 2113, 2122, 2229, 2273, 2355, 2394, 2432, 2457, 2812 |
| Root brand IDs (unique) | 178, 181, 182, 187, 189, 192, 195, 196, 198, 199, 200 |
| Sub hits (unique) | 406, 545, 560, 638, 673, 686, 693, 730, 768, 802, 834, 838, 880, 901, 913, 935, 937, 943, 988, 1005, 1027, 1185, 1237, 1334, 1664 |

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
              "gte": "2025-04-06T17:05:55Z",
              "lte": "2026-04-01T17:05:55Z"
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
              "gte": "2025-04-06T17:05:55Z",
              "lte": "2026-04-01T17:05:55Z"
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
