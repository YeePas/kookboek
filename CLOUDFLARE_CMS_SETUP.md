# Cloudflare Pages + CMS setup

Deze site kan prima op Cloudflare Pages draaien, met Decap CMS als GitHub-backed CMS.

De contentstroom wordt dan:

1. je logt in via `/admin`
2. Decap CMS gebruikt GitHub OAuth via een Cloudflare Worker
3. Decap CMS schrijft een commit naar GitHub
4. Cloudflare Pages ziet de commit op `main`
5. Cloudflare bouwt `_site` opnieuw en zet de wijziging live

## Bestanden in deze repo

- CMS-config: [src/admin/config.yml](src/admin/config.yml)
- CMS-admin pagina: [src/admin/index.html](src/admin/index.html)
- Recepten: [src/recepten](src/recepten)
- Afbeeldingen: [fotos](fotos)

## CMS-config

De CMS-config is al voorbereid op een GitHub-backend:

```yml
backend:
  name: github
  repo: YOUR_GITHUB_USERNAME/kookboek
  branch: main
  base_url: https://cms-auth.example.com
```

Vervang:

- `YOUR_GITHUB_USERNAME/kookboek` door je echte repo, bijvoorbeeld `joepwillemsen/kookboek`
- `https://cms-auth.example.com` door de URL van je Cloudflare Worker, bijvoorbeeld `https://cms-auth.jouwdomein.nl`

## Cloudflare Pages instellen

1. Log in bij Cloudflare.
2. Ga naar `Workers & Pages`.
3. Kies `Create application`.
4. Kies `Pages`.
5. Kies `Connect to Git`.
6. Selecteer deze GitHub-repo.
7. Gebruik deze buildinstellingen:
   - Production branch: `main`
   - Build command: `npm run build`
   - Build output directory: `_site`
8. Start de eerste deploy.

## GitHub OAuth app maken

1. Open GitHub.
2. Ga naar `Settings`.
3. Ga naar `Developer settings`.
4. Ga naar `OAuth Apps`.
5. Kies `New OAuth App`.
6. Vul in:
   - Application name: `Kookboek CMS`
   - Homepage URL: de URL van je site, bijvoorbeeld `https://kookboek.jouwdomein.nl`
   - Authorization callback URL: de callback van je worker, bijvoorbeeld `https://cms-auth.jouwdomein.nl/callback`
7. Sla de app op.
8. Bewaar:
   - Client ID
   - Client Secret

## Cloudflare Worker voor CMS-auth

Je hebt een kleine OAuth-proxy nodig omdat Netlify Identity/Git Gateway verdwijnt.

Gebruik bij voorkeur een bestaande Decap OAuth worker, bijvoorbeeld:

- `https://github.com/sterlingwes/decap-proxy`
- `https://github.com/sveltia/sveltia-cms-auth`

Globale stappen:

1. Maak in Cloudflare een nieuwe Worker aan.
2. Deploy daar de code van de OAuth proxy.
3. Koppel een route of subdomein, bijvoorbeeld `cms-auth.jouwdomein.nl`.
4. Voeg secrets toe in de Worker:
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET`
5. Stel in de Worker ook de toegestane site-URL in als de gekozen proxy dat vraagt.
6. Test of de callback-URL bereikbaar is.

## Wat je daarna nog in deze repo moet invullen

Open [src/admin/config.yml](src/admin/config.yml) en vervang de placeholders:

```yml
backend:
  name: github
  repo: joepwillemsen/kookboek
  branch: main
  base_url: https://cms-auth.jouwdomein.nl
```

## Testen

1. Deploy de site op Cloudflare Pages.
2. Open `/admin`.
3. Log in via GitHub.
4. Maak een testrecept aan.
5. Controleer of er een commit op GitHub verschijnt.
6. Controleer of Cloudflare Pages daarna automatisch een nieuwe build start.

## Sync-regels

- GitHub is de bron van waarheid.
- CMS-wijzigingen komen als commits in GitHub terecht.
- Cloudflare Pages bouwt vanaf GitHub.
- Werk lokaal altijd zo:
  1. `git pull origin main`
  2. wijzig code
  3. `git pull --rebase origin main`
  4. `git push origin main`
