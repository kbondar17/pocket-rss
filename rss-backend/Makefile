-include .env
export


lint:
	@mypy weedly
	@flake8 weedly


test:
	@pytest


db.up:
	@docker-compose up -d db

add_test_rss:db.up
	@python -m weedly.db create
	@python -m weedly.db add-test-rss
	
go_db:
	db.up
	add_test_rss



db.recreate: db.clean db.up
	@sleep 5
	@python -m weedly.db


db.clean:
	@echo "clean all resources: db"
	@docker-compose down -t1


run:
	@gunicorn -w 4 -b 0.0.0.0:5000 weedly.app:app

