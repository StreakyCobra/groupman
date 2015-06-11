ENVFOLDER := _ENV

build: $(ENVFOLDER)
	pip install . --upgrade

help: $(ENVFOLDER)
	@echo "Run the following command:\n"
	@echo "    eval \$$(make setup)"

setup: $(ENVFOLDER)
	@echo "source ./$(ENVFOLDER)/bin/activate; source ./completions/zsh; export PATH=./$(ENVFOLDER)/bin:$$PATH"

clean:
	@rm -rf $(ENVFOLDER)

$(ENVFOLDER):
	@virtualenv $(ENVFOLDER) 1>/dev/null
