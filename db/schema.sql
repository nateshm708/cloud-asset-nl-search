CREATE TABLE IF NOT EXISTS cloud_accounts (
    account_id VARCHAR(12) PRIMARY KEY,
    account_name VARCHAR(50) NOT NULL,
    environment VARCHAR(20) CHECK (environment IN ('production', 'staging', 'development'))
);

CREATE TABLE IF NOT EXISTS ec2_instances (
    instance_id VARCHAR(30) PRIMARY KEY,
    account_id VARCHAR(12) REFERENCES cloud_accounts(account_id),
    name VARCHAR(100),
    region VARCHAR(20) NOT NULL,
    instance_type VARCHAR(20) NOT NULL,
    state VARCHAR(20) CHECK (state IN ('running', 'stopped', 'terminated')),
    launch_time TIMESTAMP,
    vpc_id VARCHAR(30),
    subnet_id VARCHAR(30),
    public_ip VARCHAR(45),
    private_ip VARCHAR(45),
    is_publicly_accessible BOOLEAN NOT NULL DEFAULT FALSE,
    tags_json TEXT
);

CREATE TABLE IF NOT EXISTS s3_buckets (
    bucket_name VARCHAR(100) PRIMARY KEY,
    account_id VARCHAR(12) REFERENCES cloud_accounts(account_id),
    region VARCHAR(20) NOT NULL,
    creation_date TIMESTAMP,
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    encryption_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    versioning_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    size_gb NUMERIC(10, 2) DEFAULT 0.0,
    tags_json TEXT
);

CREATE TABLE IF NOT EXISTS rds_instances (
    db_instance_id VARCHAR(100) PRIMARY KEY,
    account_id VARCHAR(12) REFERENCES cloud_accounts(account_id),
    region VARCHAR(20) NOT NULL,
    engine VARCHAR(30) NOT NULL,
    engine_version VARCHAR(20),
    instance_class VARCHAR(30),
    status VARCHAR(20),
    is_publicly_accessible BOOLEAN NOT NULL DEFAULT FALSE,
    storage_encrypted BOOLEAN NOT NULL DEFAULT TRUE,
    allocated_storage_gb INT,
    vpc_id VARCHAR(30),
    tags_json TEXT
);

CREATE TABLE IF NOT EXISTS security_groups (
    group_id VARCHAR(30) PRIMARY KEY,
    account_id VARCHAR(12) REFERENCES cloud_accounts(account_id),
    group_name VARCHAR(100) NOT NULL,
    region VARCHAR(20) NOT NULL,
    vpc_id VARCHAR(30),
    description TEXT,
    has_open_ingress_world BOOLEAN NOT NULL DEFAULT FALSE,
    open_ports TEXT,
    tags_json TEXT
);

CREATE TABLE IF NOT EXISTS iam_roles (
    role_arn VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(12) REFERENCES cloud_accounts(account_id),
    role_name VARCHAR(100) NOT NULL,
    create_date TIMESTAMP,
    is_admin_privilege BOOLEAN NOT NULL DEFAULT FALSE,
    attached_policies TEXT,
    tags_json TEXT
);