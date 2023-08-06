PROJECT='filesysobjects'
VERSION="0.0.3"
RELEASE="0.0.3"
NICKNAME="Yggdrasil"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='pre-alpha'
MISSION='Support extensions for executables as Units of PyUnit.'

# the absolute pathname for this source
MYPATH=${BASH_SOURCE%/*}/
if [ "X${MYPATH#.}" != "X$MYPATH" ];then
	MYPATH=${PWD}/${MYPATH#.};MYPATH=${MYPATH//\/\//\/}
fi

# input base directory
INDIR=${INDIR:-$MYPATH}
if [ "X${INDIR#.}" != "X$INDIR" ];then
	INDIR=${PWD}/${INDIR#.};INDIR=${INDIR//\/\//\/}
fi

echo "MYPATH=$MYPATH"
echo "INDIR=$INDIR"
 
# output base directory
OUTDIR=${OUTDIR:-build/}
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}"
fi
export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH

# import directory for entries of static reference 
STATIC="${OUTDIR}/apidoc/sphinx/_static"

# source entities
FILEDIRS=""
FILEDIRS="${INDIR}epydoc"
FILEDIRS="$FILEDIRS ${INDIR}UseCases"
FILEDIRS="$FILEDIRS ${INDIR}tests"

CALL=""
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
CALL="$CALL sphinx-apidoc "
CALL="$CALL -A '$AUTHOR'"
CALL="$CALL -H '$PROJECT'"
CALL="$CALL -V '$VERSION'"
CALL="$CALL -R '$RELEASE'"
CALL="$CALL -o ${OUTDIR}/apidoc/sphinx"
CALL="$CALL -f -F "
CALL="$CALL $@"

#
#build=patches
DOCHTML=${OUTDIR}apidoc/sphinx/_build/html/index.html
cat <<EOF
#
# Create apidoc builder...
#
EOF
IFSO=$IFS
IFS=';'
FX=( ${FILEDIRS} )
IFS=$IFSO
for fx in ${FX[@]};do
	echo "CALL=<$CALL '$fx'>"
	eval $CALL "$fx"
done

echo "extensions.append('sphinx.ext.intersphinx.')" >> ${OUTDIR}/apidoc/sphinx/conf.py
echo "sys.path.insert(0, os.path.abspath('$PWD/..'))" >> ${OUTDIR}/apidoc/sphinx/conf.py

# put the docs together
#
cat docsrc/index.rst                     > ${OUTDIR}/apidoc/sphinx/index.rst
{
cat <<EOF
Project data summary:

* PROJECT=${PROJECT}

* MISSION=${MISSION}

* AUTHOR=${AUTHOR}

* COPYRIGHT=${COPYRIGHT}

* LICENSE=${LICENSE}

* VERSION=${VERSION}

* RELEASE=${RELEASE}

* STATUS=${STATUS}

* NICKNAME=${NICKNAME}

  Filesystem based class trees for Python by ${NICKNAME} see \`${NICKNAME}, the mythical tree that connects the nine worlds... <https://en.wikipedia.org/wiki/Yggdrasil>\`_  

EOF
} >> ${OUTDIR}/apidoc/sphinx/index.rst 

#
cat docsrc/pyfilesysobjects.rst > ${OUTDIR}/apidoc/sphinx/pyfilesysobjects.rst
cat docsrc/filesysobjects.rst > ${OUTDIR}/apidoc/sphinx/filesysobjects.rst
cat docsrc/pysourceinfo.rst > ${OUTDIR}/apidoc/sphinx/pysourceinfo.rst
#

#
# static - literal data
cat ArtisticLicense20.html > "${STATIC}/ArtisticLicense20.html"
cat licenses-amendments.txt > "${STATIC}/licenses-amendments.txt"
#
#cp docsrc/lionwhisperer.png "${STATIC}"

#CALL="SPHINXOPTS= "
CALL=" "
#CALL="SPHINXBUILD=sphinx-build PYTHONPATH=$PYTHONPATH "
CALL="export SPHINXBUILD=sphinx-build; "
CALL="$CALL cd ${OUTDIR}/apidoc/sphinx;"
#CALL="$CALL export PYTHONPATH=$PYTHONPATH "
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
#CALL="$CALL export PYTHONPATH=$PYTHONPATH; "
CALL="$CALL make html ;"
CALL="$CALL cd - "
cat <<EOF
#
# Build apidoc...
#
EOF
echo "CALL=<$CALL>"
eval $CALL

echo
echo "display with: firefox -P preview.simple ${DOCHTML}"
echo
