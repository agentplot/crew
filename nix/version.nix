# The package's version, from crew's release file (crew-flake,
# crew-release): a release's x.y.z, which the release commit a tag names
# writes there (set-version.sh), as it is; main's 0.0.0 as nixpkgs' form
# for an untagged commit, 0-unstable-YYYY-MM-DD, from `date`, the tree's
# last change as YYYYMMDD…; and any other version fails evaluation,
# naming the file. `release` is the file's JSON.
{ lib }:
{ release, date }:
let
  version = release.version or null;
  released = lib.isString version && builtins.match "[0-9]+\\.[0-9]+\\.[0-9]+" version != null;
in
if version == "0.0.0" then
  "0-unstable-${lib.substring 0 4 date}-${lib.substring 4 2 date}-${lib.substring 6 2 date}"
else if released then
  version
else
  throw "crew: plugin/release.json gives version ${builtins.toJSON version}, neither x.y.z nor 0.0.0"
