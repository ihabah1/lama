pipeline {
    agent any
    options {
        timestamps()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Docker build') {
            steps {
                sh 'docker build -t mandel-lotto:${BUILD_NUMBER} .'
            }
        }
        stage('Django check in container') {
            steps {
                sh 'docker run --rm mandel-lotto:${BUILD_NUMBER} python manage.py check'
            }
        }
        stage('Django tests in container') {
            steps {
                sh 'docker run --rm mandel-lotto:${BUILD_NUMBER} python manage.py test analyzer'
            }
        }
    }
}
