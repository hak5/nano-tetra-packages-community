#
# Copyright (C) 2006-2015 OpenWrt.org
# Copyright (C) 2018 seb@hak5.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=aircrack-ng-hak5
PKG_VERSION:=1.2-rc5
PKG_RELEASE:=1
PKG_LICENSE:=GPLv2

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/aircrack-ng/aircrack-ng.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=7e32bd321147bfef000f7ce4f29613352604323a
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz

PKG_FIXUP:=autoreconf

PKG_BUILD_PARALLEL:=1
PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk

define Package/aircrack-ng-hak5
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=+libpcap +libpthread +libopenssl +libnl +wireless-tools +ethtool +libstdcpp
  TITLE:=WLAN tools for breaking 802.11 WEP/WPA keys
  URL:=http://www.aircrack-ng.org/
  MAINTAINER:=Sebastian Kinne <seb@hak5.org>
  SUBMENU:=wireless
endef

define Package/aircrack-ng-hak5/description
  WLAN tools for breaking 802.11 WEP/WPA keys
endef

CONFIGURE_ARGS+=  --with-ext-scripts \
		  --with-experimental \
		  --without-opt

MAKE_FLAGS+= 	prefix=/usr \
		OSNAME=Linux

CFLAGS="$(TARGET_CFLAGS) -Wall -Iinclude/ $(TARGET_CPPFLAGS) -D_REVISION=0" \

define Package/aircrack-ng-hak5/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/* $(1)/usr/bin/
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/* $(1)/usr/sbin/
endef

$(eval $(call BuildPackage,aircrack-ng-hak5))
