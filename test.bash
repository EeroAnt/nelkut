if [ -f .env.test ]; then
	export $(grep -v '^#' .env.test | xargs)
fi

poetry run coverage run --branch -m pytest
