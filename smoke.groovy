pipeline{
    agent any
    stages{
stage('Installing packages') {
            steps {
                script {
                    bat 'pip install -r requirements.txt'
                }
            }
        }
        stage('Running Unit tests') {
            steps {
                   echo "${email}"
                    echo "${host}"
                script {
                    bat "behave -D emailReceiver=${email} -D host=${host}"
                }
            }
        }
    }
}