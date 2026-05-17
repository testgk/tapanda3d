# 🚀 Jenkins-GitLab Manual Setup Reference (No Scripts)

## Quick Setup Commands

### 1. Start Jenkins
```bash
cd runner
docker-compose up -d jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 2. Configure Jenkins Web UI
- Open: http://localhost:8080
- Enter admin password
- Install suggested plugins
- Create admin user
- Get API token from user settings

### 3. Create Jenkins Job
- New Item → "laser-integration-tests" → Pipeline
- Description: "Laser CI integration tests triggered from GitLab"
- Build Triggers: Check "Trigger builds remotely", Token: "laser-ci-token"
- Pipeline Script: Copy the script from below

### 4. Jenkins Pipeline Script
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout tests') {
            steps {
                sh '''
                    git clone --depth 1 https://gitlab.com/aqualaser/laser_ci.git laser_ci_src
                    cp -r laser_ci_src/tests .
                    cp -r laser_ci_src/scripts .
                '''
            }
        }

        stage('Download artifacts') {
            steps {
                sh '''
                    curl --fail -L \\
                         --header "PRIVATE-TOKEN: ${GITLAB_ACCESS_TOKEN}" \\
                         --output artifacts.zip \\
                         "${GITLAB_ARTIFACT_URL}"
                    unzip -q artifacts.zip
                '''
            }
        }

        stage('Run integration tests') {
            steps {
                sh '''
                    python3 -m pip install pytest --quiet
                    python3 tests/integration/run_tests.py
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'tests/integration/results/integration-results.xml'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Integration tests passed — GitLab pipeline can proceed to deploy.'
        }
        failure {
            echo 'Integration tests FAILED — GitLab pipeline will be blocked.'
        }
    }
}
```

### 5. GitLab CI/CD Variables
In GitLab project Settings → CI/CD → Variables:

| Variable | Value | Protected | Masked |
|----------|-------|-----------|--------|
| JENKINS_URL | http://jenkins:8080 | ✅ | ❌ |
| JENKINS_USER | admin | ✅ | ❌ |
| JENKINS_API_TOKEN | [your-token] | ✅ | ✅ |
| GITLAB_ACCESS_TOKEN | [gitlab-token] | ✅ | ✅ |
| JENKINS_JOB_NAME | laser-integration-tests | ❌ | ❌ |

### 6. Test Commands
```bash
# Test Jenkins connection
curl http://localhost:8080/api/json

# Test authentication
curl -u "admin:[token]" http://localhost:8080/api/json

# Test job exists
curl -u "admin:[token]" http://localhost:8080/job/laser-integration-tests/api/json

# Test GitLab token
curl --header "PRIVATE-TOKEN: [token]" "https://gitlab.com/api/v4/user"

# Trigger pipeline
git push origin main
```

### 7. Monitor Commands
```bash
# Check containers
docker ps

# Check Jenkins logs
docker logs jenkins

# Restart Jenkins
docker restart jenkins
```

## Synchronization Flow

1. **GitLab builds** components and creates artifacts
2. **GitLab triggers** Jenkins with artifact URL + metadata
3. **Jenkins downloads** artifacts from GitLab
4. **Jenkins runs** integration tests
5. **Jenkins reports** results back to GitLab pipeline

## Key URLs

- **Jenkins**: http://localhost:8080
- **Jenkins Job**: http://localhost:8080/job/laser-integration-tests/
- **GitLab Pipelines**: https://gitlab.com/aqualaser/laser_ci/-/pipelines

## Troubleshooting

### Jenkins Issues
```bash
# Check if running
docker ps | grep jenkins

# Check logs
docker logs jenkins

# Restart
docker restart jenkins
```

### Connection Issues
```bash
# Test Jenkins API
curl http://localhost:8080/api/json

# Test with auth
curl -u "admin:token" http://localhost:8080/api/json
```

### GitLab Issues
```bash
# Test GitLab token
curl --header "PRIVATE-TOKEN: token" "https://gitlab.com/api/v4/user"
```

---

**Manual Setup Complete - No Scripts Required!** 🎉
