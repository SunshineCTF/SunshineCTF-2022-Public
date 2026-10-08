# docker-compose TCP challenge (no PwnableHarness TARGET); this Build.mk only
# registers the check. `pwnmake check` starts it, runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),22201,python3 autosolver/solver.py --no-repeat --skip-first-sleep)
