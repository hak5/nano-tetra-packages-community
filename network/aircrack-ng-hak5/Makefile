#
# Copyright (C) 2006-2015 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=aircrack-ng-hak5
PKG_VERSION:=1.5.2
PKG_RELEASE:=$(PKG_SOURCE_VERSION)
PKG_LICENSE:=GPL-2.0
PKG_LICENSE_FILES:=LICENSE

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/aircrack-ng/aircrack-ng.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=42f2b48d7f46b39e0d5d2f2a64cbf63f87416a70
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.xz
PKG_MIRROR_HASH:=17893e05278635675a77a3cb0927202ec4df2fc9a742689a7a88e4a8f27a69b6

PKG_BUILD_PARALLEL:=1
PKG_INSTALL:=1

PKG_MAINTAINER:=Marc E. <marc@hak5.org>

PKG_FIXUP:=autoreconf

PKG_CONFIG_DEPENDS:= \
	CONFIG_AIRCRACK_NG_HAK5_GCRYPT \
	CONFIG_AIRCRACK_NG_HAK5_OPENSSL \
	\
	CONFIG_AIRCRACK_NG_HAK5_OPTIMIZE_SPEED \
	\
	CONFIG_AIRCRACK_NG_HAK5_HWLOC \
	CONFIG_AIRCRACK_NG_HAK5_SQLITE3

include $(INCLUDE_DIR)/uclibc++.mk
include $(INCLUDE_DIR)/package.mk

define Package/aircrack-ng-hak5
	SECTION:=net
	CATEGORY:=Network
	DEPENDS:=+libpcap +libpcre +libpthread $(CXX_DEPENDS)
	DEPENDS += +AIRCRACK_NG_HAK5_HWLOC:libhwloc
	DEPENDS += +AIRCRACK_NG_HAK5_OPENSSL:libopenssl
	DEPENDS += +AIRCRACK_NG_HAK5_GCRYPT:libgcrypt
	DEPENDS += +AIRCRACK_NG_HAK5_SQLITE3:libsqlite3
	DEPENDS += +libnl-core +libnl-genl +zlib
	TITLE:=WLAN Cracking and Sniffing tools (Hak5)
  	URL:=https://www.aircrack-ng.org/
  	SUBMENU:=Wireless
endef

define Package/aircrack-ng-hak5/description
	WLAN Cracking and Sniffing tools
	Some tools in this package are omitted for saving space.
endef

define Package/aircrack-ng-hak5/config
  	source "$(SOURCE)/Config.in"
endef

define Build/Prepare
	$(call Build/Prepare/Default)
	echo "$(PKG_VERSION)_rev$(PKG_SOURCE_VERSION)" > $(PKG_BUILD_DIR)/VERSION
endef

CONFIGURE_ARGS += \
	--disable-silent-rules \
	--enable-shared \
	--with-experimental \
	--with-libpcap-include=$(STAGING_DIR)/usr/include \
	--with-libpcap-lib=$(STAGING_DIR)/usr/lib \
	--without-opt \
	\
	PYTHON=$(PYTHON) \
	\
	$(if $(CONFIG_AIRCRACK_NG_HAK5_OPENSSL),,--without-openssl) \
	$(if $(CONFIG_AIRCRACK_NG_HAK5_GCRYPT),--with-gcrypt,--without-gcrypt) \
	$(if $(CONFIG_AIRCRACK_NG_HAK5_HWLOC),--enable-hwloc,--disable-hwloc) \
	$(if $(CONFIG_AIRCRACK_NG_HAK5_SQLITE3),--with-sqlite3=$(STAGING_DIR)/usr,--without-sqlite3)

TARGET_CFLAGS += -Wall -Wextra -ffunction-sections -fdata-sections

ifeq ($(CONFIG_AIRCRACK_NG_OPTIMIZE_SPEED),y)
	TARGET_CFLAGS := $(filter-out -O%,$(TARGET_CFLAGS)) -O3
endif

TARGET_LDFLAGS+= \
	-Wl,--gc-sections

define Package/aircrack-ng-hak5/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/aircrack-ng $(1)/usr/bin/
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/aireplay-ng $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/airmon-ng $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/airodump-ng $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/sbin/airodump-ng-oui-update $(1)/usr/sbin/
	$(INSTALL_DIR) $(1)/usr/lib
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/lib/* $(1)/usr/lib/
endef

$(eval $(call BuildPackage,aircrack-ng-hak5))
