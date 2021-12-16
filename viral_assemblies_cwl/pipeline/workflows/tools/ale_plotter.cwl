cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/ale:20180904--py27ha92aebf_0
label: ALE 20180904
baseCommand: plotter3.py

inputs:
  aleout:
    type: File
    inputBinding:
      position: 2

  specificContig:
    type: string
    inputBinding:
      position: 1
      prefix: '-sc'

outputs:
  plot:
    type: File
    outputBinding:
      glob: '*.pdf'
  stderr:
    type: stderr
  stdout:
    type: stdout
stderr: plotter.stderr
stdout: plotter.stdout
