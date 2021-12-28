python=python3.8

define run-generate =
rm -rf _$(1)/ $(1)/
openapi-python-client generate --path services/$(1).yaml --config services/$(1)_config.yaml
mv _$(1)/_$(1) $(1)
cp _$(1)/README.md $(1)/
rm -rf _$(1)/
endef

run:
	${python} -m uvicorn main:app --reload --log-level debug
requirements:
	${python} -m pip install -r requirements.txt
tests:
	${python} -m pytest --capture=no
lint:
	${python} -m pylint --extension-pkg-whitelist='pydantic' --disable=C,R ./main.py app/ 

clients:
	$(call run-generate,guide)
	$(call run-generate,users)
	$(call run-generate,navigator)
