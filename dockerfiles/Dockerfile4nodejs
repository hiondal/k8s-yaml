FROM node:slim

ARG MAIN_APP
ENV APPNAME ${MAIN_APP}
ENV USERNAME docker  
ENV ARTIFACTORY_HOME /home/${USERNAME}

# DON'T change USERNAME
# Add a docker user, make work dir
RUN adduser --disabled-password --gecos "" ${USERNAME} && \
  echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
  mkdir -p ${ARTIFACTORY_HOME} && \
  chown ${USERNAME}:${USERNAME} ${ARTIFACTORY_HOME}

WORKDIR ${ARTIFACTORY_HOME}

COPY . ./

RUN npm install

# RUN as docker user
USER ${USERNAME}
CMD node ${APPNAME}


