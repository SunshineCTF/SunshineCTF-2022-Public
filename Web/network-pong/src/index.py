#!/usr/local/bin/python3
# Web server
from flask import Flask, render_template, request, Response, redirect
import uuid, subprocess, os, signal

app = Flask(__name__)


@app.route('/')
def index():
    try:
        ip = request.args['ip']
        # sanitize ip, because this is unhackable.
        if ip.find(" ") != -1:
            return render_template('index.html', res="Error: Please only enter the IP or domain!")
        elif ip.find("cat") != -1 or ip.find("head") != -1 or ip.find("tail") != -1:
            return render_template('index.html', res="Error: Do not mention body parts, felines, or body parts of felines.")

    except:
        return render_template('index.html')

    pid=-1
    try:
        os.nice(20)
        cmd = subprocess.Popen("{ping,-c,1," + ip + "}",
            shell=True,
            executable='/bin/bash',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True,
            process_group=0)
        pid = cmd.pid
        try:
            output = cmd.communicate(timeout=5)[0].decode('utf-8')
        except subprocess.TimeoutExpired:
            # kill the process now that we read the output, in case they fork bombed
            os.killpg(pid, signal.SIGABRT)
            output = cmd.communicate()[0].decode('utf-8')
    except Exception as e:
        # clean up the group with a good old fashioned abort
        if pid != -1:
            os.killpg(pid, signal.SIGABRT)
        return render_template('index.html', res=("Timed out: " + e.message))

    return render_template('index.html', res=output)

def create_app():
    return app
