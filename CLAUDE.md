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

## Local testing

`/plugin marketplace add /Users/jeremy/repos/catalogue`, then `/plugin install dev@catalogue`.
