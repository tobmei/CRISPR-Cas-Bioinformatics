cwlVersion: v1.0
class: CommandLineTool

hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/bowtie2:2.2.4--py27h6bb024c_4
label: Bowtie2 2.2.4
baseCommand: bowtie2-build
arguments:
  - position: 3
    valueFrom: 'index'

inputs:
  reference:
    type: File
    inputBinding:
      position: 2

outputs:
  indexes:
    type: File[]
    outputBinding:
      glob: '*.bt2'
