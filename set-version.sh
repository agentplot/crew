#!/bin/sh
# shellcheck disable=SC2016 # awk programs name their own $fields.
# Writes a release's version into every file of crew's tree that carries
# crew's version: its release file, plugin/release.json, which crew reads
# where it runs with no git and crew's flake versions its package by; and
# crew's manifest, plugin/.claude-plugin/plugin.json, which Claude Code
# reads. main gives 0.0.0 in each. The release job runs this on the commit
# it releases, and its tag names the release commit it makes of what this
# wrote (.github/workflows/release.yml); tests/t-release.sh holds main's
# files at 0.0.0 and runs this on a scratch copy of them.
#
#   sh set-version.sh <major.minor.patch> [<root>]
set -eu

[ $# -ge 1 ] && [ $# -le 2 ] || {
  echo "usage: set-version.sh <major.minor.patch> [<root>]" >&2
  exit 2
}
version=$1
root=${2:-$(dirname "$0")}
printf '%s\n' "$version" | grep -Eqx '[0-9]+\.[0-9]+\.[0-9]+' || {
  echo "set-version: $version is not a version major.minor.patch" >&2
  exit 2
}

# The file $1 under the root, rewritten by the awk program $2 with the
# version as `v`; the program counts what it wrote in `written`, and
# a file it wrote nothing in is refused.
put() {
  file=$root/$1
  awk -v v="$version" "$2"'
    END { exit (written ? 0 : 1) }
  ' "$file" >"$file.set-version" || {
    rm -f "$file.set-version"
    echo "set-version: $1 gives no version where crew's is" >&2
    exit 1
  }
  mv "$file.set-version" "$file"
}

# The release file's one line, {"version": "<v>"}.
put plugin/release.json '
  /"version": "[^"]*"/ && !written {
    sub(/"version": "[^"]*"/, "\"version\": \"" v "\"")
    written++
  }
  { print }
'

put plugin/.claude-plugin/plugin.json '
  /^ *"version": "[^"]*",?$/ && !written {
    sub(/"version": "[^"]*"/, "\"version\": \"" v "\"")
    written++
  }
  { print }
'
