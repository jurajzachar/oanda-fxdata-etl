# install the new version
sudo apt-get update
sudo apt-get install postgresql-14 postgresql-server-dev-14

# halt the old server
sudo systemctl stop postgresql.service

# postgres upgrade script (v12 --> v14)
sudo -u postgres /usr/lib/postgresql/14/bin/pg_upgrade \
--old-datadir=/var/lib/postgresql/12/main \
--new-datadir=/var/lib/postgresql/14/main \
--old-bindir=/usr/lib/postgresql/12/bin \
--new-bindir=/usr/lib/postgresql/14/bin \
--old-options '-c config_file=/etc/postgresql/12/main/postgresql.conf' \
--new-options '-c config_file=/etc/postgresql/14/main/postgresql.conf'

# activate the new server version and verify
sudo systemctl start postgresql.service
sudo -u postgres psql -c "SELECT version();"

# install timescaledb extension
sudo apt install timescaledb-2-postgresql-14

# update timescaledb config
timescaledb-tune --quiet --yes

# see also: https://medium.com/yavar/upgrade-postgresql-version-in-ubuntu-20-04-dfdce9193bc