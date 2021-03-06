#############################################################
#
# expat
#
#############################################################

EXPAT_VERSION = 2.0.1
EXPAT_SOURCE = expat-$(EXPAT_VERSION).tar.gz
EXPAT_SITE = $(BR2_SOURCEFORGE_MIRROR)/project/expat/expat/$(EXPAT_VERSION)

EXPAT_LIBTOOL_PATCH = NO
EXPAT_INSTALL_STAGING = YES
EXPAT_INSTALL_TARGET = YES

EXPAT_INSTALL_STAGING_OPT = DESTDIR=$(STAGING_DIR) installlib
EXPAT_INSTALL_TARGET_OPT = DESTDIR=$(TARGET_DIR) installlib
EXPAT_HOST_INSTALL_OPT = DESTDIR=$(HOST_DIR) installlib

EXPAT_CONF_OPT = --enable-shared
EXPAT_DEPENDENCIES = uclibc host-pkgconfig

$(eval $(call AUTOTARGETS,package,expat))

$(eval $(call AUTOTARGETS_HOST,package,expat))
