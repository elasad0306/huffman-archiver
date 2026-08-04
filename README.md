# Huffman Archiver 
C'est un outil de compression de fichiers sans perte basé sur l'**algorithme de Huffman**, développé en Python. Il permet de réduire la taille de fichiers (notamment textuels) et de les archiver sous un format personnalisé `.huff`.

---
## 1. Qu'est-ce le codage Huffman (Huffman Coding) ? 
Le codage de Huffman est un algorithme de compression statistique inventé par David Huffman. Le principe fondamental repose sur la fréquence d'apparition des symboles (octets ou caractères) dans un fichier :
* Les symboles **les plus fréquents** reçoivent un code binaire **court** (ex: `0` ou `10`).
* Les symboles **les plus rares** reçoivent un code binaire **long** (ex: `11010`).

Contrairement aux encodages classiques (où chaque caractère prend une taille fixe, par exemple 8 bits), Huffman utilise des **codes à longueur variable** sans ambiguïté (propriété de préfixe : aucun code n'est le préfixe d'un autre), ce qui permet de réduire significativement la taille globale du fichier.

---
## 2. Structure du fichier `.huff`
Pour qu'un fichier compressé puisse être décompressé ultérieurement, le format `.huff` embarque un en-tête (*header*) suivi des données :
1. **Le Padding (1 octet)** : Indique le nombre de bits de bourrage ajoutés à la fin de la chaîne binaire pour obtenir une longueur multiple de 8.
2. **La taille de la table (4 octets)** : Indique la taille en octets de la table des fréquences sérialisée.
3. **La table des fréquences** : Sérialisée via le module `pickle`, elle permet de reconstruire l'arbre de Huffman à l'identique lors de la décompression.
4. **Les données compressées** : Les octets effectifs générés à partir de la chaîne de bits.

---
## 3. Fonctionnement du Code

Le script principal s'articule autour des étapes clés suivantes :

* **Lecture du fichier (`'rb'`)** : Le fichier source est lu en mode binaire pour traiter directement tous types de flux d'octets.
* **Calcul des fréquences** : Utilisation de `Counter` pour compter les occurrences de chaque octet.
* **Construction de l'arbre de Huffman** : Utilisation d'un tas min (`heapq`) pour fusionner itérativement les nœuds de plus faibles fréquences.
* **Génération des codes** : Un parcours récursif de l'arbre associe à chaque octet sa séquence binaire unique.
* **Padding et conversion en octets** : La chaîne de bits globale est complétée par des zéros pour s'aligner sur des blocs de 8 bits, puis convertie en un tableau d'octets (`bytearray`).
* **Écriture de l'archive** : Assemblage et écriture de l'en-tête et des données dans le fichier de sortie (`arch_nom_du_fichier.huff`).

---
## 4. Utilisation

Pour lancer la compression, assurez-vous d'avoir Python installé et exécutez le script principal en adaptant le chemin de votre fichier source dans le programme :

```bash
python main.py
````