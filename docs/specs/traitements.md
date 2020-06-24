---
title:
- Description des traitements
date:
- 17-06-2020
author: |
  | Valar Morghulis
  | by
  | Birna Gérald, Sergent Pierre-Louis & Launay Matthieu
papersize:
- a4
fontsize:
- 12pt
geometry:
- margin=1.25in
header-includes: |
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhead[L]{Projet tutoré}
    \fancyhead[R]{Protection et vérification des sources}
---

\maketitle
\clearpage
\tableofcontents
\clearpage

# Objet du document

Ce document aura pour but de reprendre la description des fonctionnalités effectuées dans le cahier des charges et d'apporter des précisions supplémentaires afin de mener à bien le développement.

# Fonctionnalités détaillées

Les fonctionnalités seront découpés en plusieurs niveaux de priorités : 

- **Obligatoires** (FOB) : absolument nécessaire pour la *MVP (Minimum Valuable Product)*  du projet
- **Optionnelles** (FOPT) : pas totalement nécessaire mais peuvent être utile pour avoir un produit abouti 
- **Futures** (FF) : pas vraiment attendues dans le cadre de la réalisation du projet tutoré, mais souhaitable pour le futur

## Obligatoires

Les utilisateurs pourront s'inscrire, créer des articles et par ce biais déposer des documents sur la plateforme. Ils pourront ensuite soumettre ces articles aux médias et experts pour vérification.

Le dépôt de documents se fera dépendemment de la création d'article. Un article pourra comporter un titre, un corps et un ensemble de documents (facultatif).

Les médias ou expert pourront créer un compte sur le plateforme puis demander à être vérifiés pour acquérir un statut particulier, qui leur permettra de recevoir les articles que les utilisateurs lambda veulent faire vérifier.

---

**FOB.1 - Module d'authentification**

L'utilisateur pourra créer un compte, qui aura les droits de base. Il devra effectuer une demande spéciale par mail si il souhaite acquérir un compte vérifié.

- **FOB.1.1 - Inscription**
- **FOB.1.2 - Connexion/déconnexion**

**FOB.2 - Module cloud sécurisé**

Une fois connecté l'utilisateur aura accès à une page qui listera tous les articles qu'il a rédigé. Il pourra accéder aux détails de chacun d'entre eux, télécharger les documents qui sont liés à ces derniers et modifier/supprimer les contenus. Il pourra aussi publier ou soumettre son article à vérification auprès des experts.

- **FOB.2.1 - CRUD Article**\newline
L'utilisateur pourra seulement déposer des **articles** sur son "cloud", tout dépôt de documents se fera avec la création d'un article. De plus, les données stockées en base seront sécurisés, plusieurs pistes possibles pour le chiffrement (communication SSL, utilisation d'une clef de chiffrement).\newline
Chaque article aura la possibilité d'avoir une vignette de certification, qui atteste que l'article a été validé par les médias/experts.
	- ***FOB.2.1.1*** : lister les articles
	- ***FOB.2.1.2*** : créer un article (contenu + fichiers)\newline
		Formulaire : titre, corps et fichiers
		
	Les fichiers et informations devront être cryptés sur le serveur
	- ***FOB.2.1.3*** : détails d'un article
		- FOB.2.1.3.1 : afficher contenu
		- FOB.2.1.3.2 : télécharger fichiers liés 
	- ***FOB.2.1.4*** : modifier un article
	- ***FOB.2.1.5*** : supprimer un article\newline

- **FOB.2.2 - Soumettre article**\newline
Formulaire : sélection des médias/experts qui auront accès à l'article ainsi que tous les fichiers joints, et qui pourront attester la véracité des informations. A savoir que si un article est soumis à plusieurs médias/experts, l'article devra recevoir une majorité d'avis favorable pour recevoir la vignette de certification.

---

**FOB.3 - Module de vérification**

Si un utilisateur se fait vérifier par la plateforme il gagne alors le statut de média/expert. De ce fait, il a maintenant accès à une nouvelle page qui répertorie les articles mis à sa disposition pour une demande de vérification. Il peut désormais les consulter et rendre son verdict.

**Processus de vérification** : envoie d'un mail à l'équipe de développement, constitution d'un dossier avec les pièces justificatives nécessaires et enfin vérification du profil. Une fois le verdict rendu, la mise à jour du profil se fera par les développeurs à partir de la plateforme d'administration ou la base de données.

- **FOB.3.1 - Consultation articles soumis**
	- ***FOB.3.1.1*** : lister les articles soumis (similaire *FOB.2.1.1*)
	- ***FOB.3.1.2*** : vue détaillée de chaque article (similaire *FOB.2.1.3*)\newline

- **FOB.3.2 - Validation article**\newline
Simple boutton présent dans la vue détaillée.

### Vues obligatoires

- Connexion / inscription classique
- Espace de stockage "cloud" (*FOB.2.1*)
	- créer article (formulaire)
	- détail article
	- soumettre article (formulaire)

**Réservé utilisateurs vérifiés** :

- Espace de vérification (*FOB.3.1*)

## Optionnelles

Le module décrit dans la partie *2.1.2 - Feed d'actualité* sera développé dans un second temps, si et seulement si les fonctionnalités obligatoires ont été satisfaites. Ce module sera donc optionnel, tout comme certaines améliorations qui rendront l'utilisation de la plateforme plus agréable.

- **FOB.2.1 - CRUD Article**
	- ***FOB.2.1.1*** : lister les articles
		- FOPT.2.1.1.1 : filtrer / trier les articles avec différents critères
	- ***FOB.2.1.3*** : détails d'un article
		- FOPT.2.1.3.3 : lire / consulter les documents directement en ligne (sans télécharger)
		- FOPT.2.1.3.4 : un espace "description" pour chaque document\newline

- **FOPT.2.3 - Publier article**\newline
Permet de place l'article dans l'espace public du site et sera lisible dans la section *FOPT.4*.

---

- **FOB.3.1 - Consultation articles soumis**
	- ***FOB.3.1.1*** : lister les articles soumis (similaire *FOB.2.1.1*)
		- FOPT.3.1.1.1 : filtrer / trier les articles avec différents critères (similaire *FOPT.2.1.1.1*)
	- ***FOB.3.1.2*** : détails d'un article (doublon *FOB.2.1.3*)
		- FOPT.3.1.2.1 : lire / consulter les documents directement en ligne (sans télécharger) (similaire *FOPT.2.1.3.3*)
		- FOPT.3.1.2.2 : un espace "description" pour chaque document (similaire *FOPT.2.1.3.4*)
	- ***FOPT.3.1.3*** : commentaires / discussion avec l'auteur de l'article\newline
	Le media/expert pourra commenter les articles ou entrer en contact avec le lanceur d'alerte pour demander des informations supplémentaires\newline

- **FOB.3.2 - Validation article**
	- ***FOPT.3.2.1*** : argumenter les raisons de la validation / invalidation\newline
	A la manière de la *FOPT.3.1.3*, le media/expert pourra laisser un commentaire avec le rendu de son verdict

---

**FOPT.4 - Module feed d'actualité**

Si un utilisateur décide de publier son article (*FOPT.2.3*), alors il sera accessible librement par tous directement sur la page d'accueil. Le fil d'actualité sera décidé en fonction du nombre de votes sur chaque article, ainsi qu'à la vignette de certification. Les articles les plus encensés et les plus vérifiés seront mis en avant.

- **FOPT.4.1 - Lister les articles publiés**
	- ***FOPT.4.1.1*** : consulter le détail d'un article (similiaire *FOB.2.1.3*)\newline
	Possibilité d'y effectuer les fonctionnalités *FOPT.4.2* et *FOPT.4.3*

- **FOPT.4.2 - Upvote / downvote**\newline
A la manière de Reddit, l'utilisateur pourra pour chaque article mettre un *upvote* ou un *downvote*. Ces votes auront une influence sur la constitution de l'ordre du fil d'actualité.

- **FOPT.4.3 - Sourçage**\newline
Les utilisateurs pourront valider ou invalider la véracité de chaque article en ajoutant des liens à ces derniers. Dans un premier temps, seul les liens vers des sites web seront acceptés.

### Vues optionnelles

Vues obligatoires +

- Fil d'actualité (*FOPT.4.1*)
	- détail article

*Ajout de source et vote directement sur la page principale*
	
## Futures

Concernant les fonctionnalités futures, elles consistueront essentiellement des améliorations du fil d'actualité et de l'expérience générale du site.

**FF.1 - Réputation utilisateur**\newline
Donner des points de "réputation" aux utilisateurs lorsqu'ils reçoivent un certain nombre de upvote ou de certification.

**FF.2 - Consulter les nouveaux articles publiés**\newline
Avoir une page dédiée aux nouveaux articles afin de garantir une bonne visibilité à toutes les *news*.

--- 

- **FOPT.4.1 - Lister les articles publiés**
	- ***FF.4.1.2*** : filtrer / trier les articles avec différents critères\newline

- **FOPT.4.3 - Sourçage**
	- ***FF.4.3.1*** : accompagner les liens ajoutés de commentaires
	- ***FF.4.3.2*** : système de vote sur les commentaires / sourçages
	- ***FF.4.3.3*** : vérifier lien en amont, *scrapping* de la page pour vérifier son contenu et ainsi valider ou invalider un lien
	- ***FF.4.3.4*** : possibilité de fournir un ouvrage comme source
	
### Vues futures

Vues obligatoires et optionnelles +

- Compte utilisateur (informations générales + réputation)
- Nouveaux articles
