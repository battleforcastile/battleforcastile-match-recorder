# Battle For Castile: Match Recorder

## 1. Installation and set up

This guide assumes that there's a K8s cluster and Postgres SQL DB set up in Google Cloud.
Google cloud only allows access to its DB using a proxy container, so we need to set up the
proxy-user first

> Make sure to active the following API first: https://console.developers.google.com/apis/api/sqladmin.googleapis.com/overview?project=678954142891

#### 1.1 Create proxy-user (for SQL instance proxy)
```
gcloud iam service-accounts create proxy-user --display-name "proxy-user"
```

#### 1.2 Get `serviceAccount` of newly created proxy-user.
```
gcloud iam service-accounts list
```

#### 1.3 Add IAM for newly created proxy-user
```
gcloud projects add-iam-policy-binding <project> --member \
serviceAccount:<service_account_email> --role roles/cloudsql.client
```

#### 1.4 Create credentials key
```
gcloud iam service-accounts keys create key.json --iam-account <service_account_email>
```

#### 1.5 Convert credentials key to base64 and write down the value.
```
openssl base64 < key.json | tr -d '\n'
```

Now we need to set up `Helm`, so we can easily deploy releases in our cluster.

#### 1.6 Set up Tiller in our cluster
```
helm init --history-max 200

kubectl create serviceaccount --namespace kube-system tiller

kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller

kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

#### 1.7 Go to `/helm/batteforcastile_match_recorder/` folder and copy the content from `templates_examples` to `templates`
```
cp helm/batteforcastile_match_recorder/templates_examples/* helm/batteforcastile_match_recorder/templates/*
```

#### 1.8 Uncomment the content from `cloudsql_instance_credentials.yml` (from `templates`) and replace:
 - The value of `credentials.json` by the `base64` value we wrote down previously (`key.json`)

#### 1.9 Uncomment the content from `battleforcastile_match_recorder_secrets.yml` (from `templates`) and replace:
 - The value of `secret_key` by the `base64` value of the secret key of your Flask App (can be random)
 - The value of `sqlalchemy_database_uri` by the `base64` value of the DB URI from Google Cloud (It will be something like `postgresql+pg8000://<db_user>:<db_password>@127.0.0.1:5432/<database_name>`)

#### 1.10 Go to `/helm/batteforcastile_match_recorder/values.yml` and replace the `instance_connection_name` by the one you get from Google cloud (It will be something like `<project>:<zone>:<sql_instance_name>`)

#### 1.11 Run `helm install helm/batteforcastile_match_recorder` and in a few minutes it should be deployed! :)
