pipeline {
    agent any
    stages {
        stage('Run docker builds') {
            environment {
                TAG = "${BUILD_NUMBER}"
                PROJECT_NAME = "grafana"
                RETRIES = 3
            }
            steps {
                sh 'docker-compose -p ${PROJECT_NAME}-${BRANCH_NAME}-${BUILD_NUMBER} build --pull --no-cache --parallel'
                retry ("${RETRIES}") {
                    sh 'docker build ansible'
                }
                sh 'echo ${GIT_COMMIT}'
            }
        }
    }
}
