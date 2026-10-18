# nathan-labbe.fr

Site statique (HTML, CSS, JS, aucun build, aucune dépendance) servi gratuitement par GitHub Pages sur www.nathan-labbe.fr.

## Contenu du repo

- `index.html` : la page, sections commentées
- `assets/css/style.css` : styles ; couleurs en variables en haut du fichier
- `assets/js/main.js` : menu mobile, section active, tracé du parcours (le site marche sans JS)
- `assets/fonts/` : police B612 auto-hébergée (aucun appel à Google Fonts)
- `assets/nl_picture.png` : ta photo, ajoutée à la main
- `assets/img/` : badges de certification (`itil4`, `PL300`, `PSPO`, `linguaskill`, noms exacts), `og-image.png` (l'aperçu affiché quand le lien est partagé sur LinkedIn…) et, si le script a tourné, les logos des compétences dans `skills/`
- `scripts/fetch_framer_assets.py` : rapatrie les logos des compétences depuis Framer (optionnel)
- `CNAME` : domaine personnalisé (`www.nathan-labbe.fr`)
- `404.html` : renvoie les anciennes URL Framer (`/projets/…`) vers l'accueil
- `robots.txt`, `sitemap.xml`, favicons

## Modifier le site

- Textes : `index.html`.
- Couleurs : bloc `:root` (thème clair) et bloc `prefers-color-scheme: dark` (thème sombre, automatique selon le réglage du visiteur) dans `style.css`.
- Compteurs de l'accueil : `<dd>8+</dd>` et `<dd>33+</dd>` dans `index.html`.
- Parcours : chaque ligne porte `--s` (début) et `--e` (fin) en années depuis 2020 (2022 = 2, en cours = 7) et `data-kind` : `exp`, `form` ou `now`.
- Compétences : `--v:92` = jauge à 92 %, le texte affiché est à côté.
- Badges : section Certifications de `index.html`. `data-ext` liste les autres extensions essayées si le fichier n'existe pas avec la première.
- Photo : remplacer `assets/nl_picture.png`. Nom exact, en minuscules : en ligne, `NL_Picture.PNG` ne sera pas trouvé, même si ça marche en local sur Mac ou Windows. Au-delà de ~500 Ko, la réduire à ~800 px de large.
- Aperçu de partage : `assets/img/og-image.png` (1200 × 630). LinkedIn garde l'ancien aperçu en cache plusieurs jours ; pour forcer la mise à jour, coller l'adresse du site dans https://www.linkedin.com/post-inspector/
- Prévisualiser : `python3 -m http.server 8000` à la racine, puis http://localhost:8000. En double-cliquant sur `index.html`, Chrome bloque les polices : c'est normal, le site en ligne n'a pas ce problème.
- Publier : commit + push, en ligne en 1 à 2 minutes.

## Mise en ligne (bascule depuis Framer)

Temps actif : environ 30 minutes. Attente : jusqu'à 1 h de propagation DNS (TTL actuel des enregistrements : 3600 s), puis l'émission du certificat HTTPS (GitHub annonce jusqu'à 24 h, c'est souvent bien plus court). Pendant cette attente, `https://` affiche une erreur de certificat : faire la bascule le soir.

### 1. Rapatrier les logos des compétences (optionnel), avant toute résiliation Framer

```
python3 scripts/fetch_framer_assets.py
```

Windows : `py scripts\fetch_framer_assets.py`. Le script dit ce qui a réussi et sort en erreur si une image manque. Ajouter aussi la photo (`assets/nl_picture.png`) et les badges (`assets/img/`), puis vérifier en local (voir « Prévisualiser »).

### 2. Vérifier le domaine sur GitHub

Protège contre le détournement du domaine par un autre compte GitHub.

1. GitHub, photo de profil → Settings → Pages → Add a domain → `nathan-labbe.fr`.
2. GitHub affiche un enregistrement TXT. Chez IONOS (Domaines & SSL → nathan-labbe.fr → DNS → ajouter un enregistrement) : type `TXT`, nom d'hôte `_github-pages-challenge-bouierck`, valeur donnée par GitHub.
3. Retour sur GitHub → Verify. Si ça échoue, réessayer quelques minutes plus tard.

### 3. Créer le repo et pousser

Repo public : GitHub Pages n'est gratuit que sur un repo public. Nom libre, par exemple `nathan-labbe.fr`, créé vide (sans README).

```
cd nathan-labbe.fr
git init -b main
git add .
git commit -m "Site statique nathan-labbe.fr"
git remote add origin https://github.com/bouierck/nathan-labbe.fr.git
git push -u origin main
```

### 4. Activer GitHub Pages

Repo → Settings → Pages :

- Build and deployment → Source : `Deploy from a branch` → branche `main`, dossier `/ (root)` → Save.
- Custom domain : `www.nathan-labbe.fr` → Save (souvent déjà rempli grâce au fichier `CNAME`).

Le « DNS check » échoue tant que l'étape 5 n'est pas faite : normal. Tant que le DNS pointe vers Framer, l'adresse `bouierck.github.io/...` redirige vers Framer, donc la seule prévisualisation possible avant bascule est en local.

### 5. Basculer le DNS chez IONOS

Domaines & SSL → nathan-labbe.fr → DNS.

Supprimer (Framer) :

- `A` `@` → `31.43.160.6`
- `A` `@` → `31.43.161.6`
- tout autre enregistrement vers Framer (`31.43.x.x` ou `sites.framer.app`), y compris un éventuel `*`

Modifier :

- `CNAME` `www` : `sites.framer.app` devient `bouierck.github.io`

Ajouter :

- `A` `@` → `185.199.108.153`
- `A` `@` → `185.199.109.153`
- `A` `@` → `185.199.110.153`
- `A` `@` → `185.199.111.153`
- `AAAA` `@` → `2606:50c0:8000::153`
- `AAAA` `@` → `2606:50c0:8001::153`
- `AAAA` `@` → `2606:50c0:8002::153`
- `AAAA` `@` → `2606:50c0:8003::153`

Ne pas toucher : `MX` (`mx00.ionos.fr`, `mx01.ionos.fr`) et `TXT` `v=spf1 include:_spf-eu.ionos.com ~all`, qui servent à la messagerie IONOS du domaine.

### 6. Activer HTTPS

Settings → Pages : attendre « DNS check successful », puis cocher `Enforce HTTPS`. La case reste grisée tant que le certificat n'est pas émis.

### 7. Tester

- https://www.nathan-labbe.fr affiche le nouveau site, cadenas valide.
- https://nathan-labbe.fr redirige vers `www`.
- https://www.nathan-labbe.fr/projets revient à l'accueil.
- `nslookup www.nathan-labbe.fr` répond `bouierck.github.io`.

### 8. Seulement ensuite : Framer

Retirer le domaine dans les réglages du projet Framer, puis résilier l'offre. Les images hébergées par Framer peuvent disparaître après résiliation : l'étape 1 doit être faite avant.

## Dépannage

- DNS check bloqué plus d'une heure : vérifier qu'il ne reste aucun `A` ou `AAAA` sur `@` autre que ceux de GitHub (IONOS peut recréer un enregistrement par défaut) et que `www` pointe sur `bouierck.github.io`, sans nom de repo.
- `Enforce HTTPS` toujours grisé après un DNS check réussi : Custom domain → Remove, puis le ressaisir → Save. Ça relance l'émission du certificat.
- Badge manquant : vérifier le nom exact du fichier dans `assets/img/`, majuscules comprises. Logo de compétence manquant : relancer le script. Dans les deux cas, l'emplacement est masqué proprement, sans icône cassée.
- Photo visible en local mais pas en ligne : le nom n'a pas exactement la bonne casse. Il doit être `assets/nl_picture.png`.

## Coûts

GitHub Pages : 0 €. Reste le renouvellement du domaine chez IONOS (échéance le 20/01/2027). Plus de statistiques de visite (Framer en fournissait) ; si besoin, GoatCounter est gratuit, sans cookie, et s'ajoute avec une ligne de script.

## Crédits

Police B612, conçue pour les écrans de cockpit Airbus, sous licence SIL Open Font License 1.1 (`assets/fonts/OFL.txt`).
