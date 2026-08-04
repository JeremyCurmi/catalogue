---
name: worktree
description: Work inside a git worktree kept under <repo-root>/.worktrees/ — resume the matching one if it exists, otherwise create a fresh one branched off the latest main. Use for "/worktree", "start working on X", "continue working on X", "spin up a worktree", "work on this in a worktree", or any request to work on something without dirtying the current checkout.
---

# Worktree

Put the session in a git worktree under `<repo-root>/.worktrees/`. Resume before you create.

## 1. Resolve the repo root

```bash
git rev-parse --path-format=absolute --git-common-dir
```

Strip the trailing `/.git` — that is `ROOT`. This works from the main checkout *and* from inside an existing worktree, so the worktrees always land in one place.

Not a git repo → stop and say so.

## 2. Look for an existing worktree

```bash
git -C "$ROOT" worktree list --porcelain
```

Match the user's intent against the worktree paths and branch names. Then:

- **One clear match** → go to step 4 and enter it. Report how far behind `origin/<default>` its branch is (`git rev-list --count <branch>..origin/<default>`), and any uncommitted files. Do **not** rebase or pull unless asked.
- **Several plausible matches** → list them with branch + last commit date and ask which one.
- **No match** → step 3.

## 3. Create one

Name the branch from the task (`feat/…`, `fix/…`, whatever the repo's convention is — check recent branch names). The directory is the branch name with `/` replaced by `-`.

Base it on the latest main, always, unless the user says otherwise:

```bash
DEFAULT=$(git -C "$ROOT" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)
git -C "$ROOT" fetch origin
git -C "$ROOT" worktree add -b "$BRANCH" "$ROOT/.worktrees/$DIR" "$DEFAULT"
```

- No `origin` remote → base on the local default branch and say plainly that nothing was pulled.
- Branch already exists but has no worktree → drop `-b` and pass the branch as the base ref.
- Adding an existing branch that is checked out elsewhere fails; use `--force` only if the user asks.

Keep the worktrees out of git status without touching a tracked file — append `.worktrees/` to `$ROOT/.git/info/exclude` if it is not already there.

## 4. Enter it

Call `EnterWorktree` with `path` set to the absolute worktree path. Never with `name` — that would create one under `.claude/worktrees/` instead.

Then say which branch and path the session is on, in one line.

## Leaving

`ExitWorktree` will not delete a worktree entered by path; use `action: "keep"` to return to the original directory. To actually remove one: `git -C "$ROOT" worktree remove .worktrees/<dir>`.
