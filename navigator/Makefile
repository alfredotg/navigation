python=python3.8

TEST_DB_FILE=./db/test.db
TEST_DB=sqlite:///${TEST_DB_FILE}

run: migrate
	${python} -m uvicorn main:app --reload --port 8102
migrate:
	${python} -m alembic upgrade head
migrate-rollback:
	${python} -m alembic downgrade -1
create-migration:
	read -p 'Migration name: ' name; \
	${python} -m alembic revision --message=$$name --autogenerate
requirements:
	${python} -m pip install -r requirements.txt
tests:
	rm -f ${TEST_DB_FILE} 
	DATABASE_URL=${TEST_DB} ${python} -m alembic upgrade head 
	DATABASE_URL=${TEST_DB} ${python} -m pytest --capture=no
lint:
	find . -type f -name "*.py" | grep -v alembic/ | xargs ${python} -m pylint  --extension-pkg-whitelist='pydantic' --disable=C,R
spec:
	${python} spec.py
