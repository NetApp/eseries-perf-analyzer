pipeline {
    agent { label 'linux-docker' }
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(artifactNumToKeepStr: '5', numToKeepStr: '20'))
    }
    environment {
        TAG = "${BRANCH_NAME}-${BUILD_NUMBER}"
        PROJECT_NAME = "esg-grafana"
        VERSION = "3.0"
        QUIET = "yes"
    }
    stages {
        stage('Run docker builds') {
            steps {
                sh'''
                    # Overwrite the default environment options
                    sed --in-place \
                        -e "s/^TAG=.*/TAG=${TAG}/" \
                        -e "s/^PROJ_NAME=.*/PROJ_NAME=${PROJECT_NAME}/" \
                        .env
                    cat .env
                    make build
                '''
                sh 'echo ${GIT_COMMIT}'
            }
        }
        stage('Run python unit tests') {
            steps {
                sh'''
                    # Overwrite the default environment options
                    sed --in-place \
                        -e "s/^TAG=.*/TAG=${TAG}/" \
                        -e "s/^PROJ_NAME=.*/PROJ_NAME=${PROJECT_NAME}/" \
                        .env
                    ./plugins/eseries_monitoring/collector/tests/initiate_testing.sh ${PROJECT_NAME} ${TAG}
                '''
            }
        }
    }
    post {
        always {
            sh'''
                make clean || true
            '''
            cleanWs deleteDirs: true
        }
    }
}
