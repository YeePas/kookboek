# Foodnotes CMS auth worker

Dit is de Cloudflare Worker voor Decap CMS GitHub OAuth.

## Welke optie kies je in Cloudflare?

Kies:

- `Worker`
- daarna de eenvoudige `Hello World`-achtige code-optie

Kies niet:

- `Static files`

Deze worker is namelijk geen statische site, maar een klein stukje servercode voor OAuth.

## URLs voor jouw setup

- huidige site op Cloudflare Pages: `https://kookboek.joep-willemsen.workers.dev`
- huidige GitHub repo: `https://github.com/yeepas/kookboek`
- tijdelijke auth worker URL: `https://cms-auth.joep-willemsen.workers.dev`
- latere gewenste domeinen:
  - site: `https://foodnotes.nl`
  - auth worker: `https://cms-auth.foodnotes.nl`

## Wat staat al klaar in de repo

De CMS-config in `src/admin/config.yml` gebruikt nu:

```yml
backend:
  name: github
  repo: yeepas/kookboek
  branch: main
  base_url: https://cms-auth.joep-willemsen.workers.dev
  auth_endpoint: /auth
```

## Snelle route in de Cloudflare UI

1. Ga naar `Workers & Pages`.
2. Kies `Create`.
3. Kies `Worker`.
4. Geef hem de naam `cms-auth`.
5. Open de editor.
6. Vervang de standaardcode door de inhoud van `src/index.js`.
7. Deploy de worker.

## Secrets toevoegen

Voeg in de Worker settings deze secrets toe:

- `GITHUB_OAUTH_ID`
- `GITHUB_OAUTH_SECRET`

Optioneel:

- `GITHUB_SCOPE`

Voor deze publieke repo is de standaard meestal goed:

`public_repo read:user`

## GitHub OAuth app instellen

Maak in GitHub een OAuth App met:

- Homepage URL: `https://cms-auth.joep-willemsen.workers.dev`
- Authorization callback URL: `https://cms-auth.joep-willemsen.workers.dev/callback`

## Test

1. Open `https://cms-auth.joep-willemsen.workers.dev`
2. Als je tekst ziet als `Hello from the Foodnotes CMS auth worker.`, dan draait hij.
3. Open daarna je CMS op `/admin`.
4. Log in met GitHub.

## Later naar foodnotes.nl

Als `foodnotes.nl` op Cloudflare staat, maak dan een custom domain voor de worker:

- `cms-auth.foodnotes.nl`

Daarna wijzig je in `src/admin/config.yml` alleen:

```yml
base_url: https://cms-auth.foodnotes.nl
```
