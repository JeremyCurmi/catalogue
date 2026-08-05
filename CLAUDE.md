# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Jeremy's shareable AI setup — skills, agents, and commands, published as plugins.

## Layout

This repo is a plugin marketplace (`.claude-plugin/marketplace.json`) shipping two plugins:

- `plugins/dev/` — engineering
- `plugins/productivity/` — day-to-day

Each is a plugin root holding `.claude-plugin/plugin.json` plus whichever component
directories it uses:

- `skills/<skill-name>/SKILL.md` — a skill is a *directory*
- `agents/<agent>.md`, `commands/<command>.md` — a flat `.md` file each
- `hooks/hooks.json`, `.mcp.json`

Adding a plugin means a new directory under `plugins/` *and* an entry in `marketplace.json`.

## Keeping docs in sync

Any time a skill/agent/command/plugin is added, removed or renamed, update
`marketplace.json` and README.md's Skills table + Install/Layout blocks in the SAME change.

## Local testing

`/plugin marketplace add /Users/jeremy/repos/catalogue`, then `/plugin install dev@catalogue`.

Iterate with `claude --plugin-dir plugins/dev` (overrides the installed copy for that
session) and `/reload-plugins` after each edit.

Installs are copies under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, not
live references — for an installed copy, push, then `/plugin marketplace update catalogue`
and `/plugin update <plugin>@catalogue`.

`plugin.json` deliberately omits `version`: setting it pins the plugin and updates are
skipped until the string changes. Without it every commit is a new version. Don't add it back.
