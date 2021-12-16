cwlVersion: v1.0
class: CommandLineTool
# requirements:
    # - class: ResourceRequirement
    # coresMin: 56
    # coresMax: 56
    # ramMin: 2048
    # tmpdirMin: 4096
hints:
  DockerRequirement:
    #dockerPull: quay.io/biocontainers/trimmomatic:0.38--0
    dockerPull: comics/trimmomatic
label: Trimmomatic 0.38
baseCommand: java
arguments:
  - "-jar"
  - "/software/applications/Trimmomatic/0.36/trimmomatic-0.36.jar"
  - "PE"
  - "-baseout"
  - "$(inputs.forward.basename)"
  - "-threads"
  - "48"
inputs:
  forward:
    type: File
    inputBinding:
      position: 1
  reverse:
    type: File
    inputBinding:
      position: 2
  headcrop:
    type: int?
    inputBinding:
      position: 3
      prefix: 'HEADCROP:'
      separate: false
  illuminaclip:
    type: string
    inputBinding:
      position: 4
      prefix: 'ILLUMINACLIP:/usr/local/share/trimmomatic-0.38-0/adapters/'
      separate: false
  illuminaclip2:
    type: string?
    inputBinding:
      position: 5
      prefix: 'ILLUMINACLIP:/usr/local/share/trimmomatic-0.38-0/adapters/'
      separate: false
  illuminaclip3:
    type: string?
    inputBinding:
      position: 6
      prefix: 'ILLUMINACLIP:/usr/local/share/trimmomatic-0.38-0/adapters/'
      separate: false
  illuminaclip4:
    type: string?
    inputBinding:
      position: 6
      prefix: 'ILLUMINACLIP:/usr/local/share/trimmomatic-0.38-0/adapters/'
      separate: false
  crop:
    type: int?
    inputBinding:
      position: 7
      prefix: 'CROP:'
      separate: false
  leading:
    type: int?
    inputBinding:
      position: 8
      prefix: 'LEADING:'
      separate: false
  trailing:
    type: int?
    inputBinding:
      position: 9
      prefix: 'TRAILING:'
      separate: false
  slidingwindow:
    type: string?
    inputBinding:
      position: 10
      prefix: 'SLIDINGWINDOW:'
      separate: false
  minlen:
    type: int?
    inputBinding:
      position: 20
      prefix: 'MINLEN:'
      separate: false
outputs:
  forwardPaired:
    type: File
    outputBinding:
      glob: '*_1P.fastq.gz'
  reversePaired:
    type: File
    outputBinding:
      glob: "*_2P.fastq.gz"
  forwardUnpaired:
    type: File
    outputBinding:
      glob: "*_1U.fastq.gz"
  reverseUnpaired:
    type: File
    outputBinding:
      glob: "*_2U.fastq.gz"
  log:
    type: stdout
stderr: $(inputs.forward.basename).log
