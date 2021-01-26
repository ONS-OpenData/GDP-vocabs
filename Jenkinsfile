@Library('pmd@family-pmd4') _

import uk.org.floop.jenkins_pmd.Drafter
import uk.org.floop.jenkins_pmd.PMDConfig
import uk.org.floop.jenkins_pmd.models.CatalogMetadata

pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Add referenced vocabs') {
            steps {
                script {
                    def pmd = pmdConfig('pmd')
                    for (myDraft in pmd.drafter
                            .listDraftsets(Drafter.Include.OWNED)
                            .findAll { it['display-name'] == env.JOB_NAME }) {
                        pmd.drafter.deleteDraftset(myDraft.id)
                    }
                    def id = pmd.drafter.createDraftset(env.JOB_NAME).id
                    for (graph in util.jobGraphs(pmd, id)) {
                        pmd.drafter.deleteGraph(id, graph)
                        echo "Removing own graph ${graph}"
                    }
                    for (vocab in readJSON(file: 'vocabs/index.json')) {
                        echo "Adding ${vocab.src}..."
                        String graph, localFilePath
                        if (vocab.src.startsWith('http')) {
                            graph = vocab.src

                            def fileContents = util.getUrlAsText(vocab.src)

                            writeFile(file: "${WORKSPACE}/download.ttl", text: fileContents)
                            localFilePath = "${WORKSPACE}/download.ttl"
                        } else {
                            graph = vocab.graph
                            localFilePath = "${WORKSPACE}/${vocab.src}"
                        }
                        pmd.drafter.deleteGraph(id, graph)
                        pmd.drafter.addData(id, localFilePath, vocab.format, 'UTF-8', graph)

                        if (vocab.conceptSchemes != null){
                            for (conceptScheme in vocab.conceptSchemes) {
                                def catalogMetadata = new CatalogMetadata(conceptScheme)
                                writeFile(file: "catalogConceptSchemeMeta.ttl", text: util.getCatalogMetadata(graph, catalogMetadata))
                                pmd.drafter.addData(id, "${WORKSPACE}/catalogConceptSchemeMeta.ttl", "text/turtle", 'UTF-8', graph)
                            }
                        }

                        writeFile(file: "prov.ttl", text: util.jobPROV(graph))
                        pmd.drafter.addData(id, "${WORKSPACE}/prov.ttl", "text/turtle", "UTF-8", graph)
                    }
                    pmd.drafter.publishDraftset(id)
                }
            }
        }
    }
}
