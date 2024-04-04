#!/usr/bin/python3
"""This Fabric script generates a .tgz archive from the
contents of the web_static folder of my AirBnB Clone repo,
using the function do_pack.
It also distributes an archive to my web
servers, using the function do_deploy.
It also creates and distributes an archive to my web servers,"""
from fabric.api import local
from fabric.api import env
from fabric.api import put
from fabric.api import run
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["54.87.250.235", "18.204.11.190"]
env.key_filename = "~/.ssh/school"


def do_pack():
    """Generates a .tgz archive"""
    try:
        local("mkdir -p versions")
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        file = "versions/web_static_{}.tgz".format(time)
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to my web servers"""
    if not archive_path:
        return False
    try:
        put(archive_path, "/tmp/")
        file = archive_path.split("/")[-1]
        folder = "/data/web_static/releases/{}".format(file[:-4])
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}/".format(file, folder))
        run("rm /tmp/{}".format(file))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        return True
    except Exception:
        return False


def deploy():
    """Creates an archive and deploys it"""
    if not hasattr(env, 'archive_exists'):
        env.archive_exists = True
        archive = do_pack()
        if archive is None:
            return False
        env.archive_path = archive
    return do_deploy(env.archive_path)
