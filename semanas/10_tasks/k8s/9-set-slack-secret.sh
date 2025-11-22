#!/usr/bin/bash
./kubectl create secret generic slack-webhook \
  --from-literal=SLACK_WEBHOOK_URL="$@"

