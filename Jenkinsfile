pipeline {
    agent {
        label 'hub'
    }
    triggers {
        cron('H H(17-20) * * *')
    }
    options {
        timeout(time: 1, unit: 'HOURS')
    }
    environment {
        TAG = "${BUILD_NUMBER}"
        PROJECT_NAME = "esg-grafana"
        VERSION = "1.0"
    }
    stages {
        stage('Run docker builds') {
            environment {
                TAG = "${BUILD_NUMBER}"
                QUIET = "yes"
                # This determines what repositories to use for building the images
                PIP_CONF = 'pip.conf.internal'
                ALPINE_REPO_FILE = 'repositories.internal'
            }
            steps {
				sh'''
					make build-nc
				'''
                sh 'echo ${GIT_COMMIT}'
            }
        }
        stage('Prepare for scan'){
            steps {
                sh'''
                    make export
                '''
            }
        }
        stage('Security Scan'){
            when{
                // When triggered based on time or based on a user interaction
                anyOf { triggeredBy 'TimerTrigger'; triggeredBy cause: "UserCause"}
            }
            steps {
                // Validate the images, running a security scan
                hubScan("${PROJECT_NAME}", "${VERSION}")
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
