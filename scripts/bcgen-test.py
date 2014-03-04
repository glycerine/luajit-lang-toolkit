import os
import re
import subprocess

test_dir = "tests"
luajit_exec = "luajit"

for dirpath, dirnames, filenames in os.walk(test_dir):
    for filename in filenames:
        m = re.match(r'([^.]+)\.lua$', filename)
        if m:
            fullname = os.path.join(dirpath, filename)
            test_name = m.group(1)
            out_tst = None
            run_error = False
            try:
                out_tst = subprocess.check_output([luajit_exec, "run.lua", fullname])
            except subprocess.CalledProcessError:
                run_error = True
            out_ref = subprocess.check_output([luajit_exec, fullname])
            led, msg = None, None
            if run_error:
                led, msg = "*", "fail to run"
            elif out_tst == out_ref:
                if out_tst in ["", "\n", "\r\n"] or not out_tst:
                    led, msg = "-", "pass / no output"
                else:
                    led, msg = " ", "pass"
            else:
                led, msg = "*", "fail"
                log = open("tests/log/%s.output.diff" % test_name, "w")
                log.write("*** reference ***\n%s\n" % out_ref)
                log.write("*** test program ***\n%s\n" % out_tst)
                log.close()

            print("%s %-24s %s" % (led, test_name, msg))
