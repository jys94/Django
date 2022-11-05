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
      app.push("v${env.BUILD_NUMBER}")
    }
  }
  stage('k8s deploy') {
    sh 'kubectl apply -f django.yaml'
  }
  stage('send diff') {
    script {
      def publisher = LastChanges.getLastChangesPublisher "PREVIOUS_REVISION", "SIDE", "LINE", true, true, "", "", "", "", ""
      publisher.publishLastChanges()
      def htmlDiff = publisher.getHtmlDiff()
      writeFile file: "deploy-diff-${env.BUILD_NUMBER}.html", text: htmlDiff
    }
    slackSend(message: """${env.JOB_NAME} #${env.BUILD_NUMBER} End
    (<${env.BUILD_URL}/last-changes|Check Last changed>)"""
    , color: 'good', tokenCredentialId: 'slack-key')
  }
}
