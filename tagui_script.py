# -*- coding: utf-8 -*-
# +
#AUTHOR :  NIVED N , Ken Soh
# -

import re
import os
import platform
import subprocess
import sys
from RPA.core.notebook import notebook_print as np

def _python2_env():
    """function to check python version for compatibility handling"""
    if sys.version_info[0] < 3: return True
    else: return False

def _python3_env():
    """function to check python version for compatibility handling"""
    return not _python2_env()

def _patch_macos_pjs():
    """patch PhantomJS to latest v2.1.1 that plays well with new macOS versions"""
    if platform.system() == 'Darwin' and not os.path.isdir(os.path.expanduser('~') + '/.tagui/src/phantomjs_old'):
        original_directory = os.getcwd(); os.chdir(os.path.expanduser('~') + '/.tagui/src')
        np('[RPA][INFO] - downloading latest PhantomJS to fix OpenSSL issue')
        download('https://github.com/tebelorg/Tump/releases/download/v1.0.0/phantomjs-2.1.1-macosx.zip', 'phantomjs.zip')
        if not os.path.isfile('phantomjs.zip'):
            np('[RPA][ERROR] - unable to download latest PhantomJS v2.1.1')
            os.chdir(original_directory); return False
        unzip('phantomjs.zip'); os.rename('phantomjs', 'phantomjs_old'); os.rename('phantomjs-2.1.1-macosx', 'phantomjs')
        if os.path.isfile('phantomjs.zip'): os.remove('phantomjs.zip')
        os.system('chmod -R 755 phantomjs > /dev/null 2>&1')
        os.chdir(original_directory); return True
    else:
        return True

def download(download_url = None, filename_to_save = None):
    """function for python 2/3 compatible file download from url"""

    if download_url is None or download_url == '':
        np('[RPA][ERROR] - download URL missing for download()')
        return False

    # if not given, use last part of url as filename to save
    if filename_to_save is None or filename_to_save == '':
        download_url_tokens = download_url.split('/')
        filename_to_save = download_url_tokens[-1]

    # delete existing file if exist to ensure freshness
    if os.path.isfile(filename_to_save):
        os.remove(filename_to_save)

    # handle case where url is invalid or has no content
    try:
        if _python2_env():
            import urllib; urllib.urlretrieve(download_url, filename_to_save)
        else:
            import urllib.request; urllib.request.urlretrieve(download_url, filename_to_save)

    except Exception as e:
        np('[RPA][ERROR] - failed downloading from ' + download_url + '...')
        np(str(e))
        return False

    # take the existence of downloaded file as success
    if os.path.isfile(filename_to_save):
        return True

    else:
        np('[RPA][ERROR] - failed downloading to ' + filename_to_save)
        return False

def unzip(file_to_unzip = None, unzip_location = None):
    """function to unzip zip file to specified location"""
    import zipfile

    if file_to_unzip is None or file_to_unzip == '':
        np('[RPA][ERROR] - filename missing for unzip()')
        return False
    elif not os.path.isfile(file_to_unzip):
        np('[RPA][ERROR] - file specified missing for unzip()')
        return False

    zip_file = zipfile.ZipFile(file_to_unzip, 'r')

    if unzip_location is None or unzip_location == '':
        zip_file.extractall()
    else:
        zip_file.extractall(unzip_location)

    zip_file.close()
    return True

def setup():
    """function to setup TagUI to user home folder on Linux / macOS / Windows"""

    # get user home folder location to setup tagui
    if platform.system() == 'Windows':
        home_directory = os.environ['APPDATA']
    else:
        home_directory = os.path.expanduser('~')

    np('[RPA][INFO] - setting up TagUI for use in your Python environment')

    # special check for macOS - download() will fail due to no SSL certs for Python 3
    if platform.system() == 'Darwin' and _python3_env():
        if os.system('/Applications/Python\ 3.9/Install\ Certificates.command > /dev/null 2>&1') != 0:
            if os.system('/Applications/Python\ 3.8/Install\ Certificates.command > /dev/null 2>&1') != 0:
                if os.system('/Applications/Python\ 3.7/Install\ Certificates.command > /dev/null 2>&1') != 0:
                    os.system('/Applications/Python\ 3.6/Install\ Certificates.command > /dev/null 2>&1')

    # set tagui zip filename for respective operating systems
    if platform.system() == 'Linux': tagui_zip_file = 'TagUI_Linux.zip'
    elif platform.system() == 'Darwin': tagui_zip_file = 'TagUI_macOS.zip'
    elif platform.system() == 'Windows': tagui_zip_file = 'TagUI_Windows.zip'
    else:
        np('[RPA][ERROR] - unknown ' + platform.system() + ' operating system to setup TagUI')
        return False
    
    if not os.path.isfile('rpa_python.zip'):
        # primary installation pathway by downloading from internet, requiring internet access
        np('[RPA][INFO] - downloading TagUI (~200MB) and unzipping to below folder...')
        np('[RPA][INFO] - ' + home_directory)

        # set tagui zip download url and download zip for respective operating systems
        tagui_zip_url = 'https://github.com/kelaberetiv/TagUI/releases/download/v6.14.0/' + tagui_zip_file 
        if not download(tagui_zip_url, home_directory + '/' + tagui_zip_file):
            # error message is shown by download(), no need for message here 
            return False

        # unzip downloaded zip file to user home folder
        unzip(home_directory + '/' + tagui_zip_file, home_directory)
        if not os.path.isfile(home_directory + '/' + 'tagui' + '/' + 'src' + '/' + 'tagui'):
            np('[RPA][ERROR] - unable to unzip TagUI to ' + home_directory)
            return False

    else:
        # secondary installation pathway by using the rpa_python.zip generated from pack()
        np('[RPA][INFO] - unzipping TagUI (~200MB) from rpa_python.zip to below folder...')
        np('[RPA][INFO] - ' + home_directory)

        import shutil
        shutil.move('rpa_python.zip', home_directory + '/' + tagui_zip_file)

        if not os.path.isdir(home_directory + '/tagui'): os.mkdir(home_directory + '/tagui')
        unzip(home_directory + '/' + tagui_zip_file, home_directory + '/tagui')
        if not os.path.isfile(home_directory + '/' + 'tagui' + '/' + 'src' + '/' + 'tagui'):
            np('[RPA][ERROR] - unable to unzip TagUI to ' + home_directory)
            return False

    # set correct tagui folder for different operating systems
    if platform.system() == 'Windows':
        tagui_directory = home_directory + '/' + 'tagui'
    else:
        tagui_directory = home_directory + '/' + '.tagui'

        # overwrite tagui to .tagui folder for Linux / macOS

        # first rename existing .tagui folder to .tagui_previous 
        if os.path.isdir(tagui_directory):
            os.rename(tagui_directory, tagui_directory + '_previous')

        # next rename extracted tagui folder (verified earlier) to .tagui
        os.rename(home_directory + '/' + 'tagui', tagui_directory)

        # finally remove .tagui_previous folder if it exists
        if os.path.isdir(tagui_directory + '_previous'):
            import shutil
            shutil.rmtree(tagui_directory + '_previous')

    # after unzip, remove downloaded zip file to save disk space 
    if os.path.isfile(home_directory + '/' + tagui_zip_file):
        os.remove(home_directory + '/' + tagui_zip_file)

    # download stable delta files from tagui cutting edge version
    # np('[RPA][INFO] - done. syncing TagUI with stable cutting edge version')
    # if not _tagui_delta(tagui_directory): return False

    # perform Linux specific setup actions
    if platform.system() == 'Linux':
        # zipfile extractall does not preserve execute permissions
        # invoking chmod to set all files with execute permissions
        # and update delta tagui/src/tagui with execute permission
        if os.system('chmod -R 755 ' + tagui_directory + ' > /dev/null 2>&1') != 0:
            np('[RPA][ERROR] - unable to set permissions for .tagui folder')
            return False 

        # check that php, a dependency for tagui, is installed and working
        if os.system('php --version > /dev/null 2>&1') != 0:
            np('[RPA][INFO] - PHP is not installed by default on your Linux distribution')
            np('[RPA][INFO] - google how to install PHP (eg for Ubuntu, apt-get install php)')
            np('[RPA][INFO] - after that, TagUI ready for use in your Python environment')
            np('[RPA][INFO] - visual automation (optional) requires special setup on Linux,')
            np('[RPA][INFO] - see the link below to install OpenCV and Tesseract libraries')
            np('[RPA][INFO] - https://sikulix-2014.readthedocs.io/en/latest/newslinux.html')
            return False

        else:
            np('[RPA][INFO] - TagUI now ready for use in your Python environment')
            np('[RPA][INFO] - visual automation (optional) requires special setup on Linux,')
            np('[RPA][INFO] - see the link below to install OpenCV and Tesseract libraries')
            np('[RPA][INFO] - https://sikulix-2014.readthedocs.io/en/latest/newslinux.html')

    # perform macOS specific setup actions
    if platform.system() == 'Darwin':
        # zipfile extractall does not preserve execute permissions
        # invoking chmod to set all files with execute permissions
        # and update delta tagui/src/tagui with execute permission
        if os.system('chmod -R 755 ' + tagui_directory + ' > /dev/null 2>&1') != 0:
            np('[RPA][ERROR] - unable to set permissions for .tagui folder')
            return False

        # patch PhantomJS to solve OpenSSL issue
        if not _patch_macos_pjs(): return False
        np('[RPA][INFO] - TagUI now ready for use in your Python environment')

    # perform Windows specific setup actions
    if platform.system() == 'Windows':
        # check that tagui packaged php is working, it has dependency on MSVCR110.dll
        if os.system(tagui_directory + '/' + 'src' + '/' + 'php/php.exe -v > nul 2>&1') != 0:
            np('[RPA][INFO] - now installing missing Visual C++ Redistributable dependency')

            # download from hosted setup file, if not already present when deployed using pack()
            if not os.path.isfile(tagui_directory + '/vcredist_x86.exe'):
                vcredist_x86_url = 'https://raw.githubusercontent.com/tebelorg/Tump/master/vcredist_x86.exe'
                if not download(vcredist_x86_url, tagui_directory + '/vcredist_x86.exe'):
                    return False

            # run setup to install the MSVCR110.dll dependency (user action required)
            os.system(tagui_directory + '/vcredist_x86.exe')
                
            # check again if tagui packaged php is working, after installing vcredist_x86.exe
            if os.system(tagui_directory + '/' + 'src' + '/' + 'php/php.exe -v > nul 2>&1') != 0:
                np('[RPA][INFO] - MSVCR110.dll is still missing, install vcredist_x86.exe from')
                np('[RPA][INFO] - the vcredist_x86.exe file in ' + home_directory + '\\tagui or from')
                np('[RPA][INFO] - https://www.microsoft.com/en-us/download/details.aspx?id=30679')
                np('[RPA][INFO] - after that, TagUI ready for use in your Python environment')
                return False

            else:
                np('[RPA][INFO] - TagUI now ready for use in your Python environment')

        else:
            np('[RPA][INFO] - TagUI now ready for use in your Python environment')

    return True

def Run_Script(language, *kwargs):
    ### Here we are doing the initialisation [installation and variable intialise]

    # get user home folder location to locate tagui executable
    if platform.system() == 'Windows':
        tagui_directory = os.environ['APPDATA'] + '/' + 'tagui'
    else:
        tagui_directory = os.path.expanduser('~') + '/' + '.tagui'

    tagui_executable = tagui_directory + '/' + 'src' + '/' + 'tagui'
    end_processes_executable = tagui_directory + '/' + 'src' + '/' + 'end_processes'

    # if tagui executable is not found, initiate setup() to install tagui
    if not os.path.isfile(tagui_executable):
        if not setup():
            # error message is shown by setup(), no need for message here
            return False

    # sync tagui delta files for current release if needed
    # if not _tagui_delta(tagui_directory): return False

    # on macOS, patch PhantomJS to latest v2.1.1 to solve OpenSSL issue
    if platform.system() == 'Darwin' and not _patch_macos_pjs(): return False

    # on Windows, check if there is space in folder path name
    if platform.system() == 'Windows' and ' ' in os.getcwd():
        np('[RPA][INFO] - to use TagUI on Windows, avoid space in folder path name')
        return False

    ## remove workflow.tag if it is available
    if os.path.isfile('workflow.tag'):
        os.remove('workflow.tag')

    ## change the language settings for TagUI
    tagui_config_file = tagui_directory + '/' + 'src' + '/' + 'tagui_config.txt'
    f = open(tagui_config_file,'r')
    data = f.read()
    f.close()

    data = re.sub("(?<=var tagui_language\s\S\s\S).*(?=';)",language,data)
    f = open(tagui_config_file,'w')
    f.write(data)
    f.close()
    
    #creating new file [workflow.tag] for writing the automation scripts
    f = open('workflow.tag','w')
    f.write("\n".join(kwargs))
    f.close()

    # entry shell command to invoke tagui process
    tagui_cmd = tagui_executable + ' workflow.tag -quiet'
    
    # run tagui end processes script to flush dead processes
    # for eg execution ended with ctrl+c or forget to close()
    os.system(end_processes_executable)

    run_output = []
    try:
        # launch tagui using subprocess
        tagui_process = subprocess.Popen(
            tagui_cmd, shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # loop until tagui process has ended
        while tagui_process.poll() is None:

            # read next line of output from tagui process
            tagui_output = tagui_process.stdout.readline()

            # for python 2 and 3 str-byte compatibility handling
            if _python3_env():
                tagui_output = tagui_output.decode('utf-8')

            # do what is needed here with the live output
            if tagui_output.strip() != '':

                if tagui_output.startswith('ERROR -'):
                    raise Exception(tagui_output)

                else:
                    # rstrip() to remove ending \n char
                    np(tagui_output.rstrip())
                    run_output.append(tagui_output.rstrip())

    except Exception as e:
        raise Exception('[RPA][ERROR] - ' + str(e))

    return run_output
