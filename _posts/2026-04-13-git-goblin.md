---
layout: post
title: "📦 git-goblin: 195+ Shell Shortcuts and a Fuzzy-Find TUI in Pure Bash"
date: 2026-04-13
---

[View on GitHub](https://github.com/juleshenry/git-goblin)

![ggob](https://github.com/juleshenry/git-goblin/blob/main/ggob.jpeg?raw=1)

git-goblin is a shell productivity toolkit that replaces verbose CLI commands with short, mnemonic shortcuts. 195+ aliases and functions covering Git, Docker, Kubernetes, AWS, GCP, Terraform, Helm, Ansible, and general shell utilities. One-command setup. Source it into your bash or zsh, and your terminal becomes a different animal.

The project is on [GitHub](https://github.com/juleshenry/git-goblin). MIT licensed.

## The Greatest Hits

Before we get to the interesting stuff, here is the practical pitch. These are commands I use every single day:

```bash
gg "fix the auth bug"     # git add -A && git commit -m "..." && git push
gs                        # git status
gd                        # git diff
gb                        # git branch
gco feature               # git checkout feature
gpr                       # create GitHub PR via gh cli
gsquash 3                 # squash last 3 commits
gwip                      # commit everything as WIP
gunwip                    # undo the last WIP commit
presto                    # nuclear option: wipe git history (with confirmation)
```

Docker:

```bash
dps                       # docker ps
dcu                       # docker compose up -d
dcd                       # docker compose down
dex container bash        # docker exec -it container bash
drmi                      # docker rmi (remove image)
```

Kubernetes:

```bash
kgp                       # kubectl get pods
kgs                       # kubectl get services
kl pod-name               # kubectl logs pod-name
kex pod-name bash          # kubectl exec -it pod-name -- bash
ksc context                # kubectl config use-context
```

AWS, GCP, Terraform, Helm, Ansible -- all have similar shortcut families. The full list is 195+ commands. You do not memorize them all. You memorize the ones you use, and for the rest, there is the `G` command.

## The `G` Command

This is the centerpiece of the project, and the reason it is more than a dotfiles repo.

`G` is a "hot-doc autofiller" that operates in three modes:

### Mode 1: Best-Guess

```bash
G 'git status'
```

You type any raw CLI command -- or even a vague description -- and `G` fuzzy-matches it to the closest git-goblin shortcut. It displays the documentation and copies the shortcut to your clipboard. You typed `git status`? `G` tells you the shortcut is `gs`, shows you what it does, and copies `gs` to your clipboard. Done.

The matching uses a scoring algorithm that weights exact substring matches highest, then token overlap, then edit distance. It is not perfect. It does not need to be. It needs to be faster than grepping through a 200-line alias file, and it is.

### Mode 2: Add

```bash
G -a 'mycommand' 'what it does'
```

Register your own custom shortcuts. They persist across sessions in `~/.git-goblin-custom` and are searchable through `G` just like the built-in commands. Your team has a weird deploy script? Add it. Your CI pipeline has a 40-character incantation? Add it.

### Mode 3: Interactive TUI

```bash
G
```

No arguments. `G` launches a full-screen fuzzy-find interface. Type to filter. Arrow keys to navigate. Enter to select and copy. It looks like `fzf`, but it is built entirely in pure Bash.

No dependencies. No `fzf`. No `ncurses`. No Python. The TUI uses raw terminal escape sequences (`\033[`), `read -rsn1` for character-by-character input handling, and ANSI color codes for syntax highlighting. The entire interactive mode is a bash function that manages cursor position, screen clearing, and input parsing by hand.

I built it this way because I wanted `G` to work on any machine with bash. No installation step beyond sourcing the file. No `brew install fzf` prerequisite. You `ssh` into a bare-bones production server, source git-goblin, and the TUI works.

## Setup

```bash
./setup-git-goblin
```

One command. It auto-detects your shell (bash or zsh), backs up your RC file, sources the function files, and makes scripts executable. Takes about 3 seconds.

## The Python Utilities

git-goblin also ships with a handful of Python tools:

**`kash`** -- A file-based function cache decorator. Decorate a Python function with `@kash`, and its return value gets cached to a `.kash` JSON file on disk, keyed by the arguments. Next time you call the function with the same arguments, it reads from the file instead of recomputing. It is `functools.lru_cache` but persistent across process restarts. Useful for expensive API calls during development.

```python
from kash import kash

@kash
def expensive_api_call(query):
    return requests.get(f"https://api.example.com/{query}").json()
```

**`autosave-git-recursively.py`** -- Walks a directory tree and auto-commits/pushes every git repository it finds. I run this as a cron job on my dev machine. It is an autosave for all my projects.

**`repoinspector.py`** -- Fetches all of a GitHub user's public repositories and aggregates their open issues into a single summary. Useful for triaging across many repos without clicking through GitHub's web UI.

## Why Not Just Use Oh My Zsh?

Oh My Zsh has git aliases. They are fine. git-goblin differs in three ways:

1. **Scope.** OMZ aliases are git-only. git-goblin covers Git, Docker, Kubernetes, AWS, GCP, Terraform, Helm, Ansible, and shell utilities.
2. **The `G` command.** OMZ does not have a command finder. You memorize the aliases or you grep through the source. `G` is the difference between a reference card and a searchable database.
3. **Portability.** git-goblin works on bash and zsh with no framework dependency. OMZ is a zsh framework that you install. git-goblin is a file that you source.

The built-in `gg-help` command provides a searchable, section-filterable reference table:

```bash
gg-help              # show everything
gg-help docker       # show only Docker shortcuts
gg-help kubernetes   # show only Kubernetes shortcuts
```

195 shortcuts. A fuzzy-find TUI in pure Bash. Zero dependencies. One goblin.
