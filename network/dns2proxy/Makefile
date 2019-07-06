
#
# Copyright (C) 2019 Andreas Nilsen <adde88@gmail.com> https://github.com/adde88
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=dns2proxy
PKG_VERSION:=1.0
PKG_RELEASE:=3

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)

PKG_MAINTAINER:=Andreas Nilsen <adde88@gmail.com>

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/dns2proxy
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=+python +python-dns +python-pcapy
  TITLE:=Offensive DNS server
  URL:=https://github.com/LeonardoNve/dns2proxy
endef

define Package/dns2proxy/description
  This tools offer a different features for post-explotation once you change
  the DNS server to a Victim. <Referer to help (-h) to new params options>
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) -rf ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/dns2proxy/install
	$(INSTALL_DIR)	$(1)/usr/bin
	$(INSTALL_DIR)	$(1)/etc/dns2proxy/
	$(INSTALL_BIN)	$(PKG_BUILD_DIR)/dns2proxy.py	$(1)/usr/bin/dns2proxy
	$(INSTALL_CONF)	$(PKG_BUILD_DIR)/*.cfg		$(1)/etc/dns2proxy/
	$(INSTALL_BIN)	$(PKG_BUILD_DIR)/handler_msg.sh	$(1)/etc/dns2proxy/
	$(INSTALL_CONF	$(PKG_BUILD_DIR)/resolv.conf	$(1)/etc/dns2proxy/
endef

$(eval $(call BuildPackage,dns2proxy))
