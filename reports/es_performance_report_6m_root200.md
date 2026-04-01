# ES Performance Report

- Generated: 2026-04-01T17:05:55Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-10-03T17:04:09Z .. 2026-04-01T17:04:09Z
- Range: 6m
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
| Root avg wall (ms) | 191.64 |
| Root min/max wall (ms) | 62.79 / 1993.81 |
| Sub avg wall (ms) | 222.85 |
| Sub min/max wall (ms) | 70.02 / 1286.59 |
| Total avg wall (ms) | 425.05 |
| Total min/max (ms) | 147.11 / 2631.63 |
| Root avg ES took (ms) | 123.64 |
| Sub avg ES took (ms) | 70.04 |
| Root hits (unique) | 1098, 1189, 1347, 1449, 1459, 1547, 1631, 1691, 1692, 1828, 1847, 1958, 1962, 2029, 2036, 2070, 2099, 2198, 2212, 2308, 2379, 2396, 2428, 2774 |
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
              "gte": "2025-10-03T17:04:09Z",
              "lte": "2026-04-01T17:04:09Z"
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
              "gte": "2025-10-03T17:04:09Z",
              "lte": "2026-04-01T17:04:09Z"
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
