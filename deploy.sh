#!/usr/bin/env bash
git add -f .secrets/
eb deploy --profile EB --staged
git reset HEAD .secrets/
