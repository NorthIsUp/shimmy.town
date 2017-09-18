APP := shimmytown

run:
	cd shimmytown ; ./manage.py runserver

db-backup-production: ##@db pull down a copy of the production db
	mkdir -p db_backups
	heroku pg:backups capture --app ${APP}
	$(eval DATE := $(shell date "+%Y-%m-%d_%H:%M:%S"))
	$(eval NAME := db_backups/production-${DATE})
	curl -o ${NAME} `heroku pg:backups public-url --app ${APP}`
	mv ${NAME} ${NAME}-`md5 -q "${NAME}"`.dump

db-backup-restore: ##@db Import the latest backup into the local db
	$(eval BACKUP := db_backups/$(shell ls -t db_backups/ | head -1))
	pg_restore --clean --no-owner --role=shimmytown --dbname shimmytown ${BACKUP}

db-sync: ##@db pull down production and restore  locally
db-sync: db-backup-production db-backup-restore

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
# A category can be added with @category
HELP_FUN = \
    %help; \
    while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
    print "usage: make [target]\n\n"; \
    for (sort keys %help) { \
    print "${WHITE}$$_:${RESET}\n"; \
    for (@{$$help{$$_}}) { \
    $$sep = " " x (32 - length $$_->[0]); \
    print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
    }; \
    print "\n"; }
?: help
h: help
help: ##@other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
