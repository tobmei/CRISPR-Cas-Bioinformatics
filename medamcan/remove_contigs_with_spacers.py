from Bio import SeqIO
import sys
import os
import re
import subprocess
import multiprocessing

#spacers = sys.argv[1]  #path to spacer dir
#repeats = sys.argv[2]  #path to repeats dir
rsr_path = sys.argv[1] #path to rsr.fastas
blastdb = sys.argv[2]
assemblies = sys.argv[3]
output_dir = sys.argv[4]

dic = {}
subprocess.call("mkdir {}rsr_out".format(output_dir), shell=True)
subprocess.call("mkdir {}dvf_out".format(output_dir), shell=True)
subprocess.call("mkdir {}vf_out".format(output_dir), shell=True)
subprocess.call("mkdir {}blast_out".format(output_dir), shell=True)
subprocess.call("mkdir {}protospacer".format(output_dir), shell=True)
subprocess.call("chmod 777 {}dvf_out".format(output_dir), shell=True)
def do(rsr):
    # for each spacer, get DR with same group id and concatenate repeat+spacer+repeat and write to file
    # blast rsr against assembled contigs to find contigs with idetified spacers
    # remove identified contigs from assembly
    #id = id.split("_")[0]
    id = rsr.split("_")[0]

    #if os.path.isfile("{}vf_out/{}_protospacer_contigs_result_table.csv".format(output_dir,id)):
        #print("{} already processed".format(id))
    #elif not (os.path.isfile("{}/{}.nhr".format(blastdb,id))):
        #print("no blast. skipping {}".format(id))
    if not os.path.isfile("{}/{}.a.fna".format(assemblies,id)):
        print("no contigs. skipping {}".format(id))
    elif not (os.path.isfile("{}/{}.a.fna.nhr".format(blastdb,id)) | os.path.isfile("{}/{}.a.fna.00.nhr".format(blastdb,id))):
        print("no blast. skipping {}".format(id))


    else:
        #print("processing: "+spacers+"/{}_spacer.fasta".format(ncbi))
        print("running blastn on {}".format(id))
        #subprocess.call("blastn -db /data/tobias/databases/ncbi_opt_blastdb/{}_megahit_out_blastdb -query /data/tobias/ncbi_crispr_arrays/rs_sr/{}_rsr.fasta -num_threads 1 -evalue 0.0001 -outfmt '6 std qlen slen' | awk '{{if ($5<=3 && $6<=1 && ($13-$4)<=3) print $0}}'  > {}/blast_out/{}_blastout.txt".format(ncbi,ncbi,output_dir,ncbi), shell=True)
        #subprocess.call("blastn -db {}/{} -query {}/{}_rsr.fasta -num_threads 1 -evalue 0.0001 -outfmt '6 std qlen slen' | awk '{{if ($5<=3 && $6<=1 && ($13-$4)<=3) print $0}}'  > {}/blast_out/{}_blastout.txt".format(blastdb,id,rsr_path,id,output_dir,id), shell=True)
        subprocess.call("blastn -db {}/{}.a.fna -query {}/{}_rsr.fasta -num_threads 1 -evalue 0.0001 -outfmt '6 std qlen slen' | awk '{{if ($5<=3 && $6<=1 && ($13-$4)<=3) print $0}}'  > {}/blast_out/{}_blastout.txt".format(blastdb,id,rsr_path,id,output_dir,id), shell=True)
        subprocess.call("cat {}/blast_out/{}_blastout.txt | cut -f2 | sort | uniq > {}/rsr_out/{}_all_contig_ids.txt".format(output_dir,id,output_dir,id), shell=True)
        subprocess.call("cat {}/blast_out/{}_blastout.txt | grep -e _sr_ -e _rs_ -e _rsr_ | cut -f2 | sort | uniq > {}/rsr_out/{}_contigs_to_remove_ids.txt".format(output_dir,id,output_dir,id), shell=True)
        subprocess.call("diff {}/rsr_out/{}_contigs_to_remove_ids.txt {}/rsr_out/{}_all_contig_ids.txt | awk '/^>/ {{print $2}}' > {}/rsr_out/{}_protospacer_contig_ids.txt".format(output_dir,id,output_dir,id,output_dir,id), shell=True)
        #subprocess.call("cat {}/rsr_out/{}_contigs_to_remove_ids.txt | xargs -n 1 sh -c 'grep $0 {}/blast_out/{}_blastout.txt' > {}/blast_out/{}_crispr_blastout.txt".format(output_dir,id,output_dir,id,output_dir,id), shell=True)
        #subprocess.call("cat {}/rsr_out/{}_contigs_to_remove_ids.txt | xargs -n 1 sh -c 'grep -v $0 {}/blast_out/{}_blastout.txt' > {}/blast_out/{}_protospacer_blastout.txt".format(output_dir,id,output_dir,id,output_dir,id), shell=True)
        #subprocess.call("cat {}/blast_out/{}_protospacer_blastout.txt | cut -f2 | sort | uniq > {}/rsr_out/{}_protospacer_contig_ids.txt".format(output_dir,id,output_dir,id), shell=True)
        #subprocess.call("grep -w -A 1 -f {}/rsr_out/{}_protospacer_contig_ids.txt {}/{}/final.contigs.fa --no-group-separator > {}/protospacer/{}_protospacer_contigs.fasta".format(output_dir,id,assemblies,id,output_dir,id), shell=True)
        subprocess.call("grep -w -A 1 -f {}/rsr_out/{}_protospacer_contig_ids.txt {}/{}.a.fna.wrapped.fasta --no-group-separator > {}/protospacer/{}_protospacer_contigs.fasta".format(output_dir,id,assemblies,id,output_dir,id), shell=True)
        #subprocess.call("grep -w -A 1 -f {}/rsr_out/{}_protospacer_contig_ids.txt {}/{}_megahit_out/final.contigs.fa --no-group-separator > {}/protospacer/{}_protospacer_contigs.fasta".format(output_dir,id,assemblies,id,output_dir,id), shell=True)

        print("running dvf on {}".format(id))
        subprocess.call("docker run --rm -v {}:/workdir deepvirfinder -i /workdir/protospacer/{}_protospacer_contigs.fasta -o /workdir/dvf_out/{}_dvf".format(output_dir,id,id), shell=True)

        print("running viralverify on {}".format(id))
        subprocess.call("/home/tmeier/tools/viralVerify/viralverify.py -f {}/protospacer/{}_protospacer_contigs.fasta --hmm /data/tobias/databases/nbc_hmms.hmm.gz -o {}/vf_out -t 1".format(output_dir,id,output_dir), shell=True)


def multi():
    processes_nr = 170

    # create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    for rsr in os.listdir(rsr_path):
        pool.apply_async(do, args=(rsr,))
        #break
        #do(rsr)
    pool.close()
    pool.join()

multi()





# from Bio import SeqIO
# import sys
# import os
# import re
# import subprocess
# import multiprocessing
#
# spacers = sys.argv[1]
# repeats = sys.argv[2]
# output_dir = sys.argv[3]
#
# dic = {}
#
# def do(spacer):
#
#     # for each spacer, get DR with same group id and concatenate repeat+spacer+repeat and write to file
#     # blast rsr against assembled contigs to find contigs with idetified spacers
#     # remove identified contigs from assembly
#
#     print("processing: {}".format(spacer))
#     outfile = open("{}/{}_rsr.fasta".format(output_dir,spacer), "w")
#
#     with open(spacers+"/"+spacer, "rU") as handle:
#         for record in SeqIO.parse(handle, "fasta"):
#             group = re.search(r".*_G([0-9]+)SP([0-9]+)", record.id).group(1)
#             sp_id = re.search(r".*_G([0-9]+)SP([0-9]+)", record.id).group(2)
#
#             rsr = dic[group] + record.seq + dic[group]
#             outfile.write(">{}_G{}_{}\n".format(spacer,group,sp_id))
#             outfile.write(str(rsr)+"\n")
#
#     outfile.close()
#
#     print("blasting...")
#     subprocess.call("blastn -db /data/tobias/databases/opt_assemblies_blastdb/{}_blastdb -query {}/{}_rsr.fasta -outfmt '6 std qlen' | awk '{{if ($5<=2 && $6<=2 && ($13-$4)<=5)print $2}}' | sort | uniq > {}/{}_contigs_to_remove".format(spacer,output_dir,spacer,output_dir,spacer), shell=True)
#
#     print("removing contigs with spacers...")
#     subprocess.call("awk 'BEGIN{{while((getline<\"{}/{}_contigs_to_remove\")>0)l[\">\"$1]=1}}/^>/{{f=!l[$1]}}f' /data/tobias/ncbi_assemblies/opt_assemblies/{} > {}/{}_no_spacer_contigs.fasta".format(output_dir,spacer,spacer,output_dir,spacer), shell=True)
#
#     print("makeblastdb...")
#     #subprocess.call("cd ncbi_generic_no_spacer_contigs_blastdb", shell=True)
#     subprocess.call("makeblastdb -in {}/{}_no_spacer_contigs.fasta -dbtype nucl -parse_seqids -out /data/tobias/databases/opt_assemblies_blastdb/{}_no_spacer_contigs_blastdb -title {}_no_spacer_contigs_blastdb".format(output_dir,spacer,spacer,spacer), shell=True)
#
#
#
# def multi():
#     processes_nr = 10
#
#     # get group id and corresponding DR
#     for repeat in os.listdir(repeats):
#         with open(repeats + "/" + repeat, "rU") as handle:
#             for record in SeqIO.parse(handle, "fasta"):
#                 group = re.search(r".*_G([0-9]+)", record.id).group(1)
#                 # print(group)
#                 dic[group] = record.seq
#
#     # create a pool of workers
#     print("creating multiprocessing pool with {} workers...".format(processes_nr))
#     pool = multiprocessing.Pool(processes=processes_nr)
#     for spacer in os.listdir(spacers):
#         pool.apply_async(do, args=(spacer,))
#     pool.close()
#     pool.join()
#
# multi()