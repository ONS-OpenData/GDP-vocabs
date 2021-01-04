@Library('pmd@family-pmd4') _

import uk.org.floop.jenkins_pmd.Drafter
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
                        def graph = vocab.src
                        if (vocab.src.startsWith('http')) {
                            pmd.drafter.deleteGraph(id, vocab.src)
                            pmd.drafter.addData(id, vocab.src, vocab.format, 'UTF-8', vocab.src)
                        } else {
                            graph = vocab.graph
                            pmd.drafter.deleteGraph(id, graph)
                            pmd.drafter.addData(id, "${WORKSPACE}/${vocab.src}", vocab.format, 'UTF-8', graph)
                        }

                        if (vocab.conceptSchemes != null){
                            for (conceptScheme in vocab.conceptSchemes) {
                                def catalogMetadata = new CatalogMetadata(conceptScheme)
                                def stuff = util.getCatalogMetadata(graph, catalogMetadata)
                                echo stuff
                                writeFile(file: "catalogConceptSchemeMeta.ttl", text: stuff)
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
