Port Assignments
-----

Port assignment convention:

* SunshineCTF challenges: port = `yycnn`
  * `yy` = last 2 digits of competition year, so SunshineCTF 2022 would be `22cnn`
  * `c` = category (0 = pwn, 1 = reversing, 2 = scripting, 3 = web, 4 = crypto, 5 = misc, 6 = speedrun, 7 = pegasus)
  * `nn` = challenge index in that category, starting at 00

Only challenges with a hosted, server-side component are listed. HTTP(S) web
challenges are reverse-proxied by nginx (see `nginx/`) on their subdomain;
raw-TCP challenges are reached with `nc ctf.hackucf.org <port>`.

The Pegasus (`PEG_*`, `227nn`) rows are reserved and managed separately by the
Pegasus deployment (the `Pegasus/` submodule is out of scope here).

| Challenge Name | Category | Author | Directory | Host | Port | Connection |
|----------------|----------|--------|-----------|------|-----:|------------|
| CTF Simulator | Pwn | kcolley | Pwn/CTFSim | ctf.hackucf.org | 22000 | `nc ctf.hackucf.org 22000` |
| ChessFEN | Pwn | kcolley | Pwn/ChessFEN | ctf.hackucf.org | 22001 | `nc ctf.hackucf.org 22001` |
| [RII] MagicTheGatheRIIng | Pwn | crandyman | Pwn/RII-MagicTheGatheRIIng | ctf.hackucf.org | 22002 | `nc ctf.hackucf.org 22002` |
| [RII] EldenRIIngLite | Pwn | Z1pburg3r | Pwn/RII-EldenRIIngLite | ctf.hackucf.org | 22003 | `nc ctf.hackucf.org 22003` |
| Predictor Programmer 1 | Scripting | solarbonite | Scripting/PredictorProgrammer1 | ctf.hackucf.org | 22201 | `nc ctf.hackucf.org 22201` |
| Predictor Programmer 2 | Scripting | solarbonite | Scripting/PredictorProgrammer2 | ctf.hackucf.org | 22202 | `nc ctf.hackucf.org 22202` |
| Predictor Programmer 3 | Scripting | solarbonite | Scripting/PredictorProgrammer3 | ctf.hackucf.org | 22203 | `nc ctf.hackucf.org 22203` |
| Inspect Element | Web | solarbonite | Web/inspect-element | inspect-element.ctf.hackucf.org | 22300 | https://inspect-element.ctf.hackucf.org |
| Network Pong | Web | solarbonite | Web/network-pong | network-pong.ctf.hackucf.org | 22301 | https://network-pong.ctf.hackucf.org |
| Timely | Web | Helithumper | Web/timely | timely.ctf.hackucf.org | 22302 | https://timely.ctf.hackucf.org |
| PEG_DEBUG | Pegasus | kcolley | Pegasus | ctf.hackucf.org | 22700-22702 | managed separately |
| PEG_AUTOREV | Pegasus | kcolley | Pegasus | ctf.hackucf.org | 22703 | managed separately |
| PEG_CHEAT | Pegasus | kcolley | Pegasus | ctf.hackucf.org | 22704 | managed separately |
| PEG_AUTOREV 2 | Pegasus | kcolley | Pegasus | ctf.hackucf.org | 22705 | managed separately |

Not hosted here (no reproducible server-side component):

* `Web/listy` — serverless GCP challenge (Cloud Function + Storage buckets + a
  dev service-account key leaked in an external public git repo's history). The
  flag lives in a GCP bucket and cannot be reproduced on a single archive host.
* `Pwn/RET2-Snake` — played on the external RET2 Systems wargames platform.
* `Web/transparent` — the flag lives in the Certificate Transparency logs for a
  SunshineCTF subdomain; nothing to run.
* `Reversing/NewGameOnline` — downloadable reversing challenge (builds with
  pwnmake, solvable), no server.
