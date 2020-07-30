#
# Copyright (C) 2019 Andreas Nilsen <adde88@gmail.com>
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=asleap
PKG_VERSION:=2.2
PKG_RELEASE:=3

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)

PKG_LICENSE:=GPL-2.0
PKG_LICENSE_FILES:=COPYING

PKG_MAINTAINER:=Andreas Nilsen <adde88@gmail.com>, Original asleap package: Josh <jwright@hasborg.com>

include $(INCLUDE_DIR)/package.mk

define Package/asleap
	SECTION:=base
	CATEGORY:=Network
	TITLE:=Generic MS-CHAPv2 cracking tool, with pcap support.
	URL:=http://www.willhackforsushi.com
	DEPENDS:=+libpthread +libopenssl +libpcap
endef

define Package/asleap/description
	A generic MS-CHAPv2 cracking tool.
	Can be applied anytime you have a MS-CHAPv2 packet capture available.
endef

define Build/Prepare
        mkdir -p $(PKG_BUILD_DIR)
        $(CP) -rf ./src/* $(PKG_BUILD_DIR)/
endef

define Build/RunMake
	CFLAGS="$(TARGET_CPPFLAGS) $(TARGET_CFLAGS)" \
	$(MAKE) $(PKG_JOBS) -C $(PKG_BUILD_DIR)/$(1) \
		$(TARGET_CONFIGURE_OPTS) \
		LIBS="$(TARGET_LDFLAGS)" \
		LIBS_c="$(TARGET_LDFLAGS_C)" \
		BCHECK= \
		$(2)
endef

define Package/asleap/install
		$(INSTALL_DIR) $(1)/usr/sbin
		$(INSTALL_BIN) $(PKG_BUILD_DIR)/asleap $(1)/usr/sbin/
endef

$(eval $(call BuildPackage,asleap))
