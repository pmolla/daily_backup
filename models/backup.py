import os
import subprocess
from odoo import models, api

class BackupToLocal(models.Model):
    _name = 'backup.to.local'
    _description = 'Backup Exporter to Remote PC'

    @api.model
    def export_backup(self):
        # 1. Backup Directory (Temporary Location)
        backup_dir = "/tmp/odoo_backups/"
        os.makedirs(backup_dir, exist_ok=True)

        # 2. Create the backup file
        db_name = self.env.cr.dbname
        backup_file = os.path.join(backup_dir, f"{db_name}_dump.sql")

        # Use pg_dump to create the database backup
        dump_command = [
            'pg_dump', '--no-owner', '--file', backup_file, db_name
        ]
        try:
            subprocess.run(dump_command, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error creating database dump: {e}")

        # 3. Transfer to Remote PC using SCP
        remote_user = "pablo.molla.ar"
        remote_host = "35.232.146.42"
        remote_path = "/home/pablo_molla/amic"
        self.transfer_backup_scp(backup_file, remote_user, remote_host, remote_path)

        # 4. Cleanup Temporary Backup
        if os.path.exists(backup_file):
            os.remove(backup_file)

    def transfer_backup_scp(self, backup_file, remote_user, remote_host, remote_path):
        scp_command = [
            'sshpass', '-p', 'pimpollo72',  # Pass the password
            'scp', backup_file, f"{remote_user}@{remote_host}:{remote_path}"
        ]
        try:
            subprocess.run(scp_command, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error transferring file via SCP: {e}")
