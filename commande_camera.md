# Commande des caméras

Les Cameras sont connectés via USB à une raspberry elle même connectée via ethernet à l'autre raspberry du module de navigation et à l'ordinateur de surface via le tether.

Pour se connecter à la raspberry : 
```bash
ssh underwater@192.168.2.10
```
mdp : `underwater`

Les bibliothèques importantes : 
- `gphoto2` : commande des caméras, utilisable via un utilitaire que l'on appelle en ligne de commande / au sein de scripts shell ou via python (et C)
- `gstreamer` : programme permettant la conversion et la transmission de flux audios et video (permettant de récupérer le livefeed de la caméra : le flux vidéo de preview)

**Attention : ne pas saturer l'espace de stockage de la pi en prenant trop de photos (14Go au total)**

Pour *remonter les photos* : 
1. stocker les photos au sein d'un dossier (ex : `images`)
2. construire une archive : `tar cvf images.tar images`
3. remonter l'archive via ssh avec `scp` :
```bash
# depuis l'ordinateur de surface
scp underwater@192.168.2.10:/path/to/wd/images.tar .
```

Pour *déplacer les photos sur le disque dur* :
1. Connecter le disque dur puis utiliser `mv` (le disque devrait être monté dans `/media/underwater`)

### Réalisation d'une mission via gphoto2

Les commandes gphoto2 utiles : 
```bash
# Lister les caméras disponibles
gphoto2 --auto-detect

# prendre une photo
# cf ci dessous pour le formatage du nom de fichier
gphoto2 --capture-image-and-download --filename "%Y-%m-%d_%H:%M:%S.%C"

# lister les configurations possibles
# conseillé de rediriger ça vers un fichier pour ensuite y chercher le nom du paramètre que l'on souhaite modifier
gphoto2 --list-all-config

# connaître le réglage d'un paramètre (ex : param_name = imageformat)
gphoto2 --get-config <param_name>

# modifier un règlage
gphoto2 --set-config-index <param_name>=<index>
```

Pour retourner le flux vidéo via RTP sur l'ordi en surface (via `gstreamer`) :

- *Client* (ordinateur en surface)
```bash
gst-launch-1.0 -e -v udpsrc port=5000 ! \
	application/x-rtp, media=video, encoding-name=H264 ! \
	rtph264depay ! \
	queue ! \
	avdec_h264 ! \
	videoconvert ! \
	autovideosink
```

- *Server* (raspberry)
```bash
gphoto2 --capture-movie --stdout | gst-launch-1.0 -v -e \
  fdsrc ! \
  image/jpeg,framerate='(fraction)'24/1,width=640,height=426 ! \
  jpegdec ! \
  videocrop top=3 bottom=3 ! \
  queue ! \
  x264enc pass=qual quantizer=35 tune=zerolatency ! \
  rtph264pay ! \
  udpsink host=192.168.2.1 port=5000
```
