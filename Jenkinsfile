node {
  stage('deploy start') {
    slackSend(message: "Deploy ${env.BUILD_NUMBER} Started", color: 'good', tokenCredentialId: 'slack-key')
  }
  stage('Clone repository') {
    checkout scm
  }
  stage('git pull') {
    git url: 'https://github.com/jys94/Django.git', branch: 'main'
  }
  stage('Push image') {
    sh 'rm ~/.dockercfg || true'
    sh 'rm ~/.docker/config.json || true'

    docker.withRegistry('https://739362892804.dkr.ecr.ap-northeast-2.amazonaws.com', 'ecr:ap-northeast-2:jenkins-ecr-access-credential') {
      app = docker.build('739362892804.dkr.ecr.ap-northeast-2.amazonaws.com/django')
      app.push('v${env.BUILD_NUMBER}')
    }
  }
  stage('k8s deploy') {
    sh 'kubectl apply -f django.yaml'
  }
  stage('deploy end') {
    slackSend(message: """${env.JOB_NAME} #${env.BUILD_NUMBER} End
    """, color: 'good', tokenCredentialId: 'slack-key')
  }
}
