# B8ZS en/de-codeur - CEG3585 Lab3
## _Groupe 3 : Andie Samadoulougou ; Hedi Ben Abid_

## Tables des matieres 
I - Contexte/Sujet
II - Deroulement du programme 
II - Fonctionnement de l'encodage et du decodage
III - Communication entre programmes et principe d'encodage 
IV - Utilisation 

## Contexte/Sujet : 
1.L'entrée du programme de codage (client) est une chaîne de 0 et 1, entrée à partir du clavier.
2. La chaîne binaire d'entrée est encodée par le programme d'encodage en B8ZS. On suppose toujours
que la polarité du premier 1 est positive.
3. Le programme d'encodage doit envoyer un message « demande d’envoi » au programme de
décodage et attendre la réponse « prêt à recevoir » du programme de décodage, avant de l'envoyer.
4. Le programme de décodage (serveur) envoie un message « prêt à recevoir » au programme de
codage après avoir reçu une « demande à envoyer » du programme de codage.
5. Le flux B8ZS est alors transmis au programme de décodage via le socket.
6. Après réception du flux B8ZS, le programme de décodage accusera réception au programme
d'encodage.
7. Ensuite, le programme de décodage décode le flux B8ZS dans son format d'origine et l’imprime à
l'écran.
8. Le flux encodé de B8ZS est représenté par la séquence de trois caractères, « + », « - » et « 0 », ce
qui signifie respectivement l'impulsion positive, l'impulsion négative, et aucun signal.
9. Vous devez soumettre dans un fichier zip votre code et un fichier README expliquant comment
exécuter vos programmes et ce qui est attendu en entrée / sortie


## Deroulement du programme 

Le client se connecte au serveur actif et lui demande s'il est pret a recevoir un message encodé. 
Lorsque le Serveur recoit la demande, il active un drapeau (waiting=True) et informe le client qu'il est pret a recevoir le message. 
Lorsque le client recoit la confirmation du serveur, il lui envoie les donnees que l'utilisateur tape dans la console. 
Lorsque le serveur recoit un message de la part du client, il verifie que son drapeau est actif (ce qui veut dire qu'il est pret a faire le decodage). Si le drapeau est actif, il decode le message et l'affiche dans la console du serveur. 

##  Fonctionnement de l'encodage et du decodage

### _Encodage_ 
2 Drapeaux sont utilisés pour suivre l'etat de l'encodage : _wasLow_ qui indique si le precedent bit 1 etaient haut ou bas ; _inASequence_ qui indique si l'on est actuellement dans une sequence de B8ZS
Une autre variable entiere _toIgnore_ indique le nombre de tours a ignorer

Une boucle parcours le string qui a ete fourni en entreé et pour chaque element s'il: 
- est egal a 1 : Ajouter "+" dans la chaine de resultat si le bit precedent etait low (on le sait grace au drapeau wasLow )puis changer la valeur du drapeau a False. Sinon, Ajouter "-" dans la chaine de resulat et changer le drapeau  a true
- egal a 0 : 
> +Si on est dans une sequence ou que la variable toIgnore n'est pas nulle, ignorer ce tour 
> +Si non, verifier s'il y a au moins 8 caracteres restants. Si c'est le cas, on verifie qu'il s'agit tous de 0. Si ce sont tous des 0, on remplace par la sequence adequate et on met to ignore a 7 pour sauter les 7 prochains tours. Si ce ne sont pas tous des 0 ou qu'il y a moins de 8 characteres, on continue le processus normal  


### _Decodage_

1 Drapeau est utilisé pour suivre l'etat du decodage :  _inASequence_ qui indique si l'on est actuellement dans une sequence de B8ZS
Une autre variable entiere _toIgnore_ indique le nombre de tours a ignorer

Une boucle parcours le string qui a ete fourni en entreé et pour chaque element: 
- Si on est dans une sequence ou que la variable toIgnore n'est pas nulle, ignorer ce tour
------ Sinon   
- Si l'element est egal a 0 : 
> +Si il reste moins de 8 caracteres, ajouter 0 a la chaine de resultat 
> +S'il y'a au moins 8 caracteres, verifier s'il s'agit d'une sequence B8ZS. Si c'est le cas, on ajoute 8 zeros a la chaine de resultat, et on met le nombre de tours a ignorer a 7. Si ce n'est pas une sequence de B8ZS, on met juste 0 et on continue le processus normal 
- Si l'element est egal a + ou  a - :
> +Si il reste moins de 8 caracteres, ajouter 1 a la chaine de resultat 
> +Si non, verifier si les huits prochains caracteres correspondent a une sequence de B8ZS, on ajoute 8 zeros et on met le nombre de tours a ignorer a 7 et on indique qu'on est dans une sequence


## Communication entre programmes et principe d'encodage
La communication se fait grace aux sockets et au protocol TCP/IP que nous avons implementé durant notre premier laboratoire. 

- TCP/IP - Protocol de communication   
- B8ZS - Encodage pour la transmission de donneées
- Python - Langage de programmation 

## Utilisation 

Côté server 
```sh
python server.py
```
Côté client 
```sh
python client.py
```
Puis suivez les instructions et tapez vos donnees :) 



