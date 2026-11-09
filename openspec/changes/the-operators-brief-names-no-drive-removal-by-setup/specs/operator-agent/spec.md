## MODIFIED Requirements

### Requirement: The operator's brief says who changes the drives on its host
The operator's brief SHALL say that where its host's `~/.config/crew/teams.json` is a file and not a link into the Nix store, as Boomdrive's setup leaves a person's Mac, a drive is added or changed through Boomdrive's setup on the user's word, which gives crew the drive's entry with `crew drive set`, and that the operator edits no teams file by hand. It SHALL name no removal of a drive through Boomdrive's setup, which neither setup nor `crew drive set` provides. Its steps through swancloud's `lib/crew-teams.nix` SHALL be said for a teams file that is a link into the Nix store.

#### Scenario: The operator's brief
- **WHEN** a drive's operator brief is built
- **THEN** its *Changing the drives* says a drive on a host whose teams file is no link into the Nix store is added or changed through Boomdrive's setup, which writes crew's entry with `crew drive set`, never by a hand edit, and says the swancloud steps for a teams file that is such a link

#### Scenario: No removal through setup
- **WHEN** a drive's operator brief is built
- **THEN** its *Changing the drives* names no drive removed through Boomdrive's setup
