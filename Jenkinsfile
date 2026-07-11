pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    pip install uv
                    uv sync --package bot --package gateway --package LLM-Telegram-Bot --group dev
                    uv run pytest bot/tests gateway/tests -v
                '''
            }
        }

        stage('Build Gateway') {
            steps {
                sh 'docker build -t llm-telegram-bot-gateway:${BUILD_NUMBER} ./gateway'
            }
        }

        stage('Build Bot') {
            steps {
                sh 'docker build -t llm-telegram-bot-bot:${BUILD_NUMBER} ./bot'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed'
        }
    }

}