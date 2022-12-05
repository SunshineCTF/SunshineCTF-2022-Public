FROM c0deh4cker/pwnableharness:20.04

ARG DIR
COPY $DIR/pwnableserver /usr/local/bin/pwnableserver
COPY $DIR/libpwnableharness64.so /usr/local/lib/libpwnableharness64.so

WORKDIR /home/EldenRIIngLite
COPY $DIR/ld-2.31.so ./

RUN ln -s /ctf/flag.txt flag.txt
