
CREATE ROLE sa SUPERUSER LOGIN CREATEDB PASSWORD 'sa!v3ry_str0ng_p@ssw0rd#!';
CREATE ROLE DocApprovalUser LOGIN PASSWORD 'dau!w3aker_p@ssword';
CREATE DATABASE docapproval;
GRANT CONNECT ON DATABASE DocApproval TO DocApprovalUser;
GRANT ALL ON DATABASE DocApproval TO sa;
