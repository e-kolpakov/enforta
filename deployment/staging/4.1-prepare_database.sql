CREATE ROLE DocApprovalUser LOGIN PASSWORD 'dau!w3aker_p@ssword';
CREATE DATABASE DocApproval;
GRANT CONNECT ON Database DocApproval to DocApprovalUser;
