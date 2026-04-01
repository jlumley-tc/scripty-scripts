# ES Performance Report

- Generated: 2026-04-01T16:59:31Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2024-04-11T16:58:44Z .. 2026-04-01T16:58:44Z
- Range: 24m
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
| Root avg wall (ms) | 69.04 |
| Root min/max wall (ms) | 54.19 / 366.18 |
| Sub avg wall (ms) | 114.96 |
| Sub min/max wall (ms) | 55.15 / 9937.66 |
| Total avg wall (ms) | 187.86 |
| Total min/max (ms) | 117.09 / 10014.41 |
| Root avg ES took (ms) | 19.44 |
| Sub avg ES took (ms) | 15.59 |
| Root hits (unique) | 1123, 1227, 1228, 1395, 1533, 1602, 1669, 1672, 1763, 1806, 1918, 1923, 1994, 1997, 2070, 2080, 2153, 2167, 2273, 2329, 2381, 2407, 2432, 2475, 2854 |
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
              "gte": "2024-04-11T16:58:44Z",
              "lte": "2026-04-01T16:58:44Z"
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
              "gte": "2024-04-11T16:58:44Z",
              "lte": "2026-04-01T16:58:44Z"
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
