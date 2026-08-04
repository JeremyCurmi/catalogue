# catalogue
AI catalogue containing plugins / skills / agents and so on.

## Layout

```
skills/<name>/SKILL.md          the skill itself — frontmatter + body, kept under ~60 lines
           references/*.md      rubrics, templates, examples — read only when the body points at them
           scripts/*            repeated work the skill shouldn't reinvent every run
```

## Skills

| Skill | Does |
|---|---|
| [`tldr`](skills/tldr) | Compresses an article, X thread or long doc into a terse visual card that reads in under two minutes |

## Using a skill

Claude Code discovers skills in `~/.claude/skills/`. Symlink so edits here take effect immediately:

```sh
ln -s "$PWD/skills/tldr" ~/.claude/skills/tldr
```

Then invoke with `/tldr`, or let the description fire it.
