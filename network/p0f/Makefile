include $(TOPDIR)/rules.mk

PKG_NAME:=p0f
PKG_VERSION:=3.09b
PKG_MAINTAINER:=Michal Zalewski <lcamtuf@coredump.cx>

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tgz
PKG_SOURCE_URL:=http://lcamtuf.coredump.cx/p0f3/releases/
PKG_HASH:=543b68638e739be5c3e818c3958c3b124ac0ccb8be62ba274b4241dbdec00e7f

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

#PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk

define Package/p0f
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Passive TCP/IP stack fingerprinting tool
	DEPENDS:=+libpcap +libpthread
	URL:=http://lcamtuf.coredump.cx/p0f3/
	MAINTAINER:=Michal Zalewski <lcamtuf@coredump.cx>
endef

define Package/p0f/description
    p0f is a passive TCP/IP stack fingerprinting tool. p0f can attempt to identify the system running on 
    machines that send network traffic to the box it is running on, or to a machine that shares a medium with 
    the machine it is running on. p0f can also assist in analysing other aspects of the remote system.
endef

#TARGET_CFLAGS += -ggdb3

#define Build/Prepare
#	mkdir -p $(PKG_BUILD_DIR)
#	$(CP) ./src/* $(PKG_BUILD_DIR)/
#endef


define Package/p0f/install
	$(INSTALL_DIR) $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/p0f $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/p0f-client $(1)/usr/sbin/
	$(INSTALL_DIR) $(1)/etc/p0f
	$(CP) $(PKG_BUILD_DIR)/p0f.fp $(1)/etc/p0f/
endef


$(eval $(call BuildPackage,p0f))
