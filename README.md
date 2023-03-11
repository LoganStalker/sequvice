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