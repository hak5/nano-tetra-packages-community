#
# Copyright (C) 2019 Andreas Nilsen <adde88@gmail.com> https://github.com/adde88
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=hostapd-mana
PKG_VERSION:=2.6.5
PKG_RELEASE:=15

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)

PKG_MAINTAINER:=Andreas Nilsen <adde88@gmail.com>

PKG_LICENSE:=GPL-2.0
PKG_LICENSE_FILES:=COPYING

PKG_BUILD_PARALLEL:=1

PKG_CONFIG_DEPENDS:= \
	CONFIG_PACKAGE_kmod-ath9k \
	CONFIG_PACKAGE_kmod-cfg80211 \
	CONFIG_PACKAGE_hostapd \
	CONFIG_PACKAGE_hostapd-mini \
	CONFIG_PACKAGE_kmod-hostap \
	CONFIG_DRIVER_WEXT_SUPPORT \
	CONFIG_DRIVER_11N_SUPPORT \
	CONFIG_DRIVER_11AC_SUPPORT \
	CONFIG_DRIVER_TAXONOMY_SUPPORT

include $(INCLUDE_DIR)/package.mk

STAMP_CONFIGURED:=$(STAMP_CONFIGURED)

ifneq ($(CONFIG_DRIVER_11N_SUPPORT),)
  HOSTAPD_IEEE80211N:=y
endif

ifneq ($(CONFIG_DRIVER_11AC_SUPPORT),)
  HOSTAPD_IEEE80211AC:=y
endif

ifneq ($(CONFIG_DRIVER_TAXONOMY),)
  CONFIG_DRIVER_TAXONOMY:=y
endif

DRIVER_MAKEOPTS= \
	CONFIG_ACS=$(CONFIG_PACKAGE_kmod-cfg80211) \
	CONFIG_DRIVER_NL80211=$(CONFIG_PACKAGE_kmod-cfg80211) \
	CONFIG_IEEE80211N=$(HOSTAPD_IEEE80211N) \
	CONFIG_IEEE80211AC=$(HOSTAPD_IEEE80211AC) \
	CONFIG_IEEE80211W=$(CONFIG_DRIVER_11W_SUPPORT) \
	CONFIG_DRIVER_WEXT=$(CONFIG_DRIVER_WEXT_SUPPORT) \
	CONFIG_DRIVER_TAXONOMY=$(CONFIG_DRIVER_TAXONOMY) \

space :=
space +=

ifdef CONFIG_USE_GLIBC
  TARGET_LDFLAGS += -lrt
  TARGET_LDFLAGS_C += -lrt
endif

DRV_DEPENDS:=+PACKAGE_kmod-cfg80211:libnl

define Package/hostapd-mana/config
  source "$(SOURCE)/Config.in"
endef

define Package/hostapd-mana
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Hostapd with support for the MANA and Karma attacks.
  DEPENDS:=$(DRV_DEPENDS) +libubus +libopenssl +libpthread +libnl
  URL:=https://github.com/sensepost/hostapd-mana
  TITLE:=hostapd-mana
endef

define Package/hostapd-mana/description
  This package contains hostapd with support for the MANA/KARMA attacks.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) -rf ./src/* $(PKG_BUILD_DIR)/
endef

ifneq ($(wildcard $(PKG_BUILD_DIR)/.config_*),$(subst .configured_,.config_,$(STAMP_CONFIGURED)))
  define Build/Configure/rebuild
	$(FIND) $(PKG_BUILD_DIR) -name \*.o -or -name \*.a | $(XARGS) rm -f
	rm -f $(PKG_BUILD_DIR)/hostapd/hostapd
	rm -f $(PKG_BUILD_DIR)/wpa_supplicant/wpa_supplicant
	rm -f $(PKG_BUILD_DIR)/.config_*
	touch $(subst .configured_,.config_,$(STAMP_CONFIGURED))
  endef
endif

define Build/Configure
	$(Build/Configure/rebuild)
	$(if $(wildcard ./files/hostapd-mana.config), \
		$(CP) ./files/hostapd-mana.config $(PKG_BUILD_DIR)/hostapd/.config \
	)
endef

TARGET_CPPFLAGS := \
	-I$(STAGING_DIR)/usr/include/libnl3 \
	-I$(PKG_BUILD_DIR)/src/crypto \
	$(TARGET_CPPFLAGS) \
	-DCONFIG_LIBNL30 \
	-D_GNU_SOURCE \

TARGET_CFLAGS += -ffunction-sections -fdata-sections -flto
TARGET_LDFLAGS += -Wl,--gc-sections -flto=jobserver -fuse-linker-plugin -lubox -lubus -lm -lnl-3 -lnl-genl-3 -lnl-route-3 -ldl

define Build/RunMake
        CFLAGS="$(TARGET_CPPFLAGS) $(TARGET_CFLAGS)" \
        $(MAKE) $(PKG_JOBS) -C $(PKG_BUILD_DIR)/$(1) \
		CC="$(TARGET_CC)" \
                $(TARGET_CONFIGURE_OPTS) \
                $(DRIVER_MAKEOPTS) \
                LIBS="$(TARGET_LDFLAGS)" \
                LIBS_c="$(TARGET_LDFLAGS_C)" \
		AR="$(TARGET_CROSS)gcc-ar" \
                BCHECK= \
                $(2)
endef

define Build/Compile/hostapd-mana
	+$(call Build/RunMake,hostapd, \
		hostapd hostapd_cli \
	)
endef

define Build/Compile
	echo "LOCAL TYPE: $(LOCAL_TYPE)"
	echo "BUILD VARIANT: $(BUILD_VARIANT)"
	$(Build/Compile/hostapd-mana)
	$(Build/Compile/full)
endef

define Install/hostapd-mana
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/etc/hostapd-mana/
	$(INSTALL_DIR) $(1)/etc/hostapd-mana/cert
endef

define Package/hostapd-mana/install
	$(call Install/hostapd-mana,$(1))
	$(INSTALL_BIN)  $(PKG_BUILD_DIR)/hostapd/hostapd		$(1)/usr/sbin/hostapd-mana
	$(INSTALL_BIN)  $(PKG_BUILD_DIR)/hostapd/hostapd_cli		$(1)/usr/sbin/mana_cli
	$(INSTALL_BIN)	$(PKG_BUILD_DIR)/files/crackapd/crackapd.py	$(1)/usr/sbin/crackapd
	$(INSTALL_DATA)	$(PKG_BUILD_DIR)/files/crackapd/crackapd.conf	$(1)/etc/hostapd-mana/
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/files/conf/*			$(1)/etc/hostapd-mana/
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/files/cert/*			$(1)/etc/hostapd-mana/cert/
endef

$(eval $(call BuildPackage,hostapd-mana))
