# Custom Jenkins Docker Image for Laser CI Integration
FROM jenkins/jenkins:lts

USER root

# Install packages
RUN apt-get update -qq && \
    apt-get install -y -qq \
        curl unzip git python3 python3-pip jq xmlstarlet ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --break-system-packages --quiet pytest pytest-html

# --- SSL FIX ---
COPY certs/ /usr/local/share/ca-certificates/
RUN update-ca-certificates && \
    for cert in /usr/local/share/ca-certificates/*.crt; do \
        alias=$(basename "$cert" .crt); \
        keytool -import -trustcacerts \
            -keystore "$JAVA_HOME/lib/security/cacerts" \
            -storepass changeit -noprompt \
            -alias "$alias" \
            -file "$cert" 2>/dev/null || true; \
    done

# --- CONFIGURATION AS CODE FIX ---
# Move CasC to the 'ref' (reference) directory to avoid Volume overwrites
RUN mkdir -p /usr/share/jenkins/ref/casc_configs
COPY docker/jenkins/casc.yaml /usr/share/jenkins/ref/casc_configs/jenkins.yaml
RUN chown -R jenkins:jenkins /usr/share/jenkins/ref/casc_configs

# Set the environment variable to the REF path
ENV CASC_JENKINS_CONFIG=/usr/share/jenkins/ref/casc_configs/jenkins.yaml

# --- JOB & SCRIPT SETUP ---
RUN mkdir -p /usr/share/jenkins/ref/jobs/laser-integration-tests
COPY docker/jenkins/jenkins-job-config.xml /usr/share/jenkins/ref/jobs/laser-integration-tests/config.xml
COPY . /tmp/laser_ci/

# Jenkins Init Scripts
RUN mkdir -p /usr/share/jenkins/ref/init.groovy.d
COPY docker/jenkins/init.groovy /usr/share/jenkins/ref/init.groovy.d/

# Set environment variables for Jenkins
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Entrypoint
COPY docker/jenkins/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r//' /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

USER jenkins

# Install required plugins
RUN jenkins-plugin-cli --plugins \
    workflow-aggregator \
    git \
    pipeline-stage-view \
    htmlpublisher \
    junit \
    configuration-as-code \
    ws-cleanup \
    allure-jenkins-plugin

EXPOSE 8080 50000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=5 \
    CMD curl -f http://localhost:8080/login || exit 1