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
		    String id = pmd.drafter.createDraftset(env.JOB_NAME).id
                    def index = readJSON(file: 'vocabs/index.json')
                    for (int i = 0; i < index.size(); i++) {
                        String src = index[i]['src']
                        echo "Adding ${src}..."
                        if (src.startsWith('http')) {
                            pmd.drafter.deleteGraph(id, src)
                            pmd.drafter.addData(id, src, index[i]['format'], 'UTF-8', src)
                        } else {
                            String graph = index[i]['graph']
                            pmd.drafter.deleteGraph(id, graph)
                            pmd.drafter.addData(id, "${WORKSPACE}/${src}", index[i]['format'], 'UTF-8', index[i]['graph'])
                        }
                    }
                    pmd.drafter.publishDraftset(id)
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
