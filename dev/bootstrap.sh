#!/usr/bin/env bash

set -e

install_hooks() {
    rm -rf ./.git/hooks
    cp -r ./dev/hooks ./.git/hooks
}

log() {
    echo "$1"
}

if [ ! -d ".git" ]; then {
    log "Aborting because you are not at the root of a git repository"
    exit 1
}
fi

log "Configuring git hooks"
install_hooks
