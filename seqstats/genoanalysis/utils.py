def is_gzipped(filename):
    return filename.endswith('.gz')

def check_executable(cmd):
    import shutil
    return shutil.which(cmd) is not None
