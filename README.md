# underwater_programmation_cameras

Organisation du projet : 
- `commande_camera.md` : fondamentaux, comment se connecter à la pi de commande de caméras, contrôler les caméras via `gphoto2` (voir remonter du flux vidéo, à tester)
- `python_CLI` : ensemble de scripts permettant le contrôle des caméras depuis python, à développer
- `node_UI` : base de travail pour développer une interface graphique sous la forme d'une application web

Répartition des rôles : 
- Robin : règlage des caméras + application web
- Alexandre : interfaçage avec périphériques via arduino

## TODO

### 1. Travail sur le hardware
   - Tester le **disque dur** : le connecter à une pi et tester les vitesses d'écriture
   - Réaliser un **montage où on aurait une fathom-X pour la pi de navigation et une autre pour la pi de commande des caméras**, on remonterait ainsi l'information via 2 des 4 connecteurs du tether, qui serait décodé ensuite en surface via 2 autres fathom-X -> tester si on observe une amélioration du débit (pas donné du fait des possibles interférences entre les différentes paires de câbles dans le tether)
   - Ajouter **1 arduino par camera** et s'en servir pour connecter les périphériques suivants : 
     - capteurs d'humidité
     - voltmètre/amperemetre sur la sortie de la batterie
     - LED pour communication avec les plongeurs 
   - Mettre en place le système complet (**cablage exterieur avec joints etanches**) : 2 cameras + 2 arduino + 1 pi + 1 batterie ( + 1 fathom-X si test précédent concluant).
### 2. Travail sur le software : CLI
   - **Command line interface python** : réussir à avoir un programme basé sur 2 threads (ou plus) permettant de sortir un flux vidéo ET de prendre des photos à la demande de l'utilisateur. (voir l'ébauche de script `capture_image_and_video.py`). Attention : tous les appels gphoto2 doivent être réalisés par le même thread (limitation de la communication USB avec la caméra.)
   - Ajouter à ce programme la possibilité de **modifier les paramètres de règlages** de l'appareil (toujours en ligne de commande).
   - **Cleaner** tout ça et incorporer le contrôle de **2 caméras en même temps**
### 3. Travail sur le software : UI
UI via application web = le mieux pour notre besoin (aussi le choix de bluerobotics)
   - Trouver le moyen de lire un flux vidéo reçu via RTP (avec `gstreamer`) **sur un navigateur web** 
   - Etablir si ce serait mieux d'utiliser **node+express ou Django** (Django permet peut être une intégration plus simple des codes pythons)
### 4. Travail sur le software : misc
   - Transmettre des fichiers via ssh depuis python (peut être appeler bêtement `scp` depuis python)
   - Une fois les périphériques connectés via la arduino : intégrer ces informations aux interfaces de commandes
