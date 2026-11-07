#!/bin/sh
# The activation's cases (record 0058, flake.2), which nix/check.sh test
# runs after the evaluated ones: each runs nix/modules/activate.sh by sh in
# a scratch folder of its own, with a scratch HOME, the module's file in a
# store of its own, and a stub of uname first on PATH, whose `uname -n` is
# the case's `name`, host-a unless the case says another. It prints each
# failure as one line, nix: activate: <case>: <what>, and nothing where
# every case holds.
set -eu

activate=$(cd "$(dirname "$0")/../modules" && pwd)/activate.sh
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
cases=0

# A case's folder: its home, the module's file and the stub.
fresh() {
  cases=$((cases + 1))
  dir=$scratch/$cases
  home=$dir/home
  file=$dir/store/crew-teams.json
  target=$home/.config/crew/teams.json
  aside=$target.before-nix
  mkdir -p "$home" "$dir/store" "$dir/bin"
  printf '%s' '{"partitions":[],"version":5}' >"$file"
  echo host-a >"$dir/name"
  cat >"$dir/bin/uname" <<STUB
#!/bin/sh
case "\$*" in -n) cat "$dir/name" ;; *) exit 1 ;; esac
STUB
  chmod +x "$dir/bin/uname"
}

# activate.sh with `$@` in the case's folder: its status, output and
# error.
run() {
  status=0
  HOME=$home PATH=$dir/bin:$PATH sh "$activate" "$@" >"$dir/out" 2>"$dir/err" || status=$?
  out=$(cat "$dir/out")
  err=$(cat "$dir/err")
}

# A failure of the case `$1`, saying `$2`, where the test after them fails.
expect() {
  named=$1
  what=$2
  shift 2
  if ! "$@"; then
    echo "nix: activate: $named: $what"
  fi
}

linked() {
  [ -L "$target" ] && [ "$(readlink "$target")" = "$file" ]
}
holds() {
  [ "$(cat "$1" 2>/dev/null)" = "$2" ]
}
missing() {
  [ ! -e "$1" ] && [ ! -L "$1" ]
}
# `$1` names `$2`, then `$3`.
names() {
  case $1 in *"$2"*"$3"*) ;; *) return 1 ;; esac
}

named="Nothing there"
fresh
run link "$file" host-a
expect "$named" "link exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file" linked
expect "$named" "link says \"$out\", not that it linked $target" \
  [ "$out" = "crew: linked $target to $file" ]
expect "$named" "link says \"$err\" on its error" [ -z "$err" ]
expect "$named" "link moved something aside" missing "$aside"

named="A link there"
fresh
mkdir -p "$(dirname "$target")"
ln -s "$dir/store/another.json" "$target"
run link "$file" host-a
expect "$named" "link exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file" linked
expect "$named" "link says \"$out\", not that it linked $target" \
  [ "$out" = "crew: linked $target to $file" ]
expect "$named" "link moved the other link aside" missing "$aside"

named="Already linked"
fresh
mkdir -p "$(dirname "$target")"
ln -s "$file" "$target"
run link "$file" host-a
expect "$named" "link exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file" linked
expect "$named" "link says \"$out$err\"" [ -z "$out$err" ]
expect "$named" "link moved something aside" missing "$aside"

named="A file there"
fresh
mkdir -p "$(dirname "$target")"
echo '{"version":4}' >"$target"
run link "$file" host-a
expect "$named" "link exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file" linked
expect "$named" "$aside does not hold the file that was there" holds "$aside" '{"version":4}'
expect "$named" "link says \"$out\", not both paths" \
  [ "$out" = "crew: moved $target to $aside
crew: linked $target to $file" ]

fresh
mkdir -p "$target"
echo kept >"$target/inside"
run link "$file" host-a
expect "$named" "link of a folder exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file, where a folder was" linked
expect "$named" "$aside does not hold the folder that was there" holds "$aside/inside" kept

named="A file there and one aside already"
fresh
mkdir -p "$(dirname "$target")"
echo '{"version":4}' >"$target"
echo '{"version":3}' >"$aside"
run link "$file" host-a
expect "$named" "link exits $status, not 1" [ "$status" -eq 1 ]
expect "$named" "link changed $target" holds "$target" '{"version":4}'
expect "$named" "link changed $aside" holds "$aside" '{"version":3}'
expect "$named" "link's refusal \"$err\" names not both paths" names "$err" "$target" "$aside"
expect "$named" "link says \"$out\"" [ -z "$out" ]

named="A host whose name is not services.crew.host"
fresh
echo host-b >"$dir/name"
run link "$file" host-a
expect "$named" "link exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "$target is no link to $file" linked
expect "$named" "link says \"$err\", not one line naming host-a and host-b" \
  [ "$err" = "crew: this host is host-b, not services.crew.host's host-a: crew reads its host from hostname -s" ]

fresh
echo host-a.local >"$dir/name"
run link "$file" host-a
expect "$named" "link with uname -n host-a.local exits $status: $err" [ "$status" -eq 0 ]
expect "$named" "link with uname -n host-a.local says \"$err\"" [ -z "$err" ]

named="link's usage"
fresh
run link "$file"
expect "$named" "link with no host exits $status, not 2" [ "$status" -eq 2 ]
expect "$named" "link with no host made $target" missing "$target"
