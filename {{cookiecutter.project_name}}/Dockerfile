FROM 218546966473.dkr.ecr.us-east-1.amazonaws.com/singer-base:0.0.1
 
# The orchestrator needs all these params tap_name should be the name of
# the source without the word "tap", for example "closeio". tap_version
# should be like 1.2.3.
ENV STITCH_TAP_NAME {{cookiecutter.project_name}}
ENV STITCH_TAP_PATH tap-env/bin/${STITCH_TAP_NAME}
ARG STITCH_TAP_VERSION
ARG DOCKER_TAP_ENV=/root/venvs/$STITCH_TAP_NAME
 
# Copy the code for the tap into the image
WORKDIR /code/$STITCH_TAP_NAME
COPY LICENSE setup.py ./
COPY {{cookiecutter.package_name}}/*.py ./{{cookiecutter.package_name}}/
 
RUN python3 -m venv $DOCKER_TAP_ENV
RUN $DOCKER_TAP_ENV/bin/pip3 install --upgrade pip setuptools wheel
RUN $DOCKER_TAP_ENV/bin/pip3 install -e .
RUN ln -s $DOCKER_TAP_ENV/bin/$STITCH_TAP_NAME /usr/local/bin/

CMD [ "timeout", "--preserve-status", "--signal=SIGTERM", "6.1h", "stitch-orchestrator" ]