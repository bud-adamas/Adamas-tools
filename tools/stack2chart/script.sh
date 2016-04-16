#!/bin/bash

# this script transforms a serial of gdb stack frames into a flow chart,
# via the 'dot' program, and the color of the edge is random.
# Bud Adamas(adamas@tom.com), Mon, 25 Mar 2013 20:17:22 +0800

E_FILE_NOT_EXIST=71

# the format and the postfix of the output file
postfix=ps

# check there is a parameter
src_filename=${1:?You have to provide the file containing the stack track}

# check that file exists
if [ ! -e ${src_filename} ]
then
	echo "The file ${src_filename} does not exist"
	exit E_FILE_NOT_EXIST
fi

# check whether the 'dot' command exists
which dot > /dev/null
if [ $? != 0 ]
then
	echo "You need a 'dot' program"
	exit E_FILE_NOT_EXIST
fi

tmp_filename=`mktemp`

dot_filename=`mktemp`

dest_file=${src_filename%.*}.${postfix}

# get the stack track in reversive order
cut -d"(" -f1 ${src_filename} |awk -F" " '{print $NF}' > ${tmp_filename}

# rever the stack track, and output aux command
awk -F" " '{lines[num++] = $0} \
			END{ \
				print "digraph G{"; \

				# output all lines
				for(i=num-1; i >0; i--) \
					{print "\t"lines[i]" ->";} \
				print "\t"lines[0]; \

				# output the color
				srand(); \
				red=rand()*1000%256; \
				green=rand()*1000%256; \
				blue=rand()*1000%256; \
				printf "\t[color=\"#%x%x%x\"];\n}", red, green, blue; \
			}' ${tmp_filename} > ${dot_filename}

# draw the flow chart
dot -T${postfix} ${dot_filename} -o ${dest_file}

# remove the temp files
rm -rf ${tmp_filename} ${dot_filename}

exit 0
