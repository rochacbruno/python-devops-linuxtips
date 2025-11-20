#!/usr/bin/bash
name="$@"
./kubectl create job --from=cronjob/image-scanner-cronjob "manual-scan-$name"
sleep 5
./kubectl logs "job/manual-scan-$name"
