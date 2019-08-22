#!/usr/bin/env bash

kubectl delete deployments --all
kubectl delete services --all
kubectl delete secrets --all

# We don't delete it because it takes long time to configure
#kubectl delete ingresses --all
