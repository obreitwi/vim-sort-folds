#!/bin/bash

set -Eeuo pipefail

FOLDER_SOURCE="$(dirname "$(readlink -m "${BASH_SOURCE[0]}")")"
FOLDER_PLUGIN="$(readlink -m "${FOLDER_SOURCE}/..")"

symlink() {
    ln -sfv "$@"
}

append_package_load()
{
    cat <<EOF >>"${1}"
set runtimepath^=${FOLDER_PLUGIN} runtimepath+=${FOLDER_PLUGIN}/after
EOF
}

echo "Setting up for $(${EDITOR} --version)" >&2

# check if nvim exists
if [ "${EDITOR}" = "nvim" ]; then
    mkdir -p "${HOME}/.config/nvim"
    append_package_load "${HOME}/.config/nvim/init.vim"
else
    mkdir -p "${HOME}/.vim"
    append_package_load "${HOME}/.vim/vimrc"
fi

