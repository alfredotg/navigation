python=python3.8

run:
	${python} -m uvicorn main:app --reload --log-level debug
requirements:
	${python} -m pip install -d libs/ -r requirements.txt
tests:
	${python} -m pytest --capture=no
lint:
	find . -type f -name "*.py" | xargs ${python} -m pylint --extension-pkg-whitelist='pydantic' --disable=C,R
