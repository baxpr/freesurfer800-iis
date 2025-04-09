FROM rockylinux:8.9

# We need a few additional packages for installations, freeview, imagemagick
RUN yum -y update && \
    yum -y install wget zip unzip && \
    yum -y install epel-release && \
    yum -y install ImageMagick && \
    yum -y install xorg-x11-server-Xvfb xorg-x11-xauth && \
    yum -y install mesa-libGLU fontconfig libtiff mesa-dri-drivers && \
    yum clean all

# FS RPM package
RUN cd /opt && \
    wget https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/8.0.0/freesurfer-Rocky8-8.0.0-1.x86_64.rpm && \
    yum install freesurfer-Rocky8-8.0.0-1.x86_64.rpm

# And add our own code for custom post-processing and QC
COPY README.md /opt/fs-extensions/
COPY src /opt/fs-extensions/src

# System path needs the freesurfer python, plus our code
ENV PATH /opt/fs-extensions/src:${FREESURFER_HOME}/python/bin:${PATH}

# Entrypoint
ENTRYPOINT ["run-everything.sh"]
