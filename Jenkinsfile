pipeline {
    agent any

    environment {
        IMAGE_GATEWAY = 'harhatilatonttu/llm-telegram-bot-gateway'
        IMAGE_BOT     = 'harhatilatonttu/llm-telegram-bot-bot'
        GIT_REPO      = 'github.com/Vafth/LLM-Telegram-Bot.git'
    }

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
                    cp .env.test.example .env.test

                    uv sync --package bot --package LLM-Telegram-Bot --group dev
                    uv run pytest bot/tests -v

                    uv sync --package gateway --package LLM-Telegram-Bot --group dev
                    uv run pytest gateway/tests -v
                '''
            }
        }

        stage('Build & Push Gateway') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        def img = docker.build("${IMAGE_GATEWAY}:${BUILD_NUMBER}", './gateway')
                        img.push()
                        img.push('latest')
                    }
                }
            }
        }

        stage('Build & Push Bot') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        def img = docker.build("${IMAGE_BOT}:${BUILD_NUMBER}", './bot')
                        img.push()
                        img.push('latest')
                    }
                }
            }
        }

        stage('Update Helm values') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config user.email "jenkins@ci.local"
                        git config user.name "Jenkins CI"

                        sed -i "s|repository:.*# CI_GATEWAY_REPO|repository: ${IMAGE_GATEWAY} # CI_GATEWAY_REPO|" helm/values.yaml
                        sed -i "s|tag:.*# CI_GATEWAY_TAG|tag: \\"${BUILD_NUMBER}\\"  # CI_GATEWAY_TAG|" helm/values.yaml

                        sed -i "s|repository:.*# CI_BOT_REPO|repository: ${IMAGE_BOT} # CI_BOT_REPO|" helm/values.yaml
                        sed -i "s|tag:.*# CI_BOT_TAG|tag: \\"${BUILD_NUMBER}\\"  # CI_BOT_TAG|" helm/values.yaml

                        git add helm/values.yaml
                        git commit -m "ci: update image tags to build ${BUILD_NUMBER} [ci skip]" || echo "Brak zmian do commitu"
                        git push "https://${GIT_USER}:${GIT_TOKEN}@${GIT_REPO}" HEAD:main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}