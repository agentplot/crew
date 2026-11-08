## MODIFIED Requirements

### Requirement: The design agent's brief names each kept repository's checkout and folder as its host keeps them
The design agent's brief SHALL name its default blueprints repository's checkout and folder, and each kit's checkout with its folder, where its worktrees are cut. Each SHALL be the teams file's `checkout` and `dir` where it names the repository on the host crew runs on, and otherwise `<session dir>/<name>/main` and `<session dir>/<name>`. It SHALL say a checkout is moved only by its host: the fleet's timer, or the runner on a runner host. It SHALL mark each checkout that is the runner's clone and name the repositories the runner keeps there, saying that no `git fetch` or `git pull` is run there, that GitHub's branches are read there at `origin/<branch>` as the runner last fetched them, and that a read that needs one fresher waits for the runner's next fetch; where none is the runner's clone it SHALL say so. Where its blueprints checkout is the runner's view, it SHALL have the agent commit on a branch of its own in a worktree under the folder's `places/`, cut from `origin/main` as the runner last fetched it, in place of pulling and committing on `main`.

#### Scenario: The design brief on a runner host
- **WHEN** deneb's teams file names `agentplot/blueprints` and `agentplot/crew` with their containers and views, and agentplot's design agent's brief is built on deneb
- **THEN** it names the blueprints view as its checkout with the blueprints container as its folder, and crew's view as crew's checkout with crew's container as its folder, marked as the runner's clone

#### Scenario: The design brief fetches nothing in the runner's clone
- **WHEN** the design agent's brief is built on a host whose teams file names its blueprints repository and a kit
- **THEN** it names both as kept by the runner, says no `git fetch` or `git pull` is run there, has blueprints work committed on a branch in a worktree cut from `origin/main`, and holds no `git pull --rebase`

#### Scenario: The design brief where the file names none
- **WHEN** the teams file gives no `repositories`, and deneb's agentplot session at `/Users/chuck/Code/github_agentplot` keeps `agentplot/crew`
- **THEN** the design brief names `/Users/chuck/Code/github_agentplot/crew/main` as crew's checkout, in the folder `/Users/chuck/Code/github_agentplot/crew`, says no checkout there is a runner's clone, and pulls its blueprints before committing as before

### Requirement: The operator's brief names swancloud's checkout and folder as its host keeps them
The operator's brief SHALL name swancloud's checkout and folder as its main level's host keeps `afterthought/swancloud`, found as the design agent's are, for its worktree under `<folder>/places/`, cut from `origin/main`, and that worktree's removal. It SHALL fetch swancloud's checkout first, but where that checkout is the runner's clone, where it SHALL fetch nothing and cut from `origin/main` as the runner last fetched it. Where that host keeps none, the brief SHALL say so in words, never leaving a token blank.

#### Scenario: The operator's swancloud on a runner host
- **WHEN** deneb's teams file names `afterthought/swancloud` with its container and its view, and afterthought's operator's brief is built on deneb
- **THEN** it cuts its `crew-teams-<label>` worktree from swancloud's view under the container's `places/` with no fetch, from `origin/main` as the runner last fetched it, naming no `~/Code/github_afterthought/swancloud` and no `fetch -q origin`

#### Scenario: The operator's swancloud on a Mac with no runner's clone
- **WHEN** mac-studio's spaces keep `afterthought/swancloud` and its teams file names none
- **THEN** the operator's brief fetches in swancloud's checkout first and cuts its worktree from `origin/main`, as before

#### Scenario: A box's operator
- **WHEN** wldn's main level runs on the box, whose spaces and file keep no `afterthought/swancloud`
- **THEN** the operator's brief builds with every token filled, saying the host keeps no checkout of swancloud, and sends a change to the teams to a partition whose main level keeps one
