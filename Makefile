## Automating AWS Lambda Layer creation using Makefile
## Author: HongJinHyeok

WORKSPACE = $(PWD)
OUTPUT = audit-user-access-layer.zip
AWS_LAYER_NAME = requests
AWS_LAMBDA_REGION = us-west-2
ARCHITECTURE = x86_64
VERSION = 3.11
# VERSION = $(python --version | awk '{print $2}' | cut -d '.' -f 1,2)

.PHONY: create-lambda-layer 
create-lambda-layer:
	@mkdir -p $(WORKSPACE)
	@pip install -t $(WORKSPACE)/python -r requirements.txt
	echo "Create lambda layer"

.PHONY: zip-lambda-layer
zip-lambda-layer:
	@if [ -d $(WORKSPACE) ]; then \
		cd $(WORKSPACE) && zip -r $(OUTPUT) ./python ; \
	else \
		echo "Directory not found"; \
	fi

.PHONY: publish-lambda-layer
publish-lambda-layer:
	@if [ -d $(WORKSPACE) ]; then \
		aws lambda publish-layer-version --layer-name $(AWS_LAYER_NAME) \
		--zip-file fileb://$(WORKSPACE)/$(OUTPUT) \
		--compatible-runtimes python$(VERSION) \
		--compatible-architectures $(ARCHITECTURE) \
		--region $(AWS_LAMBDA_REGION) ; \
	else \
		@echo "Directory not found"; \
	fi

.PHONY: clean-up
clean-up:
	@if [ -d $(WORKSPACE) ]; then \
		rm -r $(OUTPUT) ; \
	else \
		@echo "Directory not found"; \
	fi

.PHONY: all
all:	
	make create-lambda-layer
	make zip-lambda-layer
	make publish-lambda-layer
	make clean-up
	@echo "Lambda layer created successfully"