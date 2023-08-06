Version: 1.1.10
Utils for ryoka.

**Usage:**

*Utils*

    from ryoka_utils.utils import Utils

    utils = Utils()

    + utils.abspath(self, path)
    + utils.basename(self, path)
    + utils.chmod(self, path, mode)
    + utils.chown(self, path, user, group)
    + utils.command(self, cmd)
    + utils.copy(self, src, dst)
    + utils.decode(self, text)
    + utils.dirname(self, path)
    + utils.exit(self)
    + utils.get_current(self, file_path)
    + utils.get_dir_path_in_dir(self, dir_path)
    + utils.get_env(self, key)
    + utils.get_file_path_in_dir(self, dir_path)
    + utils.is_root(self)
    + utils.isdir(self, path)
    + utils.isfile(self, path)
    + utils.join_dirs(self, path_list)
    + utils.mkdir(self, path)
    + utils.popd(self)
    + utils.pushd(self, path)
    + utils.remove(self, path)
    + utils.rename(self, src, dst)
    + utils.splitext(self, path)
    + utils.unzip_tar(self, src, dst)
    + utils.unzip_tar_bz2(self, src, dst)
    + utils.unzip_tar_gz(self, src, dst)
    + utils.zip_tar(self, src, dst, mode)
    + utils.zip_tar_bz2(self, src, dst)
    + utils.zip_tar_gz(self, src, dst)

*SendMail*

    from ryoka_utils.mail import SendMail

    mail = SendMail()

    + mail.send(self)
    + mail.set_body(self, body)
    + mail.set_charcode(self, code)
    + mail.set_from_address(self, address)
    + mail.set_password(self, password)
    + mail.set_title(self, title)
    + mail.set_to_address(self, address)

*Debugger*

    from ryoka_utils.debugger import Debugger

    debugger = Debugger(is_debug)

    + debugger._output(self, mode)
    + debugger.error(self)
    + debugger.log(self)
    + debugger.warn(self)

*Slack*

    from ryoka_utils.slack import Slack

    slack = Slack(token)

    + slack._is_exist_channel(self, channel)
    + slack.get_channel_list(self)
    + slack.post_message_to_channel(self, channel, message)
    + slack.set_username(self, username)
