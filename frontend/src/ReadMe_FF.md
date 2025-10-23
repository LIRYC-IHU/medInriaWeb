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
| **Sélection d’un dossier** | Sélectionner un répertoire local et afficher son contenu | `<input type="file" webkitdirectory>` + AlpineJS |
| **Liste de fichiers** | Affichage dynamique du contenu sélectionné | AlpineJS + DaisyUI |
| **Carte d’infos**  | Métadonnées patient statiques (exemple) | HTML + Tailwind  |
| **Recherche rapide** | Champ stylisé, non fonctionnel (mock-up) | DaisyUI |
| **Zone centrale** | Préparation d’un viewer avec outils (icônes SVG) | AlpineJS + SVG inline |
| **Styles & Layout** | Apparence moderne et responsive | TailwindCSS |


*Fabien Francezon - 23 octobre 2025*