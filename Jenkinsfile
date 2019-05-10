pipeline {
    agent any
    stages {
        stage('Run docker builds') {
            environment {
                TAG = "${BUILD_NUMBER}"
                PROJECT_NAME = "grafana"
                RETRIES = 3
                QUIET = "yes"
            }
            steps {
				sh'''
					make build-nc
					make rm
				'''
                sh 'echo ${GIT_COMMIT}'
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
