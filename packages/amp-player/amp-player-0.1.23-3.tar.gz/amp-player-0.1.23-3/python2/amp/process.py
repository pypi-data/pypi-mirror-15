from __future__ import absolute_import
import psutil
import signal

def kill_process_tree(parent_pid):
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()

def toggle_process_tree(parent_pid):
    try:
        parent = psutil.Process(parent_pid)
    except: return
    if parent.status() == psutil.STATUS_STOPPED:
        for child in parent.children(recursive=True):
            child.resume()
        parent.resume()
        print u"Playback resumed."

    else:
        for child in parent.children(recursive=True):
            child.suspend()
        parent.suspend()
        print u"Playback paused. Type 'amp' again to resume."
