cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 24000
#     tmpdirMin: 4096
hints:
  DockerRequirement:
    dockerPull: virusx/bbmap:36.84--0
label: BBMap 36.84
baseCommand: reformat.sh
arguments:
  # - "-Xmx$(runtime.ram)M"
  # - "nodisk=t"
  # - "out=stdout.sam"
  # - "statsfile=bbmap$(inputs.outFileSuffix).stats"
  # - "covstats=bbmap$(inputs.outFileSuffix).covstats"
   - position: 3
     prefix: "out="
     valueFrom: "interleaved.fasta"
     separate: false

inputs:
  forward:
    type: File
    inputBinding:
      position: 1
      prefix: 'in='
      separate: false
  reverse:
    type: File
    inputBinding:
      position: 2
      prefix: 'in2='
      separate: false
outputs:
  interleaved:
    type: File
    outputBinding:
      glob: 'interleaved.fasta'
