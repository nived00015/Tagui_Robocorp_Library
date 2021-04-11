import subprocess
import platform
import sys
import os

def code_block_to_run():
    # combine all the code in this function to your Run_Script()

    # below line is to clean up any dead tagui processes
    os.system(tagui_directory + '/src/end_processes')

    tagui_exec = 'tagui'
    tagui_cmd = tagui_exec + ' workflow.tag'
    try:
        # launch tagui using subprocess
        tagui_process = subprocess.Popen(
            tagui_cmd, shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # loop until tagui process is running
        while tagui_process.poll() is None:

            # read next line of output from tagui process
            tagui_output = tagui_process.stdout.readline()

            # for python 2 and 3 str-byte compatibility
            if sys.version_info[0] >= 3:
                tagui_output = tagui_output.decode('utf-8')

            # do what you want here with the live output
            if tagui_output.strip() != '':
                #rstrip() to remove \n char at the end
                print(tagui_output.rstrip())

        return True

    except Exception as e:
        print('[RPA][ERROR] - ' + str(e))
        return False

code_block_to_run()
