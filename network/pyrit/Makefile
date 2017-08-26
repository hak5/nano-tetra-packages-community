#
# Copyright (C) 2011 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=pyrit
PKG_VERSION:=0.5.1
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/JPaulMora/Pyrit.git
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_VERSION:=HEAD
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)

PKG_BUILD_PARALLEL:=1

PKG_MAINTAINER:=Andreas Nilsen <adde88@gmail.com>

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/pyrit
  SECTION:=net
  CATEGORY:=Network
  DEPENDS:=+python +libopenssl +libpcap
  TITLE:=A GPGPU-driven WPA/WPA2-PSK key cracker
  URL:=http://code.google.com/p/pyrit/
endef

define Package/pyrit/description
 A GPGPU-driven WPA/WPA2-PSK key cracker
 Pyrit exploits the computational power of many-core- and GPGPU-
 -platforms to create massive databases, pre-computing part of the 
 WPA/WPA2-PSK authentication phase in a space-time tradeoff. 
 It is a powerful attack against one of the world's most used security
 protocols
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Package/pyrit/install
	$(INSTALL_DIR) $(1)
	$(CP) $(PKG_INSTALL_DIR)/* $(1)/
endef

$(eval $(call BuildPackage,pyrit))
