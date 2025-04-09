FROM rockylinux:8.9

# We need a few additional packages for installations, xvfb, imagemagick
RUN yum -y update && \
    yum -y install wget zip unzip && \
    yum -y install epel-release && \
    yum -y install ImageMagick && \
    yum -y install xorg-x11-server-Xvfb xorg-x11-xauth && \
    yum clean all

# Don't think we need these for FS anymore because we're going via RPM?
#  mesa-libGLU fontconfig libtiff mesa-dri-drivers

# FS RPM package and patch for csvprint
# https://ftp.nmr.mgh.harvard.edu/pub/dist/lcnpublic/dist/csvprint_8.0.0_patch/README.md
RUN cd /opt && \
    wget -q https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/8.0.0/freesurfer-Rocky8-8.0.0-1.x86_64.rpm && \
    yum -y install /opt/freesurfer-Rocky8-8.0.0-1.x86_64.rpm && \
    rm freesurfer-Rocky8-8.0.0-1.x86_64.rpm
ENV FREESURFER_HOME /usr/local/freesurfer/8.0.0-1
COPY csvprint ${FREESURFER_HOME}/bin/csvprint

# Freesurfer environment
ENV FREESURFER ${FREESURFER_HOME}
ENV FREESURFER_HOME_FSPYTHON ${FREESURFER_HOME}
ENV SUBJECTS_DIR ${FREESURFER_HOME}/subjects
ENV MNI_DIR ${FREESURFER_HOME}/mni
ENV MNI_PERL5LIB ${FREESURFER_HOME}/mni/share/perl5
ENV MINC_BIN_DIR ${FREESURFER_HOME}/mni/bin
ENV MNI_DATAPATH ${FREESURFER_HOME}/mni/data
ENV FSFAST_HOME ${FREESURFER_HOME}/fsfast
ENV FSF_OUTPUT_FORMAT nii.gz
ENV LOCAL_DIR ${FREESURFER_HOME}/local
ENV FMRI_ANALYSIS_DIR ${FREESURFER_HOME}/fsfast
ENV FUNCTIONALS_DIR ${FREESURFER_HOME}/sessions
ENV PERL5LIB ${FREESURFER_HOME}/mni/share/perl5
ENV FS_OVERRIDE 0
ENV LESSOPEN "||/usr/bin/lesspipe.sh %s"
ENV FS_V8_XOPTS 0
ENV PATH /usr/local/freesurfer/8.0.0-1/mni/bin${PATH}
ENV PATH /usr/local/freesurfer/8.0.0-1/tktools:${PATH}
ENV PATH /usr/local/freesurfer/8.0.0-1/fsfast/bin:${PATH}
ENV PATH /usr/local/freesurfer/8.0.0-1/bin:${PATH}

# And add our own code for custom post-processing and QC
COPY README.md /opt/fs-extensions/
COPY README-csvprint.md /opt/fs-extensions/
COPY src /opt/fs-extensions/src
ENV PATH /opt/fs-extensions/src:${PATH}

# Entrypoint
ENTRYPOINT ["run-everything.sh"]
