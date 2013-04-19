CREATE ROLE sa SUPERUSER LOGIN CREATEDB password 'sa!v3ry_str0ng_p@ssw0rd#!';
CREATE ROLE DocApprovalUser LOGIN PASSWORD 'dau!w3aker_p@ssword';
CREATE DATABASE DocApproval;
GRANT CONNECT ON Database DocApproval to DocApprovalUser;
GRANT ALL ON DATABASE DocApproval to sa;
