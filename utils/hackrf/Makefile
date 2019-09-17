#
# Copyright (C) 2008-2014 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=hackrf
PKG_VERSION:=1.0
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/mossmann/hackrf.git
PKG_SOURCE_VERSION:=b9558ba91007d1719c8bb2194a745482d00ffe33
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)


include $(INCLUDE_DIR)/package.mk

define Package/hackrf
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=Great Scott Gadgets HackRF
  URL:=http://greatscottgadgets.com/hackrfone
  MAINTAINER:=Marc Egerton <foxtrot@realloc.me>
endef

define Package/hackrf/description
  HackRF Library and Tools.
endef

define Package/at/install
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/at $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/atd $(1)/usr/sbin
endef

$(eval $(call BuildPackage,hackrf))
