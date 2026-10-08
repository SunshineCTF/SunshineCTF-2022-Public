# docker-compose web challenge (no PwnableHarness TARGET); this Build.mk only
# registers the check. `pwnmake check` starts it, runs the solver, and tears it down.
$(call ctf_check_web,$(DIR),22302,timely.ctf.hackucf.org,python3 solve.py)
