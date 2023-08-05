from fftool import (
    OS_CONFIG as env,
    Log,
    local
)


def launch_firefox(profile_path, channel):
    """relies on the other functions (download, install, profile)
    having completed.
    """

    FIREFOX_APP_BIN = env.get(channel, 'PATH_FIREFOX_BIN_ENV')

    Log.header('LAUNCH FIREFOX')
    print("Launching Firefox {0} with profile: {1}".format(
        channel,
        profile_path)
    )

    cmd = '"{0}" -profile "{1}"'.format(FIREFOX_APP_BIN, profile_path)
    print('CMD: ' + cmd)
    local(cmd)
