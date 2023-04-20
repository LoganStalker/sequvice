git clone https://github.com/LoganStalker/sequvice.git

### **MAKE VENV**
```shell
python -m venv venv 
source venv/bin/activate
```
### **INSTALL DEPENDECIES**
```shell
pip install -r requirements.txt
```

### **INIT DATABASE**
```shell
make init_db
```

### **RUN APP**
```shell
make dev
```

### **RUN TESTS**
```shell
make t
```


### **HOW TO USE MIGRATIONS MANAGER**
Firstly change models. Then run creating command
```shell
python mograte_manage.py -create -name migration_name
```
Then run migrating commang
```shell
python mograte_manage.py -migrate
```
If need to rollback migration run rollback command. It rollback only last migration.
```shell
python mograte_manage.py -rollback
```
