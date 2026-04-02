# ES Performance Report

- Generated: 2026-04-02T14:22:40Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-07T14:21:58Z .. 2026-04-02T14:21:58Z
- Range: 12m
- Root size: 25
- Sub multiplier: 2.0
- Sub size: 50
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 23.79
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Request error for account c1a62d4b-6aaa-47d6-a878-a1bf2176caae:

| Metric | Value |
| --- | --- |
| Runs | 992 |
| Root avg wall (ms) | 579.77 |
| Root min/max wall (ms) | 173.65 / 2750.08 |
| Root p50 wall (ms) | 457.83 |
| Root p90 wall (ms) | 1166.46 |
| Root p99 wall (ms) | 1790.89 |
| Root avg TTFB (ms) | 562.00 |
| Root p50 TTFB (ms) | 443.84 |
| Root p90 TTFB (ms) | 1156.52 |
| Root p99 TTFB (ms) | 1777.88 |
| Root avg read (ms) | 17.77 |
| Root p50 read (ms) | 15.96 |
| Root p90 read (ms) | 40.09 |
| Root p99 read (ms) | 82.54 |
| Root avg decode (ms) | 0.17 |
| Root p50 decode (ms) | 0.14 |
| Root p90 decode (ms) | 0.18 |
| Root p99 decode (ms) | 1.50 |
| Sub avg wall (ms) | 505.40 |
| Sub min/max wall (ms) | 175.31 / 1843.31 |
| Sub p50 wall (ms) | 291.41 |
| Sub p90 wall (ms) | 990.60 |
| Sub p99 wall (ms) | 1286.69 |
| Sub avg TTFB (ms) | 447.40 |
| Sub p50 TTFB (ms) | 247.47 |
| Sub p90 TTFB (ms) | 902.53 |
| Sub p99 TTFB (ms) | 1226.12 |
| Sub avg read (ms) | 58.00 |
| Sub p50 read (ms) | 51.84 |
| Sub p90 read (ms) | 94.98 |
| Sub p99 read (ms) | 164.76 |
| Sub avg decode (ms) | 0.38 |
| Sub p50 decode (ms) | 0.30 |
| Sub p90 decode (ms) | 0.41 |
| Sub p99 decode (ms) | 2.38 |
| Total avg wall (ms) | 1085.75 |
| Total min/max (ms) | 362.59 / 3618.47 |
| Total p50 wall (ms) | 744.17 |
| Total p90 wall (ms) | 2135.94 |
| Total p99 wall (ms) | 2814.21 |
| Root avg ES took (ms) | 179.26 |
| Sub avg ES took (ms) | 52.84 |


## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

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
              "gte": "2025-04-07T14:21:58Z",
              "lte": "2026-04-02T14:21:58Z"
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
          "range": {
            "transaction_date": {
              "gte": "2025-04-07T14:21:58Z",
              "lte": "2026-04-02T14:21:58Z"
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
