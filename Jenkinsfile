pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Add referenced vocabs') {
            steps {
                script {
                    def pmd = pmdConfig('pmd')
                    def draftset = pmd.drafter.listDraftsets().find { it['display-name'] == env.JOB_NAME }
                    if (draftset) {
                        pmd.drafter.deleteDraftset(draftset.id)
                    }
                    def newDraftset = pmd.drafter.createDraftset(env.JOB_NAME)
                    for (int i = 0; i < index.size(); i++) {
                        String src = index[i]['src']
                        if (graph.startsWith('http')) {
                            pmd.drafter.deleteGraph(newDraftset.id, src)
                            pmd.drafter.addData(newDraftset.id, src, index[i]['format'], 'UTF-8', src)
                        } else {
                            pmd.drafter.addData(newDraftset.id, "${WORKSPACE}/${src}", index[i]['format'], 'UTF-8', index[i]['graph'])
                        }
                    }
                    pmd.drafter.publishDraftset(newDraftset.id)
                }
            }
        }
    }
    post {
        success {
            build job: '../GDP-tests', wait: false
        }
    }
}
