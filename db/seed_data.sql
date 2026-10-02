INSERT OR IGNORE INTO cloud_accounts VALUES
('123456789012', 'Production-Core', 'production'),
('987654321098', 'Staging-App', 'staging');

INSERT OR IGNORE INTO ec2_instances VALUES
('i-0a123bc456def789a', '123456789012', 'web-prod-01', 'us-east-1', 't3.micro', 'running', '2026-01-10 08:30:00', 'vpc-01111', 'subnet-0aaa1', '54.210.12.5', '10.0.1.5', TRUE, '{"Env":"prod", "Project":"WebFrontend"}'),
('i-0b987fc654edc321b', '123456789012', 'batch-processor', 'us-east-1', 'c5.2xlarge', 'stopped', '2026-02-01 12:00:00', 'vpc-01111', 'subnet-0aaa2', NULL, '10.0.2.20', FALSE, '{"Env":"prod", "Project":"DataBatch"}'),
('i-0c111222333444555', '987654321098', 'dev-test-server', 'us-west-2', 't2.small', 'running', '2026-03-15 14:20:00', 'vpc-02222', 'subnet-0bbb1', '34.220.88.99', '172.16.1.10', TRUE, '{"Env":"dev", "Owner":"Alice"}');

INSERT OR IGNORE INTO s3_buckets VALUES
('prod-customer-invoice-vault', '123456789012', 'us-east-1', '2025-05-12 10:00:00', FALSE, TRUE, TRUE, 1250.50, '{"DataClass":"Confidential"}'),
('public-website-assets-2026', '123456789012', 'us-east-1', '2026-01-01 00:00:00', TRUE, TRUE, FALSE, 15.20, '{"Project":"WebFrontend"}'),
('legacy-backup-dump-unencrypted', '123456789012', 'us-east-1', '2024-11-20 18:45:00', TRUE, FALSE, FALSE, 840.00, '{"Legacy":"True"}'),
('stg-app-temp-logs', '987654321098', 'us-west-2', '2026-02-10 09:15:00', FALSE, FALSE, FALSE, 45.00, '{"Env":"staging"}');

INSERT OR IGNORE INTO rds_instances VALUES
('prod-db-postgres-master', '123456789012', 'us-east-1', 'postgres', '15.4', 'db.m6g.xlarge', 'available', FALSE, TRUE, 500, 'vpc-01111', '{"Env":"prod", "Tier":"DB"}'),
('dev-test-mysql-public', '987654321098', 'us-west-2', 'mysql', '8.0', 'db.t3.medium', 'available', TRUE, FALSE, 100, 'vpc-02222', '{"Env":"dev"}');

INSERT OR IGNORE INTO security_groups VALUES
('sg-010101', '123456789012', 'web-public-sg', 'us-east-1', 'vpc-01111', 'Allow HTTP/HTTPS from world', TRUE, '80,443', '{"Tier":"Web"}'),
('sg-020202', '123456789012', 'ssh-debug-sg-DANGER', 'us-east-1', 'vpc-01111', 'Temporary SSH open access', TRUE, '22', '{"Temporary":"True"}'),
('sg-030303', '987654321098', 'internal-db-sg', 'us-west-2', 'vpc-02222', 'DB isolated access', FALSE, '', '{"Tier":"DB"}');

INSERT OR IGNORE INTO iam_roles VALUES
('arn:aws:iam::123456789012:role/AdministratorAccessRole', '123456789012', 'AdministratorAccessRole', '2025-01-01 00:00:00', TRUE, 'AdministratorAccess', '{"Audit":"Exempt"}'),
('arn:aws:iam::123456789012:role/EC2S3ReadRole', '123456789012', 'EC2S3ReadRole', '2026-01-15 11:30:00', FALSE, 'AmazonS3ReadOnlyAccess', '{"Service":"EC2"}');