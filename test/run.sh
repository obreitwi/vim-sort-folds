#!/bin/bash

set -euo pipefail

if (( $# < 1 )); then
    echo "Usage: $0 <testcase_directory>..." >&2
    exit 1
fi

while (( $# > 0 )); do
    dir_testcase="${1}"
    shift

    version_info="[$EDITOR/$(python --version)]"

    echo "${version_info} Testing ${dir_testcase}.." >&2

    file_cmd="${dir_testcase}/commands.vim"
    file_in="${dir_testcase}/input.txt"
    file_out="${dir_testcase}/output.txt"
    file_exp="${dir_testcase}/expected.txt"

    cp -v "${file_in}" "${file_out}"

    true > messages.log

    ${EDITOR} -V0messages.log -s "${file_cmd}" "${file_out}" 2>&1

    if diff "${file_out}" "${file_exp}"; then
        echo "${version_info} SUCCESS"  >&2
    else
        echo "${version_info} FAILED" >&2
        cat messages.log >&2
        exit 1
    fi
done
