pipeline {
    agent any

    environment {
        IMAGE_NAME = 'chevasatrio/flask-db-app'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
        PATH = "C:\\Users\\cheva\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
        COMPOSE_EXE = 'C:\\Users\\cheva\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps {
                bat '''
            echo Memeriksa Docker...
            docker --version
            "%COMPOSE_EXE%" version
        '''
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

        stage('Check Docker Compose') {
            steps {
                bat 'docker --version'
                bat '"%COMPOSE_EXE%" version'
            }
        }

        stage('Deploy dengan Database') {
            steps {
                bat '''
            "%COMPOSE_EXE%" --project-name flaskdb up ^
                -d --build
        '''
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
