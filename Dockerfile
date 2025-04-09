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

#ENV PATH ${FREESURFER_HOME}/bin:${PATH}
#ENV FREESURFER_FSPYTHON ${FREESURFER_HOME}/bin/fspython
#ENV PATH ${FREESURFER_FSPYTHON}/bin:${PATH}
#ENV FREESURFER_HOME_FSPYTHON ${FREESURFER_FSPYTHON}
#ENV SUBJECTS_DIR ${FREESURFER_HOME}/subjects
#ENV MINC_BIN_DIR ${FREESURFER_HOME}/mni/bin
#ENV MINC_LIB_DIR ${FREESURFER_HOME}/mni/lib
#ENV FS_V8_XOPTS 0

# And add our own code for custom post-processing and QC
COPY README.md /opt/fs-extensions/
COPY README-csvprint.md /opt/fs-extensions/
COPY src /opt/fs-extensions/src
ENV PATH /opt/fs-extensions/src:${PATH}

# Entrypoint
ENTRYPOINT ["run-everything.sh"]
