#
# Copyright (C) 2006-2015 OpenWrt.org
# Copyright (C) 2018 seb@hak5.org
# Copyright (C) 2018 adde88@gmail.com
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=aircrack-ng-hak5
PKG_VERSION:=1.2-rc5
PKG_RELEASE:=1
PKG_LICENSE:=GPLv2

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/aircrack-ng/aircrack-ng.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=804b711f5d03362d3cb955b0a12d2e837357ac79
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz

PKG_FIXUP:=autoreconf

PKG_BUILD_PARALLEL:=1
PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk

define Package/aircrack-ng-hak5
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=+libpcap +libpthread +libopenssl +libnl +wireless-tools +ethtool +libstdcpp +libpcre +libsqlite3
  TITLE:=WLAN tools for breaking 802.11 WEP/WPA keys
  URL:=https://www.aircrack-ng.org/
  MAINTAINER:=Andreas Nilsen <adde88@gmail.com>
  SUBMENU:=wireless
endef

define Package/aircrack-ng-hak5/description
  WLAN tools for breaking 802.11 WEP/WPA keys
endef

MAKE_FLAGS+=	pkglibexecdir=/usr/bin \
		prefix=/usr \
		OSNAME=Linux

CFLAGS="$(TARGET_CFLAGS) -Wall -Iinclude/ $(TARGET_CPPFLAGS) -D_REVISION=0" -msse -msse2 -msse3 \

define Package/aircrack-ng-hak5/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/* $(1)/usr/bin/
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/* $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/aircrack-ng--generic $(1)/usr/bin
endef

$(eval $(call BuildPackage,aircrack-ng-hak5))
