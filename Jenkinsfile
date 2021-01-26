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
            agent {
                docker {
                    image 'gsscogs/csv2rdf'
                    reuseNode true
                    alwaysPull true
                }
            }
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

                            def fileContents = util.getUrlAsText(vocab.src, vocab.format)

                            writeFile(file: "${WORKSPACE}/download.file", text: fileContents)
                            localFilePath = "${WORKSPACE}/download.file"
                        } else {
                            graph = vocab.graph
                            localFilePath = "${WORKSPACE}/${vocab.src}"
                        }
                        // Standardise the format so we can augment it if necessary
                        sh "sparql --data \"${localFilePath}\" 'CONSTRUCT {?s ?p ?o.} WHERE {?s ?p ?o.}' > \"${WORKSPACE}/standardised.format.ttl\""
                        
                        if (vocab.augment != null) {
                            for (augmentationQueryFilePath in vocab.augment) {
                                echo "Augmenting with ${augmentationQueryFilePath}"
                                sh "sparql --data \"${WORKSPACE}/standardised.format.ttl\" --query \"${WORKSPACE}/${augmentationQueryFilePath}\" >> \"${WORKSPACE}/standardised.format.ttl\""
                            }
                        }

                        pmd.drafter.deleteGraph(id, graph)
                        pmd.drafter.addData(id, "${WORKSPACE}/standardised.format.ttl", "text/turtle", "UTF-8", graph)

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
