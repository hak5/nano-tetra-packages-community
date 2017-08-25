#
# Copyright (C) 2006-2010 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=ettercap
PKG_VERSION:=0.8.2
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://github.com/Ettercap/ettercap/releases/download/v0.8.2/
PKG_MD5SUM:=b6b20851862f55644d5f296f77b785d1

PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/cmake.mk
# include $(INCLUDE_DIR)/nls.mk

define Package/ettercap
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=+libcurl +libpcap +libnet1 +libopenssl +libpcre +libncurses +libltdl +libpthread +zlib +libiconv-full
  TITLE:=Ettercap is a suite for man in the middle attacks on LAN.
  URL:=http://www.ettercap-project.org
endef

define Package/ettercap/description
	It features sniffing of live connections, content filtering on the fly
	and many other interesting tricks.
	It supports active and passive dissection of many protocols (even
	ciphered ones) and includes many feature for network and host analysis.
endef

define Package/ettercap/conffiles
/etc/etter.conf
endef

TARGET_CFLAGS += -I$(STAGING_DIR)/usr/lib/libiconv-full/include

#IPV6 -> LIBNET needed?
CMAKE_OPTIONS += \
	-DHAVE_UTF8:BOOL=OFF \
	-DINSTALL_DESKTOP:BOOL=OFF \
	-DENABLE_GTK:BOOL=OFF \
	-DBUNDLED_LIBS:BOOL=OFF \
	-DLIBNET_INCLUDE_DIR:PATH=$(STAGING_DIR)/usr/lib/libnet-1.1.x/include \
	-DLIBNET_LIBRARY:FILEPATH=$(STAGING_DIR)/usr/lib/libnet-1.1.x/lib/libnet.so \
	-DHAVE_ICONV:FILEPATH=$(STAGING_DIR)/usr/lib/libiconv-full/lib/libiconv.so \
	-DEXECUTABLE_OUTPUT_PATH=$(PKG_BUILD_DIR)/bin_out

define Package/ettercap/install
	$(INSTALL_DIR) $(1)/etc/ettercap
	$(INSTALL_CONF) $(PKG_INSTALL_DIR)/etc/ettercap/etter.* $(1)/etc/ettercap/
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/etter{cap,filter,log} $(1)/usr/bin/
	$(INSTALL_DIR) $(1)/usr/lib/ettercap
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/lib/ettercap/*.so $(1)/usr/lib/ettercap/
	$(INSTALL_DIR) $(1)/usr/lib
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/lib/libettercap.so* $(1)/usr/lib/
	$(INSTALL_DIR) $(1)/usr/share/ettercap
	$(INSTALL_DATA) $(PKG_INSTALL_DIR)/usr/share/ettercap/* $(1)/usr/share/ettercap/
endef

$(eval $(call BuildPackage,ettercap))
