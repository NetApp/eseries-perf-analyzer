@Library('hub') _
pipeline {
    agent any
    triggers {
        cron('H H(17-20) * * *')
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    environment {
        TAG = "${BRANCH_NAME}-${BUILD_NUMBER}"
        PROJECT_NAME = "esg-grafana"
        VERSION = "1.1"
        QUIET = "yes"
        // This determines what repositories to use for building the images
        PIP_CONF = 'pip.conf.internal'
        ALPINE_REPO_FILE = 'repositories.internal'
    }
    stages {
        stage('Run docker builds') {
            steps {
                sh'''
                    # Overwrite the default environment options
                    printf "TAG=${TAG}\nPROJ_NAME=${PROJECT_NAME}\n" > .env
                    make build
                '''
                sh 'echo ${GIT_COMMIT}'
            }
        }
        stage('Security Scan'){
            steps{
                hubScan("${PROJECT_NAME}", "${VERSION}", coreCount: -1)
            }
        }
        stage('Prepare for scan'){
            steps {
                sh'''
                    make export
                '''
            }
        }
        stage('Security Scan Images'){
            when{
                // When triggered based on time or based on a user interaction
                not { triggeredBy 'SCMTrigger' }
            }
            steps {
                // Validate the images, running a security scan on all docker images
                hubScanDocker("${PROJECT_NAME}", "${VERSION}", "${WORKSPACE}/images", coreCount: -1)
            }
        }
    }
    post {
        always {
            sh'''
                make clean
            '''
            cleanWs deleteDirs: true
        }
    }
}
