import os
import sys

# Audacity Boilerplate
if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")

def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response
# End of audacity and defines

volume_increase = input("Input Volume Increase (decimal, 0 -> 10 where 1 is 100%): ")
pitch_increase = input("Input Lap 3 Pitch Increase (percentage change where 0 is unchanged): ")
tempo_increase = input("Input Lap 3 Tempo Increase (percentage change where 0 is unchanged): ")
print(volume_increase + ", " + pitch_increase + ", " + tempo_increase)


directory_in_str = str(os.path.abspath(""))
print(directory_in_str)
directory = os.fsencode(directory_in_str + "\\IN")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    input_filepath = "\"" + directory_in_str + "\\IN\\" + os.fsdecode(file) + "\""
    output1_2_filepath = "\"" + directory_in_str + "\\OUT\\WAVE1_2\\" + os.fsdecode(file) + "\""
    output3_filepath = "\"" + directory_in_str + "\\OUT\\WAVE3\\" + os.fsdecode(file) + "\""
    do_command("New: ")
    do_command("Import2: Filename=" + input_filepath)
    do_command("SelectAll:")
    do_command("Amplify: Ratio=" + volume_increase)
    do_command("Export2: Filename=" + output1_2_filepath)
    do_command("ChangePitch: Percentage=" + pitch_increase)
    do_command("ChangeTempo: Percentage=" + tempo_increase)
    do_command("Export2: Filename=" + output3_filepath)


input("Press enter to exit...")