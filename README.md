# Price Scraper Project

Ce projet utilise Playwright pour scraper le site Dealabs et récupérer le produit du jour. Les informations sont ensuite envoyées à un backend Node.js. Le scrapper peut être exécuté manuellement ou automatiquement toutes les 5 minutes grâce à une tâche CRON.

## Prérequis

- **Node.js** : Version 20.x ou supérieure est recommandée.
- **npm** : Assurez-vous que npm est installé avec Node.js.

## Installation

1. Clonez le dépôt :

   ````bash
   git clone <URL_DU_DEPOT>
   cd scrap-and-back   ```

   ````

2. Installez les dépendances :

   ````bash
   npm install   ```

   ````

3. Installez les dépendances de développement :
   ````bash
   npm install --save-dev typescript @types/node   ```

## Configuration

1. Assurez-vous que le fichier `tsconfig.json` est correctement configuré pour votre environnement.

2. Modifiez les sélecteurs CSS dans `src/scraper.ts` si nécessaire pour cibler les éléments corrects sur Dealabs.

## Compilation

Compilez le projet TypeScript en JavaScript :
