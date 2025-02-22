# MySQL Database Credentials
DB_USER="root"
DB_PASS="awsPassword123fk"
DB_HOST="ispj-db.cxruucec3o8o.us-east-1.rds.amazonaws.com"
DB_NAME="ISPJ_DB"

# Backup Storage Directory (Change to your actual path)
BACKUP_DIR="/c/Users/Kenzi/Desktop/VS_CODE_FOLDER/ISPJ/AdminApp/app/databasebackup" #for integration replace with the absolute path to database backup folder
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Find MySQL bin directory
MYSQLDUMP_PATH="/c/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe" # for integration replace with absolute path to mysqldump.exe

# Ensure MySQL Dump exists
if [ ! -f "$MYSQLDUMP_PATH" ]; then
    echo "Error: mysqldump not found. Check your MySQL installation path!"
    exit 1
fi

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Run MySQL dump (WITHOUT gzip, saves as .sql)
"${MYSQLDUMP_PATH}" -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" \
    --column-statistics=0 --set-gtid-purged=OFF --no-tablespaces > "$BACKUP_FILE"

# Keep only the last 7 backups (delete older files)
find "$BACKUP_DIR" -type f -name "*.sql" -mtime +7 -exec rm {} \;

echo "✅ Backup completed successfully: $BACKUP_FILE"



#create test_backup_db to test data backup import
#CREATE DATABASE test_backup_db;

#USE test_backup_db;
#select *
#from messages

#how to use:
# Run commands in bash in vs code
#Navigate to the script folder in (bash):
        # cd "ISPJ/AdminApp/app/databasebackup"

# give permission (bash):
        # chmod +x backup_mysql.sh only need do once

#run script manuelly or wait for auto schedule :
   #./backup_mysql.sh

#task scheduler:
#set to run every 2am
#program/script: "C:\Program Files\Git\git-bash.exe"
#argument absolute path to script: -c "/c/Users/Kenzi/Desktop/VS_CODE_FOLDER/ISPJ/AdminApp/app/databasebackup/backup_mysql.sh"
