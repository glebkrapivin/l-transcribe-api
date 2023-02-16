generate:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

init_db:
	python -m scripts.sample_data

