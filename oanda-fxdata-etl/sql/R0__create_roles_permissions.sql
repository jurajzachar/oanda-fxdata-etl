DROP ROLE IF EXISTS maintainer;
CREATE ROLE maintainer WITH SUPERUSER ENCRYPTED PASSWORD 'md5bd626974ecf0ea9fffe2873d453c42b0';
-- TODO restrict permissions
GRANT ALL ON SCHEMA oanda to maintainer