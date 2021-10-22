// @Library('hub') _
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
        VERSION = "2.1"
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
        // stage('Security Scan'){
        //     when {
        //         anyOf { branch '1.0'; branch '2.0'; branch '2.1'; changelog '.*^hubScan$' }
        //     }
        //     steps{
        //         hubScan("${PROJECT_NAME}", "${VERSION}", coreCount: -1)
        //     }
        // }
        // stage('Prepare for scan'){
        //     steps {
        //         sh'''
        //             make export
        //         '''
        //     }
        // }
        // stage('Security Scan Images'){
        //     when {
        //         anyOf { branch '1.0'; branch '2.0'; branch '2.1'; changelog '.*^hubScan$' }
        //     }
        //     steps {
        //         // Validate the images, running a security scan on all docker images
        //         hubScanDocker("${PROJECT_NAME}", "${VERSION}", "${WORKSPACE}/images", coreCount: -1)
        //     }
        // }
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
