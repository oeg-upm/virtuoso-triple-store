from os import system

# system('curl --digest --verbose --user dba:mysecret --url "http://localhost:8890/sparql-graph-crud-auth?graph-uri=http://localhost:8890/demo7" -T ttl_files/building_example.ttl')

import subprocess
proc = subprocess.Popen(["curl", "--digest", "--verbose" , "--user", "dba:mysecret", "--url", 'http://localhost:8890/sparql-graph-crud-auth?graph-uri=http://localhost:8890/demo21', "-T", "ttl_files/building_example.ttl"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = proc.communicate()
lastCode = str(err).split('HTTP/1.1 ')[-1].split(" ")[0]
if lastCode == "200":
    print("All OK")
elif lastCode == "201":
    print("Created Graph")
elif lastCode == "401":
    print("Error with Authorization")
else:
    print("You did something wrong")