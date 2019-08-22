#!/usr/bin/env bash

kubectl apply -f ../prod/battleforcastile_match_recorder_secrets.yml
kubectl create secret generic cloudsql-instance-credentials --from-file=credentials.json=../prod/key.json

kubectl apply -f ../deployment.yml
kubectl apply -f ../service.yml
kubectl apply -f ../ingress.yml
