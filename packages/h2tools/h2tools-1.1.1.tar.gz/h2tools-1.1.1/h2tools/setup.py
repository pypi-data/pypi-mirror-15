def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('h2tools', parent_package, top_path) 
    config.add_subpackage('collections')
    return config
    


if __name__ == '__main__':
    print('This is the wrong setup.py to run')
