#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in docker-compose.yml to pick a Python version: 3, 3.8, 3.7, 3.6 
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED 1

# This image includes a non-root user with sudo access. Use the "remoteUser" 
# property in devcontainer.json to use it. On Linux, update the values below 
# or in docker-compose.yml to ensure the container user's UID/GID matches your
# local values. See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Update UID/GID if needed
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then \
    groupmod --gid $USER_GID $USERNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chmod -R $USER_UID:$USER_GID /home/$USERNAME; \
    fi

# change ls colors for root
RUN export SNIPPET="\nexport LS_OPTIONS='--color=auto'\neval \"\`dircolors\`\"\nalias ls='ls \$LS_OPTIONS'\nalias ll='ls \$LS_OPTIONS -l'\nalias l='ls \$LS_OPTIONS -lA'\n" \
    && echo "$SNIPPET" | tee -a ~/.bashrc \
    && echo "$SNIPPET" | tee -a ~/.zshrc

# Allow the vscode user to pip install globally w/o sudo
# ENV PIP_TARGET=/usr/local/pip-global
# ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
# ENV PATH=${PIP_TARGET}/bin:${PATH}
# RUN mkdir -p ${PIP_TARGET} \
#     && chown root ${PIP_TARGET} \
#     && export SNIPPET="if [ \"\$(stat -c '%U' ${PIP_TARGET})\" != \"vscode\" ]; then chown -R root ${PIP_TARGET}; fi" \
#     && echo "$SNIPPET" | tee -a /root/.bashrc \
#     && echo "$SNIPPET" | tee -a /root/.zshrc

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
#
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# ** [Optional] Uncomment this section to install additional packages. **
#
# RUN apt-get update \
#     && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>



