# Projet TuxML&Kernelci : LAVA

---

Copie du git contenant la version dockerisé de LAVA afin de la modifier pour la rendre utilisable en local et pour le script crée par TuxML sur un base de KernelCI.

### Requiements

- Docker
- Docker compose
- pyyaml

## Get started 

1. Ils peuvent modifier le board.yaml si il y a des storages à ajouter ou des slaves ou même des masters

```bash
./lavalab-gen.py
```

2. Build

```bash
docker-compose build
```

3. Démarrage

```bash
docker-compose up -d
```

4. Accès localhost:10080