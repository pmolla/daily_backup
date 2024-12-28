import os
import shutil
from odoo import models, fields, api
import paramiko  # For SFTP

class BackupToLocal(models.Model):
    _name = 'backup.to.local'
    _description = 'Backup Exporter'

    @api.model
    def export_backup(self):
        # 1. Backup Directory
        backup_dir = "/home/odoo/backup/"  # Odoo.sh backup location
        os.makedirs(backup_dir, exist_ok=True)

        # 2. Create the backup
        db_name = self.env.cr.dbname
        backup_file = os.path.join(backup_dir, f"{db_name}_backup.zip")

        with open(backup_file, 'wb') as backup:
            self.env['ir.actions.report']._backup_database(backup)

        # 3. Transfer to Local PC (via SFTP)
        local_folder = "/path/to/your/local/folder"
        self.sftp_transfer(backup_file, local_folder)

        # 4. Cleanup
        if os.path.exists(backup_file):
            os.remove(backup_file)

    def sftp_transfer(self, backup_file, local_folder):
        sftp_host = 'your_pc_ip'
        sftp_port = 22
        sftp_user = 'your_username'
        sftp_password = 'your_password'

        try:
            transport = paramiko.Transport((sftp_host, sftp_port))
            transport.connect(username=sftp_user, password=sftp_password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            remote_file = os.path.join(local_folder, os.path.basename(backup_file))
            sftp.put(backup_file, remote_file)
            sftp.close()
            transport.close()
        except Exception as e:
            raise Exception(f"SFTP Error: {e}")
