#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   export ES_API_KEY="..."
#   export ES_HOST="https://your-es-host:9200"
#   ./collect-es-during-load.sh
#
# Or:
#   ES_API_KEY="..." ./collect-es-during-load.sh https://your-es-host:9200
#
# Optional env vars:
#   INTERVAL=1
#   OUTDIR=./es_capture_$(date +%Y%m%d_%H%M%S)

INTERVAL="${INTERVAL:-1}"
OUTDIR="${OUTDIR:-./es_capture_$(date +%Y%m%d_%H%M%S)}"
ES_HOST="https://elastic-monos-tx-client.lb.prod-coretech-baas.cnco.tucows.systems"

if [[ -z "${ES_API_KEY:-}" ]]; then
  echo "ERROR: ES_API_KEY is not set" >&2
  exit 1
fi

if [[ -z "${ES_HOST}" ]]; then
  echo "ERROR: ES_HOST is not set and no host argument was provided" >&2
  exit 1
fi

# Trim trailing slash if present
ES_HOST="${ES_HOST%/}"

mkdir -p "${OUTDIR}"/{thread_pool,node_stats,cluster_health,http_probe,logs}

AUTH_HEADER="Authorization: ApiKey ${ES_API_KEY}"
COMMON_CURL_OPTS=(
  -sS
  --connect-timeout 5
  --max-time 30
  -H "${AUTH_HEADER}"
)

THREAD_POOL_PATH="/_cat/thread_pool/search,search_coordination,search_worker?v&h=node_name,name,active,queue,rejected,completed"
NODE_STATS_PATH="/_nodes/stats/indices,thread_pool,http,transport,breaker,jvm,os,process"
CLUSTER_HEALTH_PATH="/_cluster/health"
HTTP_PROBE_PATH="/"

log() {
  printf '%s %s\n' "$(date '+%F %T')" "$*" | tee -a "${OUTDIR}/logs/collector.log" >&2
}

check_connectivity() {
  log "Checking connectivity to ${ES_HOST}"
  curl "${COMMON_CURL_OPTS[@]}" "${ES_HOST}${CLUSTER_HEALTH_PATH}" > /dev/null
  log "Connectivity check passed"
}

collect_thread_pool() {
  while true; do
    ts="$(date +%s)"
    outfile="${OUTDIR}/thread_pool/thread_pool_${ts}.txt"
    if ! curl "${COMMON_CURL_OPTS[@]}" "${ES_HOST}${THREAD_POOL_PATH}" > "${outfile}.tmp" 2>>"${OUTDIR}/logs/thread_pool.err"; then
      log "thread_pool collection failed at ${ts}"
      rm -f "${outfile}.tmp"
    else
      mv "${outfile}.tmp" "${outfile}"
    fi
    sleep "${INTERVAL}"
  done
}

collect_node_stats() {
  while true; do
    ts="$(date +%s)"
    outfile="${OUTDIR}/node_stats/node_stats_${ts}.json"
    if ! curl "${COMMON_CURL_OPTS[@]}" "${ES_HOST}${NODE_STATS_PATH}" > "${outfile}.tmp" 2>>"${OUTDIR}/logs/node_stats.err"; then
      log "node_stats collection failed at ${ts}"
      rm -f "${outfile}.tmp"
    else
      mv "${outfile}.tmp" "${outfile}"
    fi
    sleep "${INTERVAL}"
  done
}

collect_cluster_health() {
  while true; do
    ts="$(date +%s)"
    outfile="${OUTDIR}/cluster_health/cluster_health_${ts}.json"
    if ! curl "${COMMON_CURL_OPTS[@]}" "${ES_HOST}${CLUSTER_HEALTH_PATH}" > "${outfile}.tmp" 2>>"${OUTDIR}/logs/cluster_health.err"; then
      log "cluster_health collection failed at ${ts}"
      rm -f "${outfile}.tmp"
    else
      mv "${outfile}.tmp" "${outfile}"
    fi
    sleep "${INTERVAL}"
  done
}

collect_http_probe() {
  while true; do
    ts="$(date +%s)"
    curl \
      -sS \
      -o /dev/null \
      --connect-timeout 5 \
      --max-time 30 \
      -H "${AUTH_HEADER}" \
      -w "${ts} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total} bytes=%{size_download} code=%{http_code}\n" \
      "${ES_HOST}${HTTP_PROBE_PATH}" >> "${OUTDIR}/http_probe/http_probe.log" \
      2>>"${OUTDIR}/logs/http_probe.err" || log "http_probe failed at ${ts}"
    sleep "${INTERVAL}"
  done
}

PIDS=()

cleanup() {
  log "Stopping collectors"
  for pid in "${PIDS[@]:-}"; do
    kill "${pid}" 2>/dev/null || true
  done
  wait || true
  log "Collectors stopped"
  log "Output saved in ${OUTDIR}"
}

trap cleanup EXIT INT TERM

check_connectivity

log "Starting collectors"
collect_thread_pool &
PIDS+=("$!")

collect_node_stats &
PIDS+=("$!")

collect_cluster_health &
PIDS+=("$!")

collect_http_probe &
PIDS+=("$!")

log "Collectors running"
log "Start your load test now"
log "Press Ctrl-C when the load test and cooldown are complete"

wait
