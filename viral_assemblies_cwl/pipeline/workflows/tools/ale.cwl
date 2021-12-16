cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: ResourceRequirement
    # coresMin: 56
    # ramMin: 48000
    # tmpdirMin: 8192
  - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/ale:20180904--py27ha92aebf_0
label: ALE 20180904
baseCommand: ALE
arguments:
  - position: 1
    valueFrom: '--metagenome'
  - position: 4
    valueFrom: '$(inputs.sam.basename).ALEoutput.ale'
inputs:
  sam:
    type: File
    inputBinding:
      position: 2
  assembly:
    type: File
    inputBinding:
      position: 3
outputs:
  aleOutput:
    type: File
    outputBinding:
      glob: $(inputs.sam.basename).ALEoutput.ale
