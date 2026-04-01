# ES Performance Report

- Generated: 2026-04-01T17:03:08Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2024-04-11T17:02:18Z .. 2026-04-01T17:02:18Z
- Range: 24m
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
| Root avg wall (ms) | 79.11 |
| Root min/max wall (ms) | 56.17 / 705.32 |
| Sub avg wall (ms) | 116.63 |
| Sub min/max wall (ms) | 59.65 / 677.52 |
| Total avg wall (ms) | 201.67 |
| Total min/max (ms) | 123.95 / 890.12 |
| Root avg ES took (ms) | 20.35 |
| Sub avg ES took (ms) | 22.52 |
| Root hits (unique) | 1123, 1227, 1228, 1395, 1533, 1602, 1669, 1672, 1763, 1806, 1918, 1923, 1994, 1997, 2070, 2080, 2153, 2167, 2273, 2329, 2381, 2407, 2432, 2475, 2854 |
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
              "gte": "2024-04-11T17:02:18Z",
              "lte": "2026-04-01T17:02:18Z"
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
              "gte": "2024-04-11T17:02:18Z",
              "lte": "2026-04-01T17:02:18Z"
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
