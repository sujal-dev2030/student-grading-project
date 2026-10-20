
pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'DEPLOY_TO_K8S',
            defaultValue: false,
            description: 'Deploy the application to Kubernetes'
        )
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'py -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'py -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t student-grade-devops:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { params.DEPLOY_TO_K8S }
            }
            steps {
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl rollout status deployment/student-grade-devops --timeout=120s'
            }
        }
    }

    post {
        success {
            echo 'Student Grade DevOps pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
