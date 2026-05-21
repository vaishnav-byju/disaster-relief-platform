#!/bin/bash
DATE=$(date +%F)
FILE="/tmp/db_backup_$DATE.sql"

DB_HOST="disaster-relief-db.c3cgc2ya8kr0.ap-south-1.rds.amazonaws.com"
DB_USER="postgres"
DB_NAME="reliefdb"

pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $FILE

aws s3 cp $FILE s3://disaster-relief-backups-vaishnav/backups/
