cwlVersion: v1.0
class: CommandLineTool

requirements:
  InitialWorkDirRequirement:
    listing:
      - .bt2


hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/bowtie2:2.2.4--py27h6bb024c_4
label: Bowtie2 2.2.4
baseCommand: bowtie2
arguments:
  - position: 1
    prefix: '--threads'
    valueFrom: '56'
  - position: 2
    prefix: '--local'
  - position: 3
    prefix: '--very-sensitive-local'
  - position: 4
    prefix: '-x'
    valueFrom: 'index'
  - position: 7
    prefix: '-S'
    valueFrom: '$(inputs.mate1.basename).sam'
inputs:
  mate1:
    type: File
    inputBinding:
      position: 5
      prefix: '-1'
  mate2:
    type: File
    inputBinding:
      prefix: '-2'
      position: 6

outputs:
  sam:
    type: File
    outputBinding:
      glob: '*.sam'
