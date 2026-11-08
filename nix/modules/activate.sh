#!/bin/sh
# The modules' activation, run as the user who runs crew (record 0058,
# flake.2; Boomdrive's nix/modules/activate.sh):
#
#   activate.sh link <file> <host>
#
# links ~/.config/crew/teams.json, crew's teams file, to the module's
# file. A link there is replaced. A file or folder there that is no link
# is moved once, to teams.json.before-nix, and both paths are named. Where
# teams.json.before-nix is there already, it changes neither, names both
# and fails. It says a line only where it moved or linked something.
#
# Then it reads this host's name as `hostname -s` gives it, `uname -n` up
# to its first dot, since NixOS's user activation has coreutils on its
# PATH and no hostname; where that is not <host>, services.crew.host, it
# says one line naming both, and never fails for it: the file is right
# either way, and crew reads its host from hostname -s.
set -eu

usage() {
  echo "usage: activate.sh link <file> <host>" >&2
  exit 2
}

link() {
  file=$1
  host=$2
  folder=$HOME/.config/crew
  target=$folder/teams.json
  aside=$target.before-nix

  if [ ! -L "$target" ] || [ "$(readlink "$target")" != "$file" ]; then
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      if [ -e "$aside" ] || [ -L "$aside" ]; then
        echo "crew: $target is no link and $aside is there already: left both, linked nothing; move one aside to link $file" >&2
        exit 1
      fi
      mv "$target" "$aside"
      echo "crew: moved $target to $aside"
    fi
    mkdir -p "$folder"
    ln -sfn "$file" "$target"
    echo "crew: linked $target to $file"
  fi

  name=$(uname -n)
  name=${name%%.*}
  if [ "$name" != "$host" ]; then
    echo "crew: this host is $name, not services.crew.host's $host: crew reads its host from hostname -s" >&2
  fi
}

case ${1:-} in
link)
  [ $# -eq 3 ] || usage
  link "$2" "$3"
  ;;
*) usage ;;
esac
