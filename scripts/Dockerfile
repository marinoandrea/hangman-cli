FROM ubuntu:20.04

COPY ./hangman-cli_linux_x64 ./bin

RUN apt-get -y update
RUN apt-get -y  install python3
ENV LANG C.UTF-8
CMD ["/bin/bash"]
