#!/usr/bin/env bash
git add -f .secrets/
eb deploy --profile EB --staged & sleep 3
git reset HEAD .secrets/
