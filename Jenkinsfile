pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Tests') {
            steps {
                sh 'java -cp lib/sparql.jar uk.org.floop.sparqlTestRunner.Run -s https://production-drafter-ons-alpha.publishmydata.com/v1/sparql/live'
            }
        }
    }
}
