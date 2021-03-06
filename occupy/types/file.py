import os
import difflib
import pwd
import grp
import time
import shutil

from occupy.resource import Resource, IDVAR, InvalidParameter


class File(Resource):
    def __init__(self, id, path=IDVAR, content='', owner=None, group=None,
                 mode=0o644, backup='/var/occupy/backup', **meta):
        super().__init__(id, **meta)
        self.path = os.path.expanduser(path or id)
        if not self.path.startswith(os.sep):
            raise InvalidParameter("File paths must be fully qualified, "
                                   "not %r" % self.path)
        self.content = content.encode() if isinstance(content, str) else content
        self.owner = owner
        self.group = group
        self.mode = mode
        self.backup_dir = backup

    def apply(self):
        modified = self._update_content() | self._update_owner_group()
        if not modified:
            self.logger.debug("%s does not change", self)

    def _update_content(self):
        exists = os.path.exists(self.path)
        content = open(self.path, 'rb').read() if exists else None

        if content == self.content:
            return False

        exists = content is not None

        if exists:
            self._backup()

        with open(self.path, 'wb') as f:
            f.write(self.content)
        self.logger.info("updated" if exists else "created")

        try:
            fromlines = content.decode().splitlines() if exists else []
            tolines = self.content.decode().splitlines()
        except UnicodeError:
            self.logger.info("%d bytes -> %d bytes",
                             len(content) if exists else 0,
                             len(self.content))
        else:
            diff = difflib.unified_diff(
                fromlines, tolines, self.path if exists else '/dev/null',
                self.path)
            for line in diff:
                self.logger.debug(line.rstrip())

        return True

    def _update_owner_group(self):
        st = os.stat(self.path)
        mode = st.st_mode & 0o7777
        uid = st.st_uid
        gid = st.st_gid
        new_uid = uid if self.owner is None else pwd.getpwnam(self.owner).pw_uid
        new_gid = gid if self.group is None else grp.getgrnam(self.group).gr_gid
        modified = False

        if mode != self.mode:
            self.logger.info("chmod %04o -> %04o", mode, self.mode)
            os.chmod(self.path, self.mode)
            modified = True

        if uid != new_uid or gid != new_gid:
            self.logger.info("chown %s %s -> %s %s", uid, gid, self.owner,
                             self.group)
            os.chown(self.path, new_uid, new_gid)
            modified = True

        return modified

    def _backup(self):
        # We have ensured self.path.startswith(os.sep) in __init__()
        backup_path = "%s%s" % (
            self.backup_dir, self.path + time.strftime('-%Y-%m-%dT%H:%M:%S'))
        try:
            os.makedirs(os.path.dirname(backup_path))
        except OSError:
            pass
        shutil.copy(self.path, backup_path)
