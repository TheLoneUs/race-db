# race-db

Repository with race data in SQLite DB.

## Usage

To update json, make changes to the sqlite db contents and push to `main`.
Runs a GitHub action on push that generates all of the json files and commits them automatically to the repo.
This means after pushes that generate new JSON, you will need to pull.

## Utilized

Utilized by the `snippets/race-results.liquid` template in Shopify.
