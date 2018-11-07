pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Add referenced vocabs') {
            steps {
                script {
                    configFileProvider([configFile(fileId: 'pmd', variable: 'configfile')]) {
                        def config = readJSON(text: readFile(file: configfile))
                        String PMD = config['pmd_api']
                        String credentials = config['credentials']
                        def drafts = drafter.listDraftsets(PMD, credentials, 'owned')
                        def jobDraft = drafts.find { it['display-name'] == env.JOB_NAME }
                        if (jobDraft) {
                            drafter.deleteDraftset(PMD, credentials, jobDraft.id)
                        }
                        def newJobDraft = drafter.createDraftset(PMD, credentials, env.JOB_NAME)
                        def index = readJSON(file: 'vocabs/index.json')
                        for (int i = 0; i < index.size(); i++) {
                            String graph = index[i]['src']
                            String rdf = ""
                            if (graph.startsWith('http')) {
                                def response = httpRequest(url: graph,
                                                           customHeaders: [[name: 'Accept',
                                                                            value: index[i]['format']]])
                                if (response.status == 200) {
                                    rdf = response.content
                                } else {
                                    error "Problem fetching ${url}"
                                }
                            } else {
                                graph = index[i]['graph']
                                rdf = readFile(file: index[i]['src'], encoding: 'UTF-8')
                            }
                            drafter.deleteGraph(PMD, credentials, newJobDraft.id, graph)
                            drafter.addData(PMD, credentials, newJobDraft.id,
                                            rdf, index[i]['format'] + ';charset=UTF-8', graph)
                        }
                        drafter.publishDraftset(PMD, credentials, newJobDraft.id)
                    }
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
