#!/usr/bin/env bash
set -e

cleanup() {
  echo "Stopping port-forward processes..."
  kill $(jobs -p)
}
trap cleanup EXIT

./kubectl port-forward svc/mailhog 8025:8025 &
./kubectl port-forward svc/mailhog 1025:1025 &

wait
