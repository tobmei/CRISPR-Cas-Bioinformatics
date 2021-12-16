cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 24000
#     tmpdirMin: 4096
hints:
  DockerRequirement:
    # dockerPull: virusx/bbmap:36.84--0
    dockerPull: bryce911/bbtools
label: BBMap 36.84
baseCommand: bbmap.sh
arguments:
  # - "-Xmx$(runtime.ram)M"
  - "nodisk=t"
  # - "out=$(inputs.forward.basename).bbmap.bam"
  - "out=stdout.bam"
  - "statsfile=$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).stats"
  - "covstats=$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).covstats"
  - "covhist=$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).covhist.txt"
  # - "basecov=$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).basecov.txt"
  - "bincov=$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).bincov.txt"

inputs:
  forward:
    type: File
    inputBinding:
      position: 1
      prefix: 'in='
      separate: false
  reverse:
    type: File?
    inputBinding:
      position: 2
      prefix: 'in2='
      separate: false
  reference:
    type: File
    inputBinding:
      position: 3
      prefix: 'ref='
      separate: false
  outFileSuffix:
    type: string
outputs:
  stdout:
    type: stdout
  stats:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).stats"
  covstats:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).covstats"
  covhist:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).covhist.txt"
  # basecov:
  #   type: File
  #   outputBinding:
  #     glob : "$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).basecov.txt"
  bincov:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).bbmap$(inputs.outFileSuffix).bincov.txt"

stdout: $(inputs.forward.basename).bbmap.stdout
