
run:
	docker-compose up --force-recreate --build

specs:
	make -C guide/ spec
	cp guide/openapi.yaml web/services/guide.yaml
	make -C users/ spec
	cp users/openapi.yaml web/services/users.yaml
	make -C navigator/ spec
	cp navigator/openapi.yaml web/services/navigator.yaml
