## for zip file
build-venv:
	@set PYTHONDONTWRITEBYTECODE=1
	@echo "[*] Building env"
	@rm -rf ./env
	@rm -rf ./package
	@mkdir -p package
	@python -m venv env
	@. ./env/bin/activate

install-deps:
	@echo "[*] Installing deps"
	@python -m pip install -r requirements.txt


create-package-dir:
	@echo "[*] Package Lambda Files"
	@cp file_validation.py ./package/ 
	@cp -r ./env/lib/python3.11/site-packages/ ./package/


build-zip:
	@echo "[*] Creating Zip file"
	@mkdir -p ./zips/
	@zip -r zips/aws_lambda_deployment_package.zip package
	
destroy-venv:
	@echo "[*] Destroying venv"
	@rm -rf ./package
	@rm -rf ./env

all: build-venv install-deps create-package-dir build-zip destroy-venv

# for docker file
docker: 
	@docker buildx build -t file-validation . --platform linux/amd64/v2 --no-cache
