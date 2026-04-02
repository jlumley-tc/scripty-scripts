# ES Performance Report

- Generated: 2026-04-02T14:23:22Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-07T14:22:40Z .. 2026-04-02T14:22:40Z
- Range: 12m
- Root size: 50
- Sub multiplier: 2.0
- Sub size: 100
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.56
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary


| Metric | Value |
| --- | --- |
| Runs | 990 |
| Root avg wall (ms) | 249.50 |
| Root min/max wall (ms) | 213.25 / 773.23 |
| Root p50 wall (ms) | 225.70 |
| Root p90 wall (ms) | 300.61 |
| Root p99 wall (ms) | 505.02 |
| Root avg TTFB (ms) | 198.90 |
| Root p50 TTFB (ms) | 179.29 |
| Root p90 TTFB (ms) | 245.31 |
| Root p99 TTFB (ms) | 471.97 |
| Root avg read (ms) | 50.60 |
| Root p50 read (ms) | 52.49 |
| Root p90 read (ms) | 64.26 |
| Root p99 read (ms) | 70.51 |
| Root avg decode (ms) | 0.30 |
| Root p50 decode (ms) | 0.27 |
| Root p90 decode (ms) | 0.35 |
| Root p99 decode (ms) | 1.17 |
| Sub avg wall (ms) | 308.41 |
| Sub min/max wall (ms) | 168.21 / 629.71 |
| Sub p50 wall (ms) | 286.81 |
| Sub p90 wall (ms) | 359.77 |
| Sub p99 wall (ms) | 561.14 |
| Sub avg TTFB (ms) | 198.40 |
| Sub p50 TTFB (ms) | 177.21 |
| Sub p90 TTFB (ms) | 250.34 |
| Sub p99 TTFB (ms) | 470.53 |
| Sub avg read (ms) | 110.01 |
| Sub p50 read (ms) | 116.59 |
| Sub p90 read (ms) | 130.32 |
| Sub p99 read (ms) | 138.07 |
| Sub avg decode (ms) | 0.73 |
| Sub p50 decode (ms) | 0.61 |
| Sub p90 decode (ms) | 1.26 |
| Sub p99 decode (ms) | 2.14 |
| Total avg wall (ms) | 558.99 |
| Total min/max (ms) | 464.72 / 1235.66 |
| Total p50 wall (ms) | 520.82 |
| Total p90 wall (ms) | 732.64 |
| Total p99 wall (ms) | 946.75 |
| Root avg ES took (ms) | 18.84 |
| Sub avg ES took (ms) | 15.03 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

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
              "gte": "2025-04-07T14:22:40Z",
              "lte": "2026-04-02T14:22:40Z"
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
          "range": {
            "transaction_date": {
              "gte": "2025-04-07T14:22:40Z",
              "lte": "2026-04-02T14:22:40Z"
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
