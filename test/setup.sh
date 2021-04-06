#!/bin/bash

set -Eeuo pipefail

FOLDER_SOURCE="$(dirname "$(readlink -m "${BASH_SOURCE[0]}")")"
FOLDER_PLUGIN="$(readlink -m "${FOLDER_SOURCE}/..")"

symlink() {
    ln -sfv "$@"
}

append_load_package()
{
    cat <<EOF >>"${1}"
set runtimepath^=${FOLDER_PLUGIN} runtimepath+=${FOLDER_PLUGIN}/after
EOF
}

append_load_python()
{
    cat <<EOF >>"${1}"
if !has('nvim')
  set pythonthreedll="${pythonLocation}/lib/libpython3.so"
endif
EOF
}

append_print_python_version()
{
    cat <<EOF >>"${1}"
py3 import sys; print(sys.version)
EOF
}

echo "Setting up for $(${EDITOR} --version)" >&2

# check if nvim exists
if [ "${EDITOR}" = "nvim" ]; then
    config="${HOME}/.config/nvim/init.vim"
    mkdir -p "$(dirname "${config}")"
    true > "${config}"
    append_print_python_version "${config}"
    append_load_package "${config}"
else
    config="${HOME}/.vim/vimrc"
    mkdir -p "$(dirname "${config}")"
    true > "${config}"
    append_print_python_version "${config}"
    append_load_package "${config}"
fi
