#!/usr/bin/env bash

kubectl apply -f ../prod/battleforcastile_match_recorder_secrets.yml
kubectl create secret generic cloudsql-instance-credentials --from-file=credentials.json=../prod/key.json

kubectl scale deployment battleforcastile-match-recorder-deployment --replicas=0
sleep 15;
kubectl scale deployment battleforcastile-match-recorder-deployment --replicas=1
