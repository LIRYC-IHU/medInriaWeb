#  **Liryc Girder Viewer – Documentation du Code**

## 🧩 Description générale
Ce projet est une ébauche d'**interface web de visualisation de dossiers médicaux (Girder Viewer)**.  
Il a pour but notamment :
- de **sélectionner un dossier patient anonymisé** et d’en **afficher la liste des fichiers** ;
- de **consulter des métadonnées patient ou étude** (ID,date d'acquisition, type d'imagerie, nombre de coupes) ;
- d’interagir avec différents outils de navigation, d’affichage et d’annotation d’images, de contouring (via des icônes et des interactions simulées).

L’application repose actuellemnt entièrement sur des **technologies front-end** — aucun serveur ni installation n’est requis.

Il est possible de "prélever" les blocs modulaires de code en fonction des besoins.

---

## ⚙️ Bibliothèques utilisées

| Bibliothèque | Rôle | Chargement |
| -------- | ------ | ------- |
| **[Tailwind CSS](https://tailwindcss.com/)** | Framework utilitaire pour le style CSS (mise en page responsive, couleurs, espacement, etc.) | via CDN |
| **[DaisyUI](https://daisyui.com/)** | Extension de Tailwind proposant des composants UI préconstruits (boutons, inputs, cartes...) | via CDN |
| **[AlpineJS](https://alpinejs.dev/)** | Micro-framework JavaScript réactif (gestion des états et interactions) | via CDN |

Aucune installation ni compilation n’est nécessaire : tout est importé depuis des CDN publics.

---

## 🔧 Fonctionnalités

| Fonction | Description | Technologies |
| ------ | ------ | ------ |
| **Modale de connexion** | Assurer un **accès restreint** à certaines fonctions du viewer (par exemple : chargement de données sensibles, ou synchronisation avec un serveur) | AlpineJS + DaisyUI |
| **Sélection d’un dossier** | Sélectionner un répertoire local et afficher son contenu | `<input type="file" webkitdirectory>` + AlpineJS |
| **Liste de fichiers** | Affichage **dynamique** du contenu sélectionné | AlpineJS + DaisyUI |
| **Carte d’infos**  | Métadonnées patient statiques (exemple) | HTML + Tailwind  |
| **Recherche rapide** | Champ stylisé, (mock-up) | DaisyUI |
| **Zone centrale** | Préparation d’un viewer avec outils (icônes SVG) | AlpineJS + SVG inline |
| **Styles & Layout** | Apparence moderne et responsive | TailwindCSS |

## 📑 Notions importantes à garder à l'esprit
- Garder une UI sombre et modérement contrastée pour éviter la fatigue viduelle
- Une UI simple (favoriser icones légendées au texte brut) à légèrement avancée (keybinds, menus retractibles) pour éviter de rebuter l'utilisateur. Pssibilité de la faire évoluer en fonction des retours.
- Render la webpage en priorisant la vue principale puis des annexes en tache de fond (3D sur demande) permettant ainsi une utilisation quasi immédiate (en d'autres termes : éviter les longs chargements)

## 🔬 Pistes d'amélioration
- **SOC** : Séparer les composaants en différents fichiers (maintenabilité ++)
  Séparer le JS Alpine dans un fichier dédié (viewer.js) si JS conservé
- **Style** : séparer le CSS ds un fichier dédié pour plus de lisibilité et de facilité de maintenance (créer des variables pr les styles communs)
  Thèmes clair/sombre

- Connecter la modale à un système d’authentification réel (API, JWT, session).
- Ajout d’un message d’état pr la connexion (Par exemple : “Connexion réussie” ou “Identifiants incorrects”.)
- Prévoir une modale d’inscription ou de mot de passe oublié.

- Afficher un “breadcrumb” de navigation
( = Une petite barre indiquant le dossier ouvert ex : /Documents/DICOM/Patient123/)
- Indiquer la taille et le type de fichiers
- Ajouter un “drag & drop” depuis l'arborescence du dossier vers le viewer


*Fabien Francezon - 23 octobre 2025*