#!/bin/bash
# Automated Jenkins Setup for Laser CI
# This script sets up Jenkins automatically and updates GitLab CI variables

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
DOCKER_COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running or not accessible"
        exit 1
    fi
    log_success "Docker is running"
}

# Start Jenkins with custom image
start_jenkins() {
    log_info "Starting Jenkins with custom image..."

    cd "$PROJECT_ROOT"
    docker-compose up -d jenkins-custom

    log_success "Jenkins started"
}

# Wait for Jenkins to be ready
wait_for_jenkins() {
    local max_attempts=60
    local attempt=1

    log_info "Waiting for Jenkins to be ready..."

    while [ $attempt -le $max_attempts ]; do
        if docker exec jenkins-custom curl -f http://localhost:8080/login >/dev/null 2>&1; then
            log_success "Jenkins is ready!"
            return 0
        fi

        echo -n "."
        sleep 5
        ((attempt++))
    done

    log_error "Jenkins failed to start within $(($max_attempts * 5)) seconds"
    exit 1
}

# Get API token from Jenkins container
get_api_token() {
    log_info "Retrieving API token from Jenkins..."

    local token_file="/var/jenkins_home/api-token.txt"

    # Wait a bit for the token file to be created
    sleep 10

    if ! docker exec jenkins-custom test -f "$token_file"; then
        log_error "API token file not found in Jenkins container"
        log_info "Jenkins logs:"
        docker logs jenkins-custom | tail -20
        exit 1
    fi

    JENKINS_API_TOKEN=$(docker exec jenkins-custom cat "$token_file")
    log_success "Retrieved Jenkins API token: ${JENKINS_API_TOKEN:0:8}..."
}

# Update GitLab CI configuration
update_gitlab_ci() {
    local gitlab_ci_file="$PROJECT_ROOT/pipelines/.gitlab-ci-simplified.yml"

    log_info "Updating GitLab CI configuration..."

    # Create backup
    cp "$gitlab_ci_file" "${gitlab_ci_file}.backup.$(date +%Y%m%d_%H%M%S)"

    # Update the API token in the YAML file
    sed -i "s/JENKINS_API_TOKEN: .*/JENKINS_API_TOKEN: \"$JENKINS_API_TOKEN\"/" "$gitlab_ci_file"

    log_success "Updated GitLab CI configuration with real API token"
}

# Test the setup
test_setup() {
    log_info "Testing Jenkins setup..."

    # Test Jenkins connection
    if ! docker exec jenkins-custom curl -u "admin:$JENKINS_API_TOKEN" http://localhost:8080/api/json >/dev/null 2>&1; then
        log_error "Jenkins API test failed"
        exit 1
    fi

    # Test job exists
    if ! docker exec jenkins-custom curl -u "admin:$JENKINS_API_TOKEN" http://localhost:8080/job/laser-integration-tests/api/json >/dev/null 2>&1; then
        log_error "Jenkins job test failed"
        exit 1
    fi

    log_success "Jenkins setup tests passed!"
}

# Show usage information
show_usage() {
    echo "Automated Jenkins Setup for Laser CI"
    echo ""
    echo "This script automatically:"
    echo "1. Builds and starts a custom Jenkins Docker image"
    echo "2. Configures Jenkins with the laser-integration-tests job"
    echo "3. Retrieves the API token from Jenkins"
    echo "4. Updates GitLab CI configuration with the real token"
    echo "5. Tests the setup"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  --gitlab-token TOKEN Set GitLab access token for CI updates"
    echo "  --skip-gitlab-update Skip GitLab CI configuration update"
    echo ""
    echo "Environment Variables:"
    echo "  GITLAB_ACCESS_TOKEN  GitLab token for API access"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --gitlab-token glpat-xxxxx"
}

# Main function
main() {
    local skip_gitlab_update=false
    local gitlab_token=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            --gitlab-token)
                gitlab_token="$2"
                shift 2
                ;;
            --skip-gitlab-update)
                skip_gitlab_update=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    echo
    echo "=========================================="
    echo "  Automated Jenkins Setup for Laser CI"
    echo "=========================================="
    echo

    # Check prerequisites
    check_docker

    # Start Jenkins
    start_jenkins

    # Wait for Jenkins to be ready
    wait_for_jenkins

    # Get API token
    get_api_token

    # Update GitLab CI if not skipped
    if [ "$skip_gitlab_update" = false ]; then
        update_gitlab_ci
    fi

    # Test setup
    test_setup

    echo
    log_success "Automated Jenkins setup completed successfully!"
    echo
    echo "Jenkins Details:"
    echo "  URL: http://localhost:8080"
    echo "  User: admin"
    echo "  API Token: ${JENKINS_API_TOKEN:0:8}..."
    echo "  Job: laser-integration-tests"
    echo
    echo "Next steps:"
    echo "1. Access Jenkins at: http://localhost:8080"
    echo "2. Push to GitLab to trigger pipeline"
    echo "3. Monitor results in both GitLab and Jenkins"
    echo
    if [ "$skip_gitlab_update" = false ]; then
        echo "GitLab CI configuration has been updated with the real API token."
        echo "You can now run pipelines without manual token configuration!"
    fi
    echo
}

# Run main function
main "$@"
