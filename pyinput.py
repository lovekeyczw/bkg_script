# input 1 is the directory for samples, input 2 is the temp steer file, input 3 is the num of events each steer contains
import os, sys, string
import glob

pwd=os.getcwd()
#temp=pwd+"/steers/EXC2_0000011_160214/"
temp=pwd+"/steer/"
outdir=pwd+'/4f/'

listforbid=['sze_l0e']
list20w=['qq','bhabha','e2e2','e3e3','nn','sze_l0mu','sw_l0mu','sw_l0tau','sw_sl0qq']
list2w =['Pzz_l0taumu','Pzz_l0mumu','Pzz_l0tautau','Pzz_l04mu','Pzz_l04tau']

if int(sys.argv[3]) == 0:
	threshold = 1000000000000
else: threshold = int(sys.argv[3])

if os.path.isdir(sys.argv[1]):
	prod    = sys.argv[4]
	print prod
	os.system('mkdir -p '+temp+prod)
	os.system('mkdir -p '+outdir+prod)
	filelist = os.listdir(sys.argv[1])
	i=0
	j=1
	inputfiles=''
	total=0
	for file in filelist:
		subprod = file.split('.')[0]
		num=200
		if subprod==prod:
			tempstr= sys.argv[1]+'/'+file+'\n\t'
			inputfiles+="LCIOInputFiles "+tempstr
			total+=num
			j+=1
			if total>=threshold or j>100:
				outroot = outdir+prod+'/'+prod+str(i)+'.root'
				os.system('cp '+sys.argv[2]+' '+temp+prod+'/'+prod+str(i)+'.steer -f')
				os.system('cp PBSJOBS_temp '+temp+prod+'/'+prod+str(i)+'.pbs -f')
				steer_file  = open(temp+prod+'/'+prod+str(i)+'.steer','r')
	                	lines = steer_file.readlines()
	                	steer_file  = open(temp+prod+'/'+prod+str(i)+'.steer','w')
	                	for s in lines:
	                        	steer_file.write( s.replace('%input%',inputfiles).replace('%output%', outroot))
	                	steer_file.close()
				pbs_file  = open(temp+prod+'/'+prod+str(i)+'.pbs','r')
	                        lines = pbs_file.readlines()
	                        pbs_file  = open(temp+prod+'/'+prod+str(i)+'.pbs','w')
	                        for s in lines:
	                                pbs_file.write( s.replace('%name%', prod+str(i)).replace('%log%',temp+prod+'/'+prod+str(i)).replace('%path%', temp+prod))
	                        pbs_file.close()
				i+=1
				total=0
				inputfiles=''
				j=1
	if total != 0:
		outroot = outdir+prod+'/'+prod+str(i)+'.root'
		os.system('cp '+sys.argv[2]+' '+temp+prod+'/'+prod+str(i)+'.steer -f')
		os.system('cp PBSJOBS_temp '+temp+prod+'/'+prod+str(i)+'.pbs -f')
		steer_file  = open(temp+prod+'/'+prod+str(i)+'.steer','r')
		lines = steer_file.readlines()
		steer_file  = open(temp+prod+'/'+prod+str(i)+'.steer','w')
		for s in lines:
	       		steer_file.write( s.replace('%input%',inputfiles).replace('%output%', outroot))
		steer_file.close()
		pbs_file  = open(temp+prod+'/'+prod+str(i)+'.pbs','r')
		lines = pbs_file.readlines()
		pbs_file  = open(temp+prod+'/'+prod+str(i)+'.pbs','w')
		for s in lines:
       			pbs_file.write( s.replace('%name%', prod+str(i)).replace('%log%', temp+prod+'/'+prod+str(i)).replace('%path%', temp+prod))
		pbs_file.close()

	sub_txt = 'for dir in `ls`\ndo\nfor file in `ls $dir | grep .pbs`\ndo\nqsub -q hsimq $dir/$file\ndone\ndone'
	sub_file = open(temp+'/sub_all.sh','w')
	sub_file.write(sub_txt)
	sub_file.close()
else:
	print 'Dir is required'
