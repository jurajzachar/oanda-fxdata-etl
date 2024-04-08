DROP ROLE IF EXISTS maintainer;
CREATE ROLE maintainer WITH SUPERUSER LOGIN ENCRYPTED PASSWORD 'md596d4cf3c1f62b2d963fd6b59cffdbf72';
-- TODO restrict permissions
GRANT ALL ON SCHEMA oanda to maintainer