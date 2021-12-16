cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 48000
#     tmpdirMin: 8192
#   - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: simroux/virsorter:v1.0.5
label: Virsorter
baseCommand: []
arguments:
  - position: 1
    prefix: '--db'
    valueFrom: '2'
  - position: 2
    valueFrom: '--virome'
  - position: 3
    valueFrom: '--diamond'
  - position: 4
    prefix: '--ncpu'
    valueFrom: '56'

inputs:
  contigs:
    type: File
    inputBinding:
      prefix: --fna
      position: 5

outputs:
  phageContigs:
    type: File
    outputBinding:
      glob: 'virsorter-out/VIRSorter_global-phage-signal.csv'
