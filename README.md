# Skill Launcher

A one-page launcher, hosted on GitHub Pages, for running saved skills in the Claude in Chrome extension.

## What it can and cannot do

Claude in Chrome has no documented URL or deep link that opens its side panel or runs a shortcut, and Chrome does not let a web page open another extension's side panel. So no link can do the whole job by itself. This page gets it down to one click plus one keystroke: the click copies the skill command and opens any target page, the keystroke opens the side panel, then you paste and press Enter.

## Turn it on

1. Repo **Settings → Pages → Build and deployment**, source **Deploy from a branch**, pick the branch holding `index.html` and folder `/ (root)`.
2. The page lives at `https://aprevot2599-dotcom.github.io/main/`.
3. In Chrome open `chrome://extensions/shortcuts` and give Claude a shortcut (for example `Alt+Shift+C`).

## Links

| Link | Effect |
| --- | --- |
| `.../main/` | All skills |
| `.../main/?skill=start` | Highlights one skill |
| `.../main/?skill=ir-request&open=https://forms.office.com/...` | Also opens the form when you click |
| `.../main/?text=/fte-report%20fall%20term` | One-off command from the URL |

## Adding skills

Edit the `SKILLS` list near the bottom of `index.html`. `command` must match the shortcut name as you saved it in the extension.
