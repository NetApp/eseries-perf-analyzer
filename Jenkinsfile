@Library('hub') _
pipeline {
    agent {
        label 'hub'
    }
    triggers {
        cron('H H(17-20) * * *')
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '3'))
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
					make build
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
                not { triggeredBy 'SCMTrigger' }
            }
            steps {
                // Validate the images, running a security scan
                hubScan("${PROJECT_NAME}", "${VERSION}", coreCount: -1)
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
