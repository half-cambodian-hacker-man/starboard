import subprocess

from starboard.env import STARBOARD_STATIC, STARBOARD_DATABASE

def rebuild_site():
  subprocess.Popen(["./rebuild.sh"], env={
    "STARBOARD_STATIC": STARBOARD_STATIC,
    "STARBOARD_DATABASE": STARBOARD_DATABASE
  })
