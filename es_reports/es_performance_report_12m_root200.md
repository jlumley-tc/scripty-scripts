# ES Performance Report

- Generated: 2026-04-02T14:24:50Z
- Base URL: https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems
- Index: datastream-search-account-history-financial-transaction-0
- Date range: 2025-04-07T14:24:05Z .. 2026-04-02T14:24:05Z
- Range: 12m
- Root size: 200
- Sub multiplier: 2.0
- Sub size: 400
- Iterations: 10
- Target IPS: 80.0
- Achieved IPS: 21.80
- Max concurrency: 1000
- Request cache: false
- Routing: disabled

## Results Summary

Error: Query failed for account ca6727af-1afb-48b7-b68e-dcd92742ab6b: HTTP 504 | <html><body><h1>504 Gateway Time-out</h1> The server didn't respond in time. </body></html>

| Metric | Value |
| --- | --- |
| Runs | 990 |
| Root avg wall (ms) | 1097.70 |
| Root min/max wall (ms) | 356.65 / 3806.19 |
| Root p50 wall (ms) | 554.06 |
| Root p90 wall (ms) | 3000.12 |
| Root p99 wall (ms) | 3550.10 |
| Root avg TTFB (ms) | 796.04 |
| Root p50 TTFB (ms) | 318.22 |
| Root p90 TTFB (ms) | 2480.44 |
| Root p99 TTFB (ms) | 3161.06 |
| Root avg read (ms) | 301.66 |
| Root p50 read (ms) | 238.93 |
| Root p90 read (ms) | 507.72 |
| Root p99 read (ms) | 925.27 |
| Root avg decode (ms) | 1.02 |
| Root p50 decode (ms) | 0.88 |
| Root p90 decode (ms) | 1.42 |
| Root p99 decode (ms) | 2.15 |
| Sub avg wall (ms) | 1438.04 |
| Sub min/max wall (ms) | 543.17 / 4133.17 |
| Sub p50 wall (ms) | 842.09 |
| Sub p90 wall (ms) | 3352.04 |
| Sub p99 wall (ms) | 3865.49 |
| Sub avg TTFB (ms) | 923.92 |
| Sub p50 TTFB (ms) | 385.69 |
| Sub p90 TTFB (ms) | 2567.64 |
| Sub p99 TTFB (ms) | 3322.89 |
| Sub avg read (ms) | 514.12 |
| Sub p50 read (ms) | 447.67 |
| Sub p90 read (ms) | 778.83 |
| Sub p99 read (ms) | 1193.38 |
| Sub avg decode (ms) | 2.34 |
| Sub p50 decode (ms) | 2.13 |
| Sub p90 decode (ms) | 2.68 |
| Sub p99 decode (ms) | 10.44 |
| Total avg wall (ms) | 2539.26 |
| Total min/max (ms) | 929.95 / 6584.09 |
| Total p50 wall (ms) | 1386.13 |
| Total p90 wall (ms) | 5804.72 |
| Total p99 wall (ms) | 6280.91 |
| Root avg ES took (ms) | 31.22 |
| Sub avg ES took (ms) | 27.46 |

## Sample Queries

Account UUID and transaction IDs are redacted.
Routing: disabled

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
              "gte": "2025-04-07T14:24:05Z",
              "lte": "2026-04-02T14:24:05Z"
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
          "range": {
            "transaction_date": {
              "gte": "2025-04-07T14:24:05Z",
              "lte": "2026-04-02T14:24:05Z"
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
