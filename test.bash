if [ -f .env.test ]; then
	export $(grep -v '^#' .env.test | xargs)
fi

chmod +x reset_test_db.bash
poetry run coverage run --branch -m pytest src
