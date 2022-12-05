FROM python:3.10-alpine

RUN apk add --update socat

# note: this Dockerfile is based on https://github.com/SunshineCTF/SunshineCTF-2017-Public/blob/master/Pwn/400-Notetorious/Dockerfile

# Create unprivileged unprivileged user. lol.
RUN addgroup -S unprivileged && \
	adduser -S unprivileged -G unprivileged

# start out of app, install to app.
WORKDIR /app
COPY ./key ./server-challenge-1.py /app/

# make sure the files are owned by root but visible by the unprivileged group
RUN chown root:root /app /app/key /app/server-challenge-1.py && \
	chmod 0555 /app /app/server-challenge-1.py && \
	chmod 0444 /app/key

# listens on the following port.
EXPOSE 65000/tcp
CMD socat -T 31 TCP-LISTEN:65000,fork,reuseaddr EXEC:"/app/server-challenge-1.py",su=unprivileged,pty,ctty,echo=0,stderr