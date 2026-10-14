pipeline {
    agent any

    environment {
        IMAGE_NAME = 'chevasatrio/flask-db-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        PATH = "C:\\Program Files\\Docker\\Docker\\resources\\bin;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps {
                bat 'echo Mulai build aplikasi'
                bat 'docker version'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS,
                        usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }
        stage('Deploy dengan Database') {
            steps {
                bat 'docker compose -p flaskdb up -d --build'
            }
        }
        stage('Verifikasi') {
            steps {
                sleep time: 15, unit: 'SECONDS'
                bat 'curl.exe -f http://localhost:5001/health'
                bat 'curl.exe -f http://localhost:5001/db'
            }
        }
    }

    post {
        always {
            bat(script: 'docker logout', returnStatus: true)
            echo 'Selesai build'
        }
    }
}