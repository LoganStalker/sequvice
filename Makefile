VIRTUAL_ENV     ?= venv
PROJECT         ?= app

all: $(VIRTUAL_ENV)

.PHONY: init_db
init_db: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/python -m sequvice_app -init_db

.PHONY: dev
dev: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/python -m sequvice_app -run
