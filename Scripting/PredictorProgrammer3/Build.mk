# docker-compose TCP challenge (no PwnableHarness TARGET); this Build.mk only
# registers the check. `pwnmake check` starts it, runs the solver, and tears it down.
CHECK_TIMEOUT := 300
$(call ctf_check_tcp_slow,$(DIR),22203,python3 autosolver/solver.py --no-repeat --skip-first-sleep)
