# Listy

This challenge is an abuse of a CI/CD pipeline secret leak as well as an overly broad IP restriction.

## NOTE FOR CHALLENGE DEPLOY

ADd a note saying that only GCP-related assets are in scope, no other products are in scope.

## Challenge

The user is provided with a website that has a simple list of `something TBD`. This list is updated via a call to the web server which, in turn, calls a GCP Cloud Function with certain parameters. The site exposes a `.git` directory which includes a config which points to the public Git repo hosting the codebase. Looking at the commit history exposes a GCP Credential / Testing cred for calling the function. Use this secret to call the function and get the flag.

A Secret is exposed in one execution of the pipeline and in turn the attacker must spin up a repo with the CICD platform running and invoke a "getFlag" type function to get the flag.

## Folder Structure

- `./frontend` - The web application entire repo
- `./function` - GCP Cloud Function for the user to access with compromised creds
- `./leaderboards` - Leaderboard for the challenge

## Deploy

In order to deploy this challenge you MUST first run `make deploy` in the `./frontend` directory.
